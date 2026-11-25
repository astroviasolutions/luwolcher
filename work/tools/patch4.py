p='/home/user/luwolcher/work/site/assets/index-B-Eix5hJ.js'
s=open(p,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(s.count(old),old[:80])
    s=s.replace(old,new)
# 1) modal aceita lock: clique fora não fecha
rep("function ip({open:e,onClose:t,title:n,children:r,footer:i,wide:a}){","function ip({open:e,onClose:t,title:n,children:r,footer:i,wide:a,lock:L}){")
rep("onMouseDown:e=>e.target===e.currentTarget&&t?.(),children:(0,X.jsxs)(`div`,{className:_r(`modal`,a&&`modal-wide`,o&&`v-from`)",
    "onMouseDown:e=>!L&&e.target===e.currentTarget&&t?.(),children:(0,X.jsxs)(`div`,{className:_r(`modal`,a&&`modal-wide`,o&&`v-from`)")
# 2) extrai a função de salvar e usa nos dois botões
a="onClick:async()=>{if(!c.name.trim())return i.notify(`Informe o nome da paciente`,`bad`);"
i0=s.index(a); assert s.count(a)==1
end_marker="finally{m(!1)}},children:p?`Salvando…`:u?"
i1=s.index(end_marker,i0)
body=s[i0+len("onClick:"):i1+len("finally{m(!1)}}")]   # async()=>{...}
s=s[:i0]+"onClick:sv"+s[i1+len("finally{m(!1)}}"):]
rep("return h?(0,X.jsx)(ip,{open:!0,onClose:t,title:`Termo assinado`","let sv="+body+";return h?(0,X.jsx)(ip,{open:!0,onClose:t,title:`Termo assinado`")
# 3) modal do termo: lock + botão de salvar também dentro do corpo, logo abaixo da assinatura
rep("(0,X.jsxs)(ip,{open:!0,wide:!0,onClose:t,title:`Termo de consentimento · ${e.name}`","(0,X.jsxs)(ip,{open:!0,wide:!0,lock:!0,onClose:t,title:`Termo de consentimento · ${e.name}`")
rep("(0,X.jsx)(Ow,{onChange:f}),(0,X.jsx)(`p`,{className:`muted small mt-sm`,children:`Ao assinar,",
    "(0,X.jsx)(Ow,{onChange:f}),(0,X.jsx)(Q,{block:!0,className:`mt-sm`,icon:Pd,disabled:p,onClick:sv,children:p?`Salvando…`:u?`Salvar termo assinado`:`Salvar (falta assinar)`}),(0,X.jsx)(`p`,{className:`muted small mt-sm`,children:`Ao assinar,")
open(p,'w',encoding='utf-8').write(s); print('ok')
