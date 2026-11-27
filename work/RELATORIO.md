# Lu Wolcher — correções (cópia de trabalho, NADA publicado, NADA alterado no banco)
Base: backup de 20/11/2026. Cópia corrigida: work/site (só index-B-Eix5hJ.js, index-9FCotthv.css e 3 imagens mudam).

1) Logo — criados com os nomes exatos que o JS pede: assets/mark-CaUFCnYV.png (azul, fundo transparente),
   mark-light-LLRPwY3v.png (branca), icon-fDp8y_3X.jpg. Base: icon-512.png do site. Sem alterar JS.
   Pendente: banner-BiWX_T0e.jpg (fundo do topo da página pública) — não existe arquivo-fonte; precisa da foto original.
2) Agendamento — modal "Novo agendamento": cliente sem WhatsApp (sem telefone e sem últimos 4 dígitos) trava o botão
   Agendar e mostra aviso fixo dentro do modal. Ao salvar o WhatsApp pela ficha ("Adicionar WhatsApp"), libera.
   Cliente nova (digitada) já exigia WhatsApp com 10+ dígitos.
3) Termo — botão agora sempre aparece clicável ("Salvar (falta assinar)" -> "Salvar termo assinado"), avisa na tela se faltar
   assinatura; quadro de assinatura se inicializa no 1º toque se nasceu com largura 0; rodapé do modal não encolhe.
   NÃO reproduzido (sem Firefox 115 aqui): é correção defensiva; testar no aparelho do vídeo.
4) Fichas — 307 com chaves antigas; 249 já têm as novas espelhadas; 54 só antigas. sql/04_fichas_formato_antigo.sql
   acrescenta só as chaves novas que faltam (backup + reversão incluídos). Não aplicado.

5) (21/11) Termo "não salva / precisa sair e entrar": logs do Supabase mostram 0 uploads recusados pelo servidor; todos os PDFs têm 3,1–3,4 MB
   (jsPDF sem compressão + assinatura PNG) e há rajadas de 401 ao voltar do 2º plano (token vencido).
   Correção: PDF comprimido (teste: 2,1 MB -> 39 KB), renovação da sessão antes do upload e até 3 tentativas em falha de rede/token.

6) (21/11) v3: botão "Salvar termo assinado" também dentro do corpo do termo, logo abaixo da assinatura (rodapé do modal ficava
   fora da tela em janelas baixas no Windows/Chrome); clique fora do modal do termo não fecha mais (perdia a assinatura).

7) (22/11) v4: causa real do termo "desenquadrado" e do clique-fora que fechava tudo: o termo abre DENTRO do modal da ficha; a animação
   "both" do modal da ficha (tema v2) mantinha transform ativo e fazia o termo posicionar-se pela caixa da ficha (e não pela tela);
   o clique "fora" caía no fundo da ficha e fechava tudo. Correção só em CSS (animation-fill-mode:backwards).
   Testado em navegador com Supabase simulado: termo cobre a tela (0,0,740x800), clique fora não fecha, salvar gera PDF de ~113 KB.

8) (25/11) v5: Caixa — desconto por item (serviço/produto), ao lado do acréscimo que já existia (botão ↗ da linha): campo "Desconto R$ ou %"
   + motivo. O preço do item passa a ser base + acréscimo − desconto, e a comissão já sai sobre esse valor (testado: 85 −20% = 68; comissão 60% = R$ 40,80).
   Aparece também no detalhe da venda. NÃO feito ainda: profissional por item no caixa (exige dividir a venda por profissional; ver proposta).

9) (25/11) v7: Caixa — profissional por item e pagamento opcional por item (tools/patch6.py; teste: tools/h10.js).
   - Cada serviço/produto do carrinho tem seletor "Profissional" (só quem faz o serviço; oculto para perfil barber) e "Pagamento" (Geral/Pix/Dinheiro/Débito/Crédito).
   - Agenda dividida: ao abrir "Cobrar no caixa" (antes "Cobrar só este"), os agendamentos irmãos (mesma cliente, mesmo dia, outra profissional, status agendado/confirmado — mesma regra das Comandas; não há id de grupo) entram no carrinho já com a profissional de cada um.
   - Finalizar gera UMA venda por profissional. Desconto geral (manual/benefício) repartido proporcional ao valor de cada profissional; adicional fica com a profissional da venda; insumos na venda principal.
   - Comissão sempre sobre o valor pago (desconto por item + parcela do desconto geral), com as taxas da própria profissional.
   - Pagamento por item sem escolha segue o geral. Venda com formas mistas grava "dinheiro R$ 42,30 + credito R$ 76,50"; juros/taxa de cartão calculados por forma. Saldo/fiado/permuta/pacote e dívida da cliente só no geral, aplicados UMA vez.
   - Sem divisão e sem pagamento por item: caminho antigo, idêntico.
   Testado (Supabase simulado): 2 profissionais, sem desconto (85/47, comissão 51/37,60), desconto 10% (76,50/42,30), pagamento misto, tudo na mesma profissional.
   Riscos: fidelidade/clube contam por venda (benefício clube/runas só na 1ª venda; visita de agendamento dividido conta mais de 1 — já ocorria no "Fechar comanda"); falha na 2ª venda deixa a 1ª gravada (o app avisa e tira os itens já gravados do carrinho); agendamento irmão cujos itens forem todos trocados de profissional é marcado concluído por atualização direta. NÃO testado com Supabase real, nem em edição de venda (edição segue com 1 profissional).

10) (27/11) v8: Comissões — detalhe da profissional agora mostra Valor, Desconto e Valor cobrado por item (desconto do item + parte do desconto geral da venda), seguido de % e Comissão (tools/patch7.py, teste tools/h11.js: 100 − 20 = 80, 60% = 48). Mensagem de fechamento (WhatsApp) ganhou a linha "Cobrado das clientes … (descontos de …)". Obs.: a linha-resumo da profissional (Serviços "1 · R$ 100,00") ainda soma o valor cheio.
