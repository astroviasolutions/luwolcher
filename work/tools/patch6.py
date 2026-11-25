# patch6: caixa — profissional por item + pagamento opcional por item; uma venda por profissional
p='/home/user/luwolcher/work/site/assets/index-B-Eix5hJ.js'
s=open(p,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(s.count(old),old[:100])
    s=s.replace(old,new)

HELPERS = r"""function LwStrip(i){let{apptId:a,barberId:b,...r}=i;return r}
function LwSib(e,a,c,l){return(a.appointments||[]).filter(s=>s.id!==e.id&&s.date===e.date&&[`agendado`,`confirmado`].includes(s.status)&&s.barberId!==e.barberId&&(e.clientId?s.clientId===e.clientId:s.clientName===e.clientName)).flatMap(s=>[...hT(s,c,a.packages),...eh(s,l)].map(i=>({...i,barberId:s.barberId,apptId:s.id})))}
function LwSplit(P){let{items:I,U:U,Dn:Dn,main:M,barbers:B,services:Sv,products:Pd,settings:St,Xe:Xe,Ie:Ie,Ue:Ue,Ze:Ze,ze:ze,Ve:Ve,He:He,k:k,j:j,N:N,F:F,Ke:Ke,appt:E,appts:AP}=P,R=G,eff=i=>i.barberId||M.id,
ids=[M.id,...I.map(eff)].filter((v,n,ar)=>ar.indexOf(v)===n).filter(v=>I.some(i=>eff(i)===v)||v===M.id&&U>0),
gs=ids.map(id=>{let ix=[];I.forEach((i,n)=>{eff(i)===id&&ix.push(n)});let gi=ix.map(n=>I[n]);return{id:id,ix:ix,gi:gi,sub:R(gi.reduce((t,i)=>t+i.price*i.qty,0)+(id===M.id?U:0))}}),
allot=(tot,w)=>{let sw=w.reduce((t,v)=>t+v,0),left=R(tot);return w.map((v,n)=>{let y=n===w.length-1?left:R(sw?tot*v/sw:0);left=R(left-y);return y})},
subs=gs.map(g=>g.sub),disc=allot(Ue,subs),yy=allot(Ze,subs),bn=allot(ze?Ve:0,subs),rates=[],
gr=gs.map((g,n)=>{let b=B.find(v=>v.id===g.id),q=Nr(jr(g.gi,{services:Sv,products:Pd,barber:b,materialReduces:!!Xe.materialReduces}),yy[n]);g.ix.forEach((ii,pos)=>{rates[ii]=q[pos]?.commissionRate??0});
let rt=Xe.extraMode===`none`?0:Xe.extraMode===`fixed`?Number(Xe.extraRate||0):(()=>{let sv=q.filter(i=>i.type===`service`);return sv.length?sv.reduce((t,i)=>t+Number(i.commissionRate||0),0)/sv.length:Number(b?.serviceRate??50)})(),
ex=g.id===M.id&&U>0?[{type:`extra`,refId:null,name:Dn?`Adicional: ${Dn}`:`Adicional`,price:U,qty:1,commissionRate:R(rt),commission:R(U*rt/100)}]:[],
base=[...q,...ex],tt=He?base.map(i=>({...i,commission:0})):base,Wg=R(g.sub-disc[n]),ratio=g.sub?disc[n]/g.sub:0,pm={};
if(!He)g.gi.forEach(i=>{i.pay&&!i.packageId&&i.price>0&&(pm[i.pay]=R((pm[i.pay]||0)+R(i.price*i.qty*(1-ratio))))});
let pT=R(Object.values(pm).reduce((t,v)=>t+v,0));return{g:g,n:n,b:b,tt:tt,Wg:Wg,pm:pm,gen:Math.max(0,R(Wg-pT))}}),
genT=R(gr.reduce((t,x)=>t+x.gen,0)),rT=He?0:j===``?genT:Math.min(Er(j),genT),rs=allot(rT,gr.map(x=>x.gen)),
groups=gr.map(x=>{let{g:g,n:n,tt:tt,Wg:Wg,pm:pm,gen:gen}=x,qeG=!He&&k===`credito`&&j===``&&gen>0?Zp(St,gen,F,Ke):0,qeI=!He&&pm.credito>0?Zp(St,pm.credito,F,Ke):0,qe=R(qeG+qeI),seg={},add=(p,v)=>{v>0&&(seg[p]=R((seg[p]||0)+v))};
if(!He){Object.entries(pm).forEach(([p,v])=>add(p,v+(p===`credito`?qeI:0)));if(gen>0){add(k,rs[n]+qeG);let sg=R(gen-rs[n]);sg>0&&add(N===`fiado`?`a pagar`:N,sg)}}
let ent=Object.entries(seg),total=R(Wg+qe),hasPkg=tt.some(i=>i.packageId),
payment=He?`permuta`:total===0&&hasPkg?`pacote`:ent.length===0?k:ent.length===1?ent[0][0]:ent.map(([p,v])=>`${p} ${W(v)}`).join(` + `),
fee=R(ent.reduce((t,[p,v])=>t+(Xp(p)?Yp(St,p,v,F,Ke):0),0)),
tt2=qe>0?[...tt,{type:`surcharge`,refId:null,name:`Juros do parcelamento ${F}x`,price:qe,qty:1,commissionRate:0,commission:0}]:tt,
items=Xe.feeReduces&&!He?Pr(tt2,total-qe,Math.max(0,fee-qe)):tt2,
card=ent.some(([p])=>Xp(p)),cred=ent.some(([p])=>p===`credito`);
return{barberId:g.id,main:g.id===M.id,items:items,gi:g.gi,subtotal:R(g.sub+qe),discount:disc[n],total:total,payment:payment,commissionTotal:R(items.reduce((t,i)=>t+Number(i.commission||0),0)),installments:cred?F:null,cardFee:fee,cardMachine:card?Ke:null,benefit:He?{kind:`permuta`,label:`Permuta`,amount:g.sub}:ze&&(n===0||![`club`,`runas`].includes(ze.kind))?{kind:ze.kind,label:ze.label,amount:bn[n]}:null,loyaltyRedeemed:n===0&&!He&&ze?.kind===`runas`,appointmentId:null,saldo:seg.saldo||0,fiado:seg[`a pagar`]||0}}),
used=new Set;groups.forEach(g=>{let a=g.gi.find(i=>i.apptId),id=g.main&&E?E.id:a?a.apptId:null;id&&!used.has(id)&&(used.add(id),g.appointmentId=id)});
AP.filter(v=>!used.has(v.id)).forEach(v=>{let g=groups.find(y=>!y.appointmentId&&y.barberId===v.barberId)||groups.find(y=>!y.appointmentId);g&&(g.appointmentId=v.id,used.add(v.id))});
return{groups:groups,rates:rates,total:R(groups.reduce((t,g)=>t+g.total,0)),fee:R(groups.reduce((t,g)=>t+g.cardFee,0)),saldo:R(groups.reduce((t,g)=>t+g.saldo,0)),fiado:R(groups.reduce((t,g)=>t+g.fiado,0)),leftover:AP.filter(v=>!used.has(v.id)).map(v=>v.id),pkgPay:(groups.find(g=>g.items.some(i=>i.packageId))||groups[0])?.payment||k}}
"""
rep("function oh({appointment:e,sale:t,presetBarberId:n,lockBarber:r,onDone:i}){", HELPERS+"function oh({appointment:e,sale:t,presetBarberId:n,lockBarber:r,onDone:i}){")

# siblings (agenda dividida) entram no carrinho já com a profissional de cada um
rep("...eh(e,l),...r.map(sm)]),Array.isArray(e.usage?.supplies)", "...eh(e,l),...r.map(sm),...LwSib(e,a,c,l)]),Array.isArray(e.usage?.supplies)")

# variáveis novas (antes do _t)
rep("ht=R??Km(x,c),gt=G(Ie+qe),_t=async()=>{",
 "ht=R??Km(x,c),gt=G(Ie+qe),edX=!!t,lkX=s?.role===`barber`,muX=!t&&!!xe&&x.some(i=>i.barberId&&i.barberId!==xe.id||!He&&i.pay),zrX=muX?LwSplit({items:x,U:U,Dn:D.trim(),main:xe,barbers:u,services:c,products:l,settings:a.settings,Xe:Xe,Ie:Ie,Ue:Ue,Ze:Ze,ze:ze,Ve:Ve,He:He,k:k,j:j,N:N,F:F,Ke:Ke,appt:e,appts:e?[e,...[...new Set(x.filter(i=>i.apptId).map(i=>i.apptId))].map(id=>a.appointments.find(v=>v.id===id)).filter(Boolean)]:[]}):null,_t=async()=>{")

# itens sem campos internos
rep("[...pt,...qm(ht,a.products)]","[...pt.map(LwStrip),...qm(ht,a.products)]",2)

# saldo/fiado/pacote vindos do split
rep("c=(k===`saldo`?r:0)+(s>0&&N===`saldo`?s:0),l=s>0&&N===`fiado`?s:0,u=n?at:0;",
    "c=zrX?zrX.saldo:(k===`saldo`?r:0)+(s>0&&N===`saldo`?s:0),l=zrX?zrX.fiado:s>0&&N===`fiado`?s:0,u=n?at:0;")
rep("let d=s>0?`${k} ${W(r)} + ${N===`fiado`?`a pagar`:N} ${W(s)}`:Je===0&&x.some(e=>e.packageId)?`pacote`:k;",
    "let d=zrX?zrX.pkgPay:s>0?`${k} ${W(r)} + ${N===`fiado`?`a pagar`:N} ${W(s)}`:Je===0&&x.some(e=>e.packageId)?`pacote`:k;")

# criação: uma venda por profissional
old_sale="let r=await o.createSale({date:K(),time:qn(Jn()),barberId:xe.id,clientId:t?.id||null,clientName:t?.name||B.trim()||`Cliente avulso`,appointmentId:e?.id||null,items:[...pt.map(LwStrip),...qm(ht,a.products)],subtotal:gt,discount:Ue,total:Je,payment:d,commissionTotal:mt,...ft,benefit:He?{kind:`permuta`,label:`Permuta`,amount:Ie}:ze?{kind:ze.kind,label:ze.label,amount:Ve}:null,loyaltyRedeemed:!He&&ze?.kind===`runas`});"
new_sale=("let r,rs=null;if(zrX){rs=[];let nmB=q9=>a.barbers.find(z9=>z9.id===q9)?.name?.split(` `)[0]||`profissional`;for(let g9 of zrX.groups){try{rs.push(await o.createSale({date:K(),time:qn(Jn()),barberId:g9.barberId,clientId:t?.id||null,clientName:t?.name||B.trim()||`Cliente avulso`,appointmentId:g9.appointmentId,items:[...g9.items.map(LwStrip),...g9.main?qm(ht,a.products):[]],subtotal:g9.subtotal,discount:g9.discount,total:g9.total,payment:g9.payment,commissionTotal:g9.commissionTotal,installments:g9.installments,cardFee:g9.cardFee,cardMachine:g9.cardMachine,benefit:g9.benefit,loyaltyRedeemed:g9.loyaltyRedeemed}))}catch(er9){if(rs.length){o.notify(`Já gravou a venda de ${rs.map(v9=>nmB(v9.barberId)).join(`, `)}, mas falhou a de ${nmB(g9.barberId)}: ${er9.message}. Os itens gravados saíram do carrinho; confira em Vendas e finalize o restante.`,`bad`);let dn9=new Set(rs.map(v9=>v9.barberId));S(x.filter(i9=>!dn9.has(i9.barberId||xe.id)));return}throw er9}}r=rs[0];for(let id9 of zrX.leftover)await o.updateAppointment(id9,{status:`concluido`},null).catch(()=>{})}else r="
 +old_sale[len('let r='):].replace("items:[...pt.map(LwStrip),...qm(ht,a.products)]","items:[...pt.map(LwStrip),...qm(ht,a.products)]"))
rep(old_sale,new_sale)
rep("de({sale:r,client:t,phone:t?.phone||re,","de({sale:r,sales:rs,client:t,phone:t?.phone||re,")

# linha do carrinho: comissão da profissional do item + seletores
rep("p?` · comissão ${Qe[t]?.commissionRate??0}%`:``]})","p?` · comissão ${(zrX?zrX.rates[t]:Qe[t]?.commissionRate)??0}%`:``]})")
WHO=("!edX&&(e.type===`service`||e.type===`product`)&&(0,X.jsxs)(`div`,{className:`line-who`,style:{flexBasis:`100%`,display:`flex`,gap:8,flexWrap:`wrap`,alignItems:`center`,fontSize:12},children:["
 "!lkX&&(0,X.jsxs)(`label`,{style:{display:`flex`,alignItems:`center`,gap:4},children:[`Profissional`,(0,X.jsx)(`select`,{value:e.barberId||xe?.id||``,\"aria-label\":`Profissional de ${e.name}`,onChange:ev=>{let v=ev.target.value;S(ls=>ls.map((it,ix)=>ix===t?{...it,barberId:v===xe?.id?void 0:v}:it))},children:u.filter(bb=>bb.active&&(e.type!==`service`||zr(bb,e.refId))||bb.id===(e.barberId||xe?.id)).map(bb=>(0,X.jsx)(`option`,{value:bb.id,children:bb.name},bb.id))})]}),"
 "!He&&!e.packageId&&(0,X.jsxs)(`label`,{style:{display:`flex`,alignItems:`center`,gap:4},children:[`Pagamento`,(0,X.jsxs)(`select`,{value:e.pay||``,\"aria-label\":`Pagamento de ${e.name}`,onChange:ev=>{let v=ev.target.value;S(ls=>ls.map((it,ix)=>ix===t?{...it,pay:v||void 0}:it))},children:[(0,X.jsx)(`option`,{value:``,children:`Geral (no fim)`}),ah.filter(o2=>[`pix`,`dinheiro`,`debito`,`credito`].includes(o2.value)).map(o2=>(0,X.jsx)(`option`,{value:o2.value,children:o2.label},o2.value))]})]})]}),")
rep("(0,X.jsx)(`button`,{className:`icon-btn sm`,onClick:()=>Ne(t),\"aria-label\":`Remover`,children:(0,X.jsx)(Lf,{size:16})}),n&&pe===r&&",
    "(0,X.jsx)(`button`,{className:`icon-btn sm`,onClick:()=>Ne(t),\"aria-label\":`Remover`,children:(0,X.jsx)(Lf,{size:16})}),"+WHO+"n&&pe===r&&")
# aviso agenda dividida
rep("x.length===0&&(0,X.jsx)(`p`,{className:`muted center`,children:`Toque nos serviços e produtos para adicionar.`}),",
    "x.length===0&&(0,X.jsx)(`p`,{className:`muted center`,children:`Toque nos serviços e produtos para adicionar.`}),!t&&x.some(i=>i.apptId)&&(0,X.jsx)(`p`,{className:`muted small`,children:`Atendimento dividido na agenda: os serviços das outras profissionais já vieram no carrinho, cada um com a sua. Ao finalizar sai uma venda por profissional.`}),")

# totais
rep("(0,X.jsx)(`span`,{children:`Total`}),(0,X.jsx)(`b`,{children:W(Je)})]}),p&&(0,X.jsxs)(`div`,{className:`comm`,children:[(0,X.jsxs)(`span`,{children:[`Comissão de `,xe?.name.split(` `)[0]]}),(0,X.jsx)(`b`,{children:W(mt)})]})]})",
    "(0,X.jsx)(`span`,{children:`Total`}),(0,X.jsx)(`b`,{children:W(zrX?zrX.total:Je)})]}),zrX?zrX.groups.map(g9=>(0,X.jsxs)(`div`,{className:`comm`,children:[(0,X.jsxs)(`span`,{children:[`Venda de `,a.barbers.find(z9=>z9.id===g9.barberId)?.name.split(` `)[0],` · `,W(g9.total),` · `,g9.payment.replace(/\\s?R\\$\\s?[\\d.,]+/g,m9=>m9.replace(/\\s/g,` `)),p?` · comissão `:``]}),p&&(0,X.jsx)(`b`,{children:W(g9.commissionTotal)})]},g9.barberId)):p&&(0,X.jsxs)(`div`,{className:`comm`,children:[(0,X.jsxs)(`span`,{children:[`Comissão de `,xe?.name.split(` `)[0]]}),(0,X.jsx)(`b`,{children:W(mt)})]})]})")
rep("`Finalizar · ${W(Je)}${at>0?` + dívida ${W(at)}`:``}`","`Finalizar · ${W(zrX?zrX.total:Je)}${zrX?` (${zrX.groups.length} vendas)`:``}${at>0?` + dívida ${W(at)}`:``}`")

# tela de venda finalizada
rep("(0,X.jsxs)(`h3`,{children:[`Venda finalizada · `,W(ue.sale.total)]}),p?(0,X.jsxs)(`p`,{className:`muted`,children:[`Comissão de `,xe?.name.split(` `)[0],",
    "(0,X.jsxs)(`h3`,{children:[`Venda finalizada · `,W(ue.sales?G(ue.sales.reduce((t9,v9)=>t9+Number(v9.total||0),0)):ue.sale.total)]}),ue.sales&&ue.sales.length>1?ue.sales.map(v9=>(0,X.jsxs)(`p`,{className:`muted`,children:[a.barbers.find(z9=>z9.id===v9.barberId)?.name.split(` `)[0],`: `,W(v9.total),p?` · comissão `:``,p&&(0,X.jsx)(`b`,{children:W(v9.commissionTotal)})]},v9.barberId)):p?(0,X.jsxs)(`p`,{className:`muted`,children:[`Comissão de `,xe?.name.split(` `)[0],")
rep("(0,X.jsx)(_m,{sales:[ue.sale],phone:ue.phone}),q(ue.phone).length>=10&&(0,X.jsx)(Am,{appts:ue.sale.appointmentId?[{id:ue.sale.appointmentId}]:[],client:ue.client,phone:ue.phone,serviceIds:(ue.sale.items||[]).filter(e=>e.type===`service`).map(e=>e.refId),date:ue.sale.date})",
    "(0,X.jsx)(_m,{sales:ue.sales||[ue.sale],phone:ue.phone}),q(ue.phone).length>=10&&(0,X.jsx)(Am,{appts:(ue.sales||[ue.sale]).filter(v9=>v9.appointmentId).map(v9=>({id:v9.appointmentId})),client:ue.client,phone:ue.phone,serviceIds:(ue.sales||[ue.sale]).flatMap(v9=>v9.items||[]).filter(e=>e.type===`service`).map(e=>e.refId),date:ue.sale.date})")
rep("children:L.length>1&&I?`Cobrar só este`:`Concluir e cobrar`","children:L.length>1&&I?`Cobrar no caixa (cada profissional no seu item)`:`Concluir e cobrar`")
open(p,'w',encoding='utf-8').write(s); print('ok')
