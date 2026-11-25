# Lu Wolcher — resumo para continuar em chat novo (25/11/2026)

## Contexto fixo
- Site: https://luwolcher.pages.dev (Cloudflare Pages, projeto `luwolcher`, conta bff389a3d579bdfc85852f3783ad5c22, produção = branch `main`, upload direto sem Git).
- Supabase: projeto xdvnoxliymhtayvsljlj (sa-east-1). Fonte original PERDIDA: edita-se o JS minificado em `work/site/assets/` com scripts de substituição exata (`work/tools/patch*.py`).
- Repo: astroviasolutions/luwolcher, branch claude/upbeat-dirac-1koty0. Drive: pasta "Lu Wolcher" (id 1UnxSn_BtOKnLLz_u_ioMVmJP58QKorfy) com backups e zips v1..v6.
- Regras do Christian: nada publicado/alterado no banco sem OK; só cópia; não apagar dados; honesto sobre riscos; PT-BR direto.
- Publicar por aqui NÃO funciona (proxy sobrescreve o token do upload de arquivos novos do Pages): subida é MANUAL pelo painel (zip direto, branch main). Anotar o deploy ativo antes (rollback).
- Token da Cloudflare foi colado no chat: apagar em Meu perfil > Tokens de API (expira 29/11).

## Já feito (em work/site; ver RELATORIO.md)
1 logo (mark/mark-light/icon) · 2 agendamento bloqueia cliente sem WhatsApp · 3 termo: botão sob a assinatura, PDF comprimido (3,4 MB→~100 KB),
renova sessão/retenta upload, modal não fecha ao clicar fora, CSS corrige modal aninhado · 4 migração das 54 fichas em `work/sql/04_fichas_formato_antigo.sql` (NÃO aplicada)
· 5 caixa: desconto por item (R$ ou %) com comissão sobre o valor com desconto · 6 relatório de comissões: coluna Base mostra o valor pago (85 com 20% => 68).
Produção em 25/11: conferir qual deploy está ativo (a v4 pode não ter sido a subida).

## Pedido aprovado, AINDA NÃO FEITO: profissional por item no caixa
- Cada item do carrinho com sua profissional (padrão = profissional da venda; só listar quem faz o serviço). Agendamentos já divididos por profissional
  na agenda ("Quem faz cada serviço") devem chegar ao caixa já com a profissional de cada item (investigar como ligar os agendamentos irmãos: não há id de grupo).
- Ao finalizar: gerar UMA VENDA POR PROFISSIONAL (relatórios/comissões/metas continuam iguais). Desconto geral repartido proporcional ao valor de cada profissional.
- Pagamento: opcional por item (Pix/Dinheiro/Débito/Crédito); sem escolha, segue o pagamento geral no fim como hoje. Saldo/fiado/permuta/pacote só no geral (v1).
- Pontos de atenção no código (index-B-Eix5hJ.js): finalizar do caixa (createSale ~off 638243), `Vr`/`jr`/`Ar` (comissão), editSale, crédito/fiado do cliente aplicado UMA vez, taxa de cartão (`ft`).
- Testar com o harness `work/tools/h8.js` (Playwright + Supabase simulado) antes de entregar.
