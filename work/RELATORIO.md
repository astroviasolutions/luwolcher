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
