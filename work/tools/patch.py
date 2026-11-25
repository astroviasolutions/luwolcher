import sys
p='/home/user/luwolcher/work/site/assets/index-B-Eix5hJ.js'
s=open(p,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(s.count(old),old[:60])
    s=s.replace(old,new)
# P2: bloqueia agendar cliente sem WhatsApp + mensagem inline
rep("nt=(o?f.name:Ee||(f.name||De)&&q(f.phone).length>=10)&&fe.length>0",
    "zapX=!o&&Ee&&(e=>!e||q(e.phone).length<10&&!e.phoneLast4)(s.clients.find(e=>e.id===f.clientId))&&q(f.phone).length<10,nt=!zapX&&(o?f.name:Ee||(f.name||De)&&q(f.phone).length>=10)&&fe.length>0")
rep("!nt&&Ye&&(0,X.jsx)(`p`,{className:`form-err mb-sm`,style:{width:`100%`},children:Ye})",
    "!nt&&(zapX||Ye)&&(0,X.jsx)(`p`,{className:`form-err mb-sm`,style:{width:`100%`},role:`alert`,children:zapX?`Essa cliente está sem WhatsApp no cadastro. Toque em \"Adicionar WhatsApp\" na ficha acima, informe o número com DDD e agende de novo.`:Ye})")
open(p,'w',encoding='utf-8').write(s)
print('ok')
