const {chromium}=require('playwright');
const b64=o=>Buffer.from(JSON.stringify(o)).toString('base64url');
const uid='11111111-1111-1111-1111-111111111111';
const jwt=b64({alg:'HS256',typ:'JWT'})+'.'+b64({sub:uid,role:'authenticated',aud:'authenticated',exp:Math.floor(Date.now()/1000)+36000,email:'t@t.com'})+'.sig';
const sess={access_token:jwt,refresh_token:'r',expires_in:36000,expires_at:Math.floor(Date.now()/1000)+36000,token_type:'bearer',user:{id:uid,aud:'authenticated',role:'authenticated',email:'t@t.com',app_metadata:{},user_metadata:{}}};
const client={id:'c1',name:'Mariana Teste',phone:'41999990000',birthday:null,anamnese:{},created_at:new Date().toISOString(),updated_at:new Date().toISOString()};
(async()=>{
 const b=await chromium.launch(); const ctx=await b.newContext({viewport:{width:740,height:800}}); const p=await ctx.newPage();
 const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push('console: '+m.text().slice(0,150))});
 await ctx.addInitScript(([k,v])=>localStorage.setItem(k,v),['sb-xdvnoxliymhtayvsljlj-auth-token',JSON.stringify(sess)]);

 const today=new Date().toISOString().slice(0,10); const calls=[];
 const appts=[{id:'a1',date:today,time:'10:00',duration:60,barber_id:'b1',service_ids:['sv1'],client_id:'c1',client_name:'Mariana Teste',client_phone:'41999990000',total:85,status:'agendado',notes:'',source:'balcao',created_at:new Date().toISOString()},
              {id:'a2',date:today,time:'11:00',duration:45,barber_id:'b2',service_ids:['sv2'],client_id:'c1',client_name:'Mariana Teste',client_phone:'41999990000',total:47,status:'agendado',notes:'',source:'balcao',created_at:new Date().toISOString()}];
 await p.route(/supabase\.co/,async r=>{
  const u=r.request().url(), m=r.request().method(), h={'access-control-allow-origin':'*','access-control-allow-headers':'*','access-control-allow-methods':'*','content-type':'application/json'};
  if(m==='OPTIONS') return r.fulfill({status:200,headers:h,body:''});
  const single=/vnd.pgrst.object/.test(r.request().headers()['accept']||'');
  if(u.includes('/auth/v1/user')) return r.fulfill({status:200,headers:h,body:JSON.stringify(sess.user)});
  if(u.includes('/rest/v1/rpc/create_sale')){calls.push(JSON.parse(r.request().postData()));return r.fulfill({status:200,headers:h,body:JSON.stringify('sale-'+calls.length)});}
  if(u.includes('/rest/v1/staff')){const row={id:'s1',user_id:uid,role:'admin',name:'Teste',barber_id:null,email:'t@t.com'};return r.fulfill({status:200,headers:h,body:JSON.stringify(single?row:[row])});}
  if(u.includes('/rest/v1/settings')) return r.fulfill({status:200,headers:h,body:JSON.stringify(single?{}:[{}])});
  if(u.includes('/rest/v1/services')) return r.fulfill({status:200,headers:h,body:JSON.stringify([{id:'sv1',name:'Escova cabelo longo',price:85,commission:60,duration:60,active:true,online:true,order:1,category:'Cabelo'},{id:'sv2',name:'Pedicure',price:47,commission:80,duration:45,active:true,online:true,order:2,category:'Unhas'}])});
  if(u.includes('/rest/v1/barbers')) return r.fulfill({status:200,headers:h,body:JSON.stringify([{id:'b1',name:'Luciane Wolcher',active:true,sort:1},{id:'b2',name:'Ana Souza',active:true,sort:2}])});
  if(u.includes('/rest/v1/clients')) return r.fulfill({status:200,headers:h,body:JSON.stringify([client])});
  if(u.includes('/rest/v1/appointments')&&m==='GET') return r.fulfill({status:200,headers:h,body:JSON.stringify(appts)});
  if(u.includes('/rest/v1/rpc/server_now')) return r.fulfill({status:200,headers:h,body:JSON.stringify(new Date().toISOString())});
  if(u.includes('/rest/v1/')) return r.fulfill({status:200,headers:h,body:single?'null':'[]'});
  return r.fulfill({status:200,headers:h,body:'{}'});
 });
 await p.goto('http://localhost:8766/#/painel',{waitUntil:'networkidle'}); await p.waitForTimeout(2500);
 await p.goto('http://localhost:8766/#/painel/caixa'); await p.waitForTimeout(2500);
 const body=async()=>(await p.innerText('body')).replace(/\n+/g,' | ');
 console.log('para cobrar:',(await body()).match(/Atendimentos de hoje[^|]*\|[^|]*\|[^|]*\|[^|]*/)?.[0]);
 await p.getByText(/Escova cabelo longo · Luciane/).first().click(); await p.waitForTimeout(1200);
 await p.getByRole('button',{name:/Cobrar no caixa/}).click(); await p.waitForTimeout(1200);
 console.log('BTNS:',await p.locator('button').allInnerTexts().then(a=>a.filter(x=>/cobr|finaliz|fechar|concl/i.test(x))));
 console.log('LINHAS:',(await p.locator('.modal-body .cart-lines').innerText()).replace(/\n+/g,' | '));
 console.log('selects:',await p.locator('.modal-body .line-who select').evaluateAll(es=>es.map(e=>e.getAttribute('aria-label')+'='+e.value)));
 const step=process.env.STEP||'1';
 if(step>='2'){ await p.getByLabel(/Pagamento de Pedicure/).selectOption('pix'); }
 if(step>='3'){ await p.locator('.modal-body .totals .disc input').nth(1).fill('10%'); }
 if(step>='4'){ await p.getByLabel(/Pagamento de Pedicure/).selectOption('dinheiro'); await p.locator('.modal-body .pay-btn').filter({hasText:'Crédito'}).click(); }
 if(step==='5'){ await p.getByLabel(/Profissional de Pedicure/).selectOption('b1'); }
 await p.waitForTimeout(500);
 const all=await body(); const k=all.indexOf('Subtotal'); console.log('TOTAIS:',all.slice(k,k+520));
 console.log('BOTAO:',await p.locator('.modal-body').getByRole('button',{name:/Finalizar/}).innerText());
 await p.screenshot({path:process.env.S+'/h10.png',fullPage:true});
 if(process.env.GO){ await p.locator('.modal-body').getByRole('button',{name:/Finalizar/}).click(); await p.waitForTimeout(1500);
  console.log('CALLS:',JSON.stringify(calls.map(c=>{const s=c.p_sale||c; return {barber:s.barber_id,appt:s.appointment_id,total:s.total,sub:s.subtotal,disc:s.discount,pay:s.payment,comm:s.commission_total,fee:s.card_fee,items:(s.items||[]).map(i=>i.name+':'+i.price+':'+i.commission)}}),null,1));
  console.log('FIM:',(await body()).slice(0,300)); }
 console.log('ERRS',errs.slice(0,5));
 await b.close();})();
