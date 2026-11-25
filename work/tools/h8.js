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
  if(u.includes('/rest/v1/barbers')) return r.fulfill({status:200,headers:h,body:JSON.stringify([{id:'b1',name:'Luciane Wolcher',active:true,sort:1}])});
  if(u.includes('/rest/v1/clients')) return r.fulfill({status:200,headers:h,body:JSON.stringify([client])});
  if(u.includes('/rest/v1/rpc/server_now')) return r.fulfill({status:200,headers:h,body:JSON.stringify(new Date().toISOString())});
  if(u.includes('/rest/v1/')) return r.fulfill({status:200,headers:h,body:single?'null':'[]'});
  return r.fulfill({status:200,headers:h,body:'{}'});
 });
 await p.goto('http://localhost:8766/#/painel',{waitUntil:'networkidle'}); await p.waitForTimeout(2500);

 const T=async()=>(await p.innerText('body')).replace(/\n+/g,' | ').slice(0,350);

 await p.goto('http://localhost:8766/#/painel/caixa'); await p.waitForTimeout(2500);
  console.log('caixa:',(await T()).slice(0,260));
 await p.getByText('Escova cabelo longo').first().click(); await p.waitForTimeout(600);
 console.log('apos add:',(await p.locator('.cart-lines').innerText().catch(()=>'sem cart-lines')).replace(/\n+/g,' | '));
 await p.locator('.inc-btn').first().click(); await p.waitForTimeout(400);
 await p.getByLabel(/Desconto em/).fill('20%'); await p.waitForTimeout(200);
 console.log('painel:',(await p.locator('.inc-edit').innerText()).replace(/\n+/g,' | '));
 await p.getByRole('button',{name:'Aplicar'}).click(); await p.waitForTimeout(600);
 console.log('linha:',(await p.locator('.cart-lines').innerText()).replace(/\n+/g,' | '));
 const all=await T(); const m=all.match(/Total[^|]*\|[^|]*|Comissão de[^|]*\|?[^|]*/g); console.log('resumo:',JSON.stringify(m));
 const full=await T(); console.log('TEXTO-FINAL:',full.slice(full.indexOf('Subtotal')-60, full.indexOf('Subtotal')+500)); await p.screenshot({path:process.env.S+'/h8.png',fullPage:true});
 await b.close();})();
