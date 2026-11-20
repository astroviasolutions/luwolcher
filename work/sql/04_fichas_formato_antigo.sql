-- PROBLEMA 4 — Fichas (clients.anamnese) do formato antigo.  NÃO APLICADO: aguarda OK do Christian.
-- Regra: só ACRESCENTA as chaves novas que faltam. Nunca apaga nem sobrescreve nada (chaves antigas ficam).
-- Fato verificado (só leitura, 20/11): 307 fichas têm chaves antigas; 249 já têm as novas espelhadas
-- pela importação; 54 têm só as antigas. Este script cobre essas 54 (e qualquer ficha com lacuna).

-- 1) Backup (rodar antes)
create table if not exists clients_anamnese_bkp_20261120 as
  select id, anamnese, now() as bkp_em from clients where anamnese is not null;

-- 2) DRY-RUN: quantas fichas seriam alteradas (esperado ≈ 54)
-- select count(*) from clients c where jsonb_typeof(anamnese)='object'
--  and anamnese ?| array['FUMANTE','INGERE ALCOOL','INGERE AGUA?','QUALIDADE DE SONO','BOA ALIMENTAÇAO','FAZ ATIVIDADE FISICA']
--  and not anamnese ?& array['smoker','alcohol','water','sleep','diet','exercise'];

-- 3) Migração
create or replace function pg_temp.sn(v text) returns text language sql immutable as $$
  select case when v is null then null
    when upper(trim(v)) like 'SIM%' then 'Sim'
    when upper(trim(v)) in ('NÃO','NAO') then 'Não' else v end $$;

update clients c set anamnese = n.novo
from (
  select id, anamnese
    || (jsonb_strip_nulls(jsonb_build_object(
        'smoker',       pg_temp.sn(anamnese->>'FUMANTE'),
        'alcohol',      pg_temp.sn(anamnese->>'INGERE ALCOOL'),
        'water',        pg_temp.sn(anamnese->>'INGERE AGUA?'),
        'waterLiters',  case upper(anamnese->>'QUANTOS LITROS POR DIA')
                          when 'ATÉ 2LITROS OU +' then '2 litros ou mais'
                          when 'ATÉ 1 LITRO' then 'Até 1 litro' else anamnese->>'QUANTOS LITROS POR DIA' end,
        'exercise',     pg_temp.sn(anamnese->>'FAZ ATIVIDADE FISICA'),
        'sleep',        case when upper(anamnese->>'QUALIDADE DE SONO') like 'BOA%' then 'Boa'
                             when upper(anamnese->>'QUALIDADE DE SONO') like 'RUIM%' then 'Ruim'
                             else anamnese->>'QUALIDADE DE SONO' end,
        'diet',         pg_temp.sn(anamnese->>'BOA ALIMENTAÇAO'),
        'breastfeeding',pg_temp.sn(anamnese->>'AMAMENTANDO ?'),
        'braces',       pg_temp.sn(anamnese->>'USA APARELHO ODONTOLÓGICO?'),
        'lenses',       pg_temp.sn(anamnese->>'USA LENTES NOS OLHOS?'),
        'iud',          pg_temp.sn(anamnese->>'DIU?'),
        'profession',   anamnese->>'profissão',
        'complaint',    anamnese->>'principal queixas',
        'implants',     anamnese->>'POSSUI MARCA-PASSO?PINOS OU PROTESES?',
        'surgeries',    anamnese->>'JÁ FEZ ALGUMA CIRURGIA?',
        'aesthetic',    anamnese->>'POSSUI ALGUM PROCEDIMENTO ESTÉTICO NO CORPO?',
        'aestheticWhere', anamnese->>'procedimentos já realizados',
        'otherHealth',  anamnese->>'POSSUI ALGUM PROBLEMA DE SAUDE NAO CITADO AO LADO?'
      ))
      -- o que a ficha já tem tem prioridade: as chaves existentes sobrescrevem o mapeado
      || anamnese) as novo
  from clients where jsonb_typeof(anamnese)='object'
) n
where c.id=n.id and c.anamnese is distinct from n.novo;
-- Obs.: 'SIM, NÃO' (marcado os dois no formulário antigo) vira 'Sim', igual ao que a importação já fez nas 249.
-- Obs.: 'GRAVIDEZ?' não é mapeada aqui: o app usa pregnant="false" (texto); falta confirmar o valor para 'SIM'.
-- Reverter: update clients c set anamnese=b.anamnese from clients_anamnese_bkp_20261120 b where b.id=c.id;
