p='/home/user/luwolcher/work/site/assets/index-B-Eix5hJ.js'
s=open(p,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(s.count(old),old[:70])
    s=s.replace(old,new)
# 1) canvas: (re)inicializa no 1º toque se a largura veio 0 (modal animando / Firefox) e usa fallback de tamanho
rep("s=e=>{e.preventDefault(),t.current.setPointerCapture?.(e.pointerId),n.current=!0,r.current=o(e);",
    "s=e=>{e.preventDefault();let z=t.current;if(!z.width||!z.height){let k=window.devicePixelRatio||1;z.width=(z.offsetWidth||300)*k;z.height=(z.offsetHeight||180)*k;let c=z.getContext(`2d`);c.scale(k,k);c.lineWidth=2.4;c.lineCap=`round`;c.lineJoin=`round`;c.strokeStyle=`#1B2A63`}try{z.setPointerCapture?.(e.pointerId)}catch{}n.current=!0,r.current=o(e);")
# 2) botão salvar sempre clicável (só desabilita enquanto salva); sem assinatura mostra o aviso na tela
rep("(0,X.jsx)(Q,{style:{flex:1},icon:Pd,disabled:p||!u,onClick:async()=>{if(!c.name.trim())return i.notify(`Informe o nome da paciente`,`bad`);if(!u)return i.notify(`A paciente precisa assinar no quadro`,`bad`);m(!0);",
    "(0,X.jsx)(Q,{style:{flex:1},icon:Pd,disabled:p,onClick:async()=>{if(!c.name.trim())return i.notify(`Informe o nome da paciente`,`bad`);if(!u)return i.notify(`A paciente precisa assinar no quadro antes de salvar`,`bad`);m(!0);")
# 3) rótulo mais claro
rep("children:p?`Salvando…`:`Assinar e salvar`})]}),children:[(0,X.jsxs)(`div`,{className:`form-grid`,children:[(0,X.jsx)($,{label:`Paciente`",
    "children:p?`Salvando…`:u?`Salvar termo assinado`:`Salvar (falta assinar)`})]}),children:[(0,X.jsxs)(`div`,{className:`form-grid`,children:[(0,X.jsx)($,{label:`Paciente`")
open(p,'w',encoding='utf-8').write(s)
c='/home/user/luwolcher/work/site/assets/index-9FCotthv.css'
t=open(c,encoding='utf-8').read()
t+="\n/* ajuste: rodapé do modal (botão Salvar) nunca é espremido nem some em telas baixas / Firefox antigo */\n.modal-foot{flex-shrink:0;background:var(--surface,inherit)}\n.modal-body{min-height:0;flex:1 1 auto}\n"
open(c,'w',encoding='utf-8').write(t)
print('ok')
