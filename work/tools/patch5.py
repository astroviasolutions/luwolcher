p='/home/user/luwolcher/work/site/assets/index-B-Eix5hJ.js'
s=open(p,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(s.count(old),old[:90])
    s=s.replace(old,new)

# 1) Ym: preço do item = base + acréscimo - desconto (desconto por unidade, nunca acima do valor do item)
rep("function Ym(e,t,n=``){let r=Number(e.basePrice??e.price),{basePrice:i,increase:a,increaseNote:o,...s}=e;return t>0?{...s,basePrice:r,increase:G(t),increaseNote:n.trim(),price:G(r+t)}:{...s,price:r}}",
    "function Ym(e,t,n=``,d=0,dn=``){let r=Number(e.basePrice??e.price),{basePrice:i,increase:a,increaseNote:o,discount:_d,discountNote:_n,...s}=e,u=t>0?t:0,v=Math.min(Math.max(0,Number(d)||0),r+u);return u>0||v>0?{...s,basePrice:r,...u>0?{increase:G(u),increaseNote:n.trim()}:{},...v>0?{discount:G(v),discountNote:String(dn||``).trim()}:{},price:G(r+u-v)}:{...s,price:r}}")

# 2) botão da linha: mostra acréscimo e/ou desconto
rep("function Zm({item:e,open:t,onToggle:n}){let r=Number(e.increase)>0;return(0,X.jsxs)(`button`,{type:`button`,className:`inc-btn${r?` on`:``}${t?` open`:``}`,onClick:n,\"aria-expanded\":t,title:`Aumentar o valor deste item`,\"aria-label\":`Aumentar o valor de ${e.name}`,children:[(0,X.jsx)(zf,{size:14}),r&&(0,X.jsxs)(`span`,{children:[`+`,W(Number(e.increase)*Number(e.qty||1))]})]})}",
    "function Zm({item:e,open:t,onToggle:n}){let r=Number(e.increase)>0,q2=Number(e.discount)>0;return(0,X.jsxs)(`button`,{type:`button`,className:`inc-btn${r||q2?` on`:``}${t?` open`:``}`,onClick:n,\"aria-expanded\":t,title:`Dar desconto ou aumentar o valor deste item`,\"aria-label\":`Desconto ou acréscimo em ${e.name}`,children:[(0,X.jsx)(zf,{size:14}),r&&(0,X.jsxs)(`span`,{children:[`+`,W(Number(e.increase)*Number(e.qty||1))]}),q2&&(0,X.jsxs)(`span`,{children:[`−`,W(Number(e.discount)*Number(e.qty||1))]})]})}")

# 3) painel: campo de desconto (R$ ou %) por unidade
rep("function Qm({item:e,onApply:t,onClose:n}){let[r,i]=(0,d.useState)(Number(e.increase)>0?String(e.increase).replace(`.`,`,`):``),[a,o]=(0,d.useState)(e.increaseNote||``),s=Er(r),c=Number(e.basePrice??e.price),l=Number(e.qty||1);",
    "function Qm({item:e,onApply:t,onClose:n}){let[r,i]=(0,d.useState)(Number(e.increase)>0?String(e.increase).replace(`.`,`,`):``),[a,o]=(0,d.useState)(e.increaseNote||``),[dr,di]=(0,d.useState)(Number(e.discount)>0?String(e.discount).replace(`.`,`,`):``),[dn,dno]=(0,d.useState)(e.discountNote||``),s=Er(r),c=Number(e.basePrice??e.price),l=Number(e.qty||1),dt=String(dr).trim(),ds=Math.min(dt.endsWith(`%`)?G((c+s)*Math.min(100,Math.max(0,Er(dt.slice(0,-1))))/100):Er(dt),c+s);")
rep("(0,X.jsxs)(`small`,{className:`muted`,children:[W(c),s>0?` + ${W(s)} = ${W(c+s)}`:``,l>1?` × ${l}`:``]}),(0,X.jsxs)(`div`,{className:`inc-edit-row`,children:[(0,X.jsx)(Q,{size:`sm`,onClick:()=>{t(Ym(e,s,a)),n()},children:s>0?`Aplicar acréscimo`:`Sem acréscimo`}),Number(e.increase)>0&&(0,X.jsx)(`button`,{type:`button`,className:`link`,onClick:()=>{t(Ym(e,0)),n()},children:`tirar acréscimo`}),",
    "(0,X.jsxs)(`div`,{className:`inc-edit-row`,children:[(0,X.jsxs)(`label`,{children:[(0,X.jsxs)(`span`,{children:[`Desconto`,l>1?` (por unidade)`:``,` R$ ou %`]}),(0,X.jsx)(`input`,{inputMode:`decimal`,value:dr,onChange:e=>di(e.target.value.replace(/[^\\d,.%]/g,``)),placeholder:`Ex.: 17 ou 20%`,\"aria-label\":`Desconto em ${e.name}`})]}),(0,X.jsxs)(`label`,{className:`grow`,children:[(0,X.jsx)(`span`,{children:`Motivo do desconto`}),(0,X.jsx)(`input`,{value:dn,onChange:e=>dno(e.target.value),placeholder:`Ex.: aniversário, cortesia, combinado`,maxLength:80})]})]}),(0,X.jsxs)(`small`,{className:`muted`,children:[W(c),s>0?` + ${W(s)}`:``,ds>0?` − ${W(ds)}`:``,s>0||ds>0?` = ${W(c+s-ds)}`:``,l>1?` × ${l}`:``,ds>0?` · a comissão é calculada sobre o valor com desconto`:``]}),(0,X.jsxs)(`div`,{className:`inc-edit-row`,children:[(0,X.jsx)(Q,{size:`sm`,onClick:()=>{t(Ym(e,s,a,ds,dn)),n()},children:s>0||ds>0?`Aplicar`:`Sem ajuste`}),Number(e.increase)>0&&(0,X.jsx)(`button`,{type:`button`,className:`link`,onClick:()=>{t(Ym(e,0,``,Number(e.discount||0),e.discountNote||``)),n()},children:`tirar acréscimo`}),Number(e.discount)>0&&(0,X.jsx)(`button`,{type:`button`,className:`link`,onClick:()=>{t(Ym(e,Number(e.increase||0),e.increaseNote||``,0)),n()},children:`tirar desconto`}),")

# 4) texto da linha do carrinho
rep("Number(e.increase)>0?`${W(e.basePrice)} + ${W(e.increase)} acréscimo`:W(e.price),p?` · comissão ${Qe[t]?.commissionRate??0}%`:``]}),Number(e.increase)>0&&e.increaseNote&&(0,X.jsxs)(`small`,{className:`inc-note`,children:[`Acréscimo: `,e.increaseNote]}),",
    "Number(e.increase)>0||Number(e.discount)>0?`${W(e.basePrice)}${Number(e.increase)>0?` + ${W(e.increase)} acréscimo`:``}${Number(e.discount)>0?` − ${W(e.discount)} desconto`:``}`:W(e.price),p?` · comissão ${Qe[t]?.commissionRate??0}%`:``]}),Number(e.increase)>0&&e.increaseNote&&(0,X.jsxs)(`small`,{className:`inc-note`,children:[`Acréscimo: `,e.increaseNote]}),Number(e.discount)>0&&e.discountNote&&(0,X.jsxs)(`small`,{className:`inc-note`,children:[`Desconto: `,e.discountNote]}),")

# 5) detalhe da venda já lançada (comanda)
rep("Number(r.increase)>0&&(0,X.jsxs)(`small`,{className:`inc-note`,children:[W(r.basePrice),` + `,W(r.increase),` acréscimo`,r.increaseNote?` · ${r.increaseNote}`:``]})",
    "Number(r.increase)>0&&(0,X.jsxs)(`small`,{className:`inc-note`,children:[W(r.basePrice),` + `,W(r.increase),` acréscimo`,r.increaseNote?` · ${r.increaseNote}`:``]}),Number(r.discount)>0&&(0,X.jsxs)(`small`,{className:`inc-note`,children:[W(r.basePrice),` − `,W(r.discount),` desconto`,r.discountNote?` · ${r.discountNote}`:``]})")
open(p,'w',encoding='utf-8').write(s); print('ok')
