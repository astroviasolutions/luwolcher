# patch8: valor cobrado (com desconto) no resumo, no extrato PDF e no "Meu extrato"
base='/home/user/luwolcher/work/site/assets/'
def patch(fn, pairs):
    p=base+fn; s=open(p,encoding='utf-8').read()
    for old,new in pairs:
        assert s.count(old)==1,(fn,s.count(old),old[:80]); s=s.replace(old,new)
    open(p,'w',encoding='utf-8').write(s)

# valor cobrado de um item: preço*qtd menos a parte do desconto geral da venda
NET="((q,i)=>{let w=Number(i.price)*Number(i.qty||1),T=(q.items||[]).filter(x=>[`service`,`product`,`extra`].includes(x.type)&&!x.packageId).reduce((a,x)=>a+Number(x.price)*Number(x.qty||1),0);return i.packageId||!T?w:w-Math.min(w,Number(q.discount||0)*w/T)})"

# A) resumo por profissional (Ir)
patch('index-B-Eix5hJ.js',[(
 "u=[...s,...c].reduce((e,t)=>e+t.price*t.qty,0),d=l.reduce((e,t)=>e+t.price*t.qty,0),",
 "nf="+NET+",u=G(a.reduce((z,q)=>z+q.items.filter(i=>i.type===`service`||i.type===`extra`).reduce((y,i)=>y+nf(q,i),0),0)),d=G(a.reduce((z,q)=>z+q.items.filter(i=>i.type===`product`).reduce((y,i)=>y+nf(q,i),0),0)),")])

# B) extrato PDF
patch('Relatorios-B-RrQ0M5.js',[
 ("let d=s.flatMap(e=>e.items.map((t,n)=>[n===0?w(e.date):``,n===0?e.clientName||`-`:``,`${t.qty>1?`${t.qty}x `:``}${t.name}`,D(t.price*t.qty),`${t.commissionRate??`-`}%`,D(t.commission)]));l=$(a,l,[`Data`,`Cliente`,`Item`,`Valor`,`%`,`Comissão`],d.length?d:[[``,`Sem lançamentos no período`,``,``,``,``]],{styles:{fontSize:8.5,cellPadding:1.9,textColor:St},columnStyles:{0:{cellWidth:15},3:{halign:`right`},4:{halign:`center`,cellWidth:14},5:{halign:`right`}},foot:[[``,``,`Total`,D(o.svcValue+o.prdValue),``,D(o.total)]],",
  "let nf="+NET+",tv=0,td=0,d=s.flatMap(e=>e.items.filter(t=>t.type!==`supply`).map((t,n)=>{let full=t.packageId?Number(t.unit||0)*Number(t.qty||1):Number(t.price)*Number(t.qty||1)+Number(t.discount||0)*Number(t.qty||1),net=t.packageId?full:nf(e,t),ds=Math.max(0,full-net);tv+=full;td+=ds;return[n===0?w(e.date):``,n===0?e.clientName||`-`:``,`${t.qty>1?`${t.qty}x `:``}${t.name}`,D(full),ds>.004?`-${D(ds)}`:`-`,D(net),`${t.commissionRate??`-`}%`,D(t.commission)]}));l=$(a,l,[`Data`,`Cliente`,`Item`,`Valor`,`Desconto`,`Cobrado`,`%`,`Comissão`],d.length?d:[[``,`Sem lançamentos no período`,``,``,``,``,``,``]],{styles:{fontSize:8,cellPadding:1.8,textColor:St},columnStyles:{0:{cellWidth:14},3:{halign:`right`},4:{halign:`right`},5:{halign:`right`},6:{halign:`center`,cellWidth:11},7:{halign:`right`}},foot:[[``,``,`Total`,D(tv),td>.004?`-${D(td)}`:`-`,D(o.svcValue+o.prdValue),``,D(o.total)]],")])

# C) Meu extrato da profissional
patch('Barber-C6Y2-MK1.js',[(
 "(0,R.jsxs)(`small`,{children:[e.items.map(e=>e.name).join(`, `),` · `,M(e.total)]})",
 "(0,R.jsxs)(`small`,{children:[e.items.filter(e=>e.type!==`supply`).map(e=>e.name).join(`, `),` · `,Number(e.discount)>0?`${M(e.subtotal)} − desconto ${M(e.discount)} = `:``,`cobrado `,M(e.total)]})")])
print('ok')
