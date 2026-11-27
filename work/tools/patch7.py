# patch7: comissões — detalhe mostra Valor, Desconto, Valor cobrado; mensagem do fechamento mostra cobrado/descontos
p='/home/user/luwolcher/work/site/assets/Comissoes-CLwZ0Y2d.js'
s=open(p,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(s.count(old),old[:80]); s=s.replace(old,new)
rep("base:(()=>{let o=t.packageId?Number(t.unit||0)*Number(t.qty):Number(t.price)*Number(t.qty),r=Number(t.commissionRate||0),c=Number(t.commission||0);return r>0&&c>0?Math.round(c*1e4/r)/100:o})(),rate:",
 "...(()=>{let q=Number(t.qty||1),pk=!!t.packageId,own=pk?Number(t.unit||0)*q:Number(t.price)*q,full=pk?own:own+Number(t.discount||0)*q,tot=(e.items||[]).filter(i=>[`service`,`product`,`extra`].includes(i.type)&&!i.packageId).reduce((a,i)=>a+Number(i.price)*Number(i.qty||1),0),sd=pk||!tot?0:Math.min(own,Number(e.discount||0)*own/tot),fin=Math.round((own-sd)*100)/100;return{full:Math.round(full*100)/100,base:fin,disc:Math.round((full-fin)*100)/100}})(),rate:")
rep("(0,A.jsx)(`th`,{className:`r`,children:`Base`})",
 "(0,A.jsx)(`th`,{className:`r`,children:`Valor`}),(0,A.jsx)(`th`,{className:`r`,children:`Desconto`}),(0,A.jsx)(`th`,{className:`r`,children:`Valor cobrado`})")
rep("(0,A.jsx)(`td`,{className:`r`,children:E(e.base)})",
 "(0,A.jsx)(`td`,{className:`r`,children:E(e.full)}),(0,A.jsx)(`td`,{className:`r`,children:e.disc>0?`−${E(e.disc)}`:`—`}),(0,A.jsx)(`td`,{className:`r`,children:(0,A.jsx)(`b`,{children:E(e.base)})})")
# mensagem do fechamento
rep("detalhes:`✨ Serviços:","detalhes:`🧾 Cobrado das clientes: ${E(n.revenue)}${(q=>q>0?` (descontos de ${E(q)})`:``)(e.sales.filter(v=>v.barberId===n.barber.id&&v.date>=T.from&&v.date<=T.to).reduce((a,v)=>a+Number(v.discount||0),0))}\\n✨ Serviços:")
open(p,'w',encoding='utf-8').write(s); print('ok')
