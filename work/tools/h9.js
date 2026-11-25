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
 await p.route(/supabase\.co/,async r=>{
  const u=r.request().url(), m=r.request().method(), h={'access-control-allow-origin':'*','access-control-allow-headers':'*','access-control-allow-methods':'*','content-type':'application/json'};
  if(m==='OPTIONS') return r.fulfill({status:200,headers:h,body:''});
  const single=/vnd.pgrst.object/.test(r.request().headers()['accept']||'');
  if(u.includes('/auth/v1/user')) return r.fulfill({status:200,headers:h,body:JSON.stringify(sess.user)});
  if(u.includes('/rest/v1/staff')){const row={id:'s1',user_id:uid,role:'admin',name:'Teste',barber_id:null,email:'t@t.com'};return r.fulfill({status:200,headers:h,body:JSON.stringify(single?row:[row])});}
  if(u.includes('/rest/v1/settings')) return r.fulfill({status:200,headers:h,body:JSON.stringify(single?{}:[{}])});
  if(u.includes('/rest/v1/services')) return r.fulfill({status:200,headers:h,body:JSON.stringify([{id:'sv1',name:'Escova cabelo longo',price:85,commission:60,duration:60,active:true,online:true,order:1,category:'Cabelo'},{id:'sv2',name:'Pedicure',price:47,commission:80,duration:45,active:true,online:true,order:2,category:'Unhas'}])});
  if(u.includes('/rest/v1/sales')) return r.fulfill({status:200,headers:h,body:JSON.stringify([{id:'sa1',date:new Date(Date.now()-86400000).toISOString().slice(0,10),time:'13:32:00',barber_id:'b1',client_id:null,client_name:'asheley barbosa',items:[{qty:1,name:'escova cabelo longo',type:'service',price:85,refId:'sv1',commission:40.8,commissionBase:85,commissionRate:60}],subtotal:85,discount:17,total:68,payment:'pix',commission_total:40.8,created_at:new Date().toISOString()}])});
  if(u.includes('/rest/v1/barbers')) return r.fulfill({status:200,headers:h,body:JSON.stringify([{id:'b1',name:'Monique',active:true,sort:1,service_rate:null,product_rate:null}])});
  if(u.includes('/rest/v1/clients')) return r.fulfill({status:200,headers:h,body:JSON.stringify([client])});
  if(u.includes('/rest/v1/rpc/server_now')) return r.fulfill({status:200,headers:h,body:JSON.stringify(new Date().toISOString())});
  if(u.includes('/rest/v1/')) return r.fulfill({status:200,headers:h,body:single?'null':'[]'});
  return r.fulfill({status:200,headers:h,body:'{}'});
 });
 await p.goto('http://localhost:8766/#/painel',{waitUntil:'networkidle'}); await p.waitForTimeout(2500);

 const T=async()=>(await p.innerText('body')).replace(/\n+/g,' | ').slice(0,350);

 await p.goto('http://localhost:8766/#/painel/comissoes'); await p.waitForTimeout(2500);
 const T2=async()=>(await p.innerText('body')).replace(/\n+/g,' | ');
 let t=await T2(); console.log('pagina:',t.slice(0,300));
 const btn=p.getByText('Monique').first(); if(await btn.count()){await btn.click(); await p.waitForTimeout(800);}
 t=await T2(); const k=t.indexOf('BASE'); console.log('TABELA:', k>=0? t.slice(k-80,k+260): t.slice(0,500));
 await p.screenshot({path:process.env.S+'/h9.png',fullPage:true});
 await b.close();})();
