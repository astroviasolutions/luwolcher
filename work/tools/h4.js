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
  if(u.includes('/rest/v1/barbers')) return r.fulfill({status:200,headers:h,body:JSON.stringify([{id:'b1',name:'Luciane Wolcher',active:true,sort:1}])});
  if(u.includes('/rest/v1/clients')) return r.fulfill({status:200,headers:h,body:JSON.stringify([client])});
  if(u.includes('/rest/v1/rpc/server_now')) return r.fulfill({status:200,headers:h,body:JSON.stringify(new Date().toISOString())});
  if(u.includes('/rest/v1/')) return r.fulfill({status:200,headers:h,body:single?'null':'[]'});
  return r.fulfill({status:200,headers:h,body:'{}'});
 });
 await p.goto('http://localhost:8766/#/painel',{waitUntil:'networkidle'}); await p.waitForTimeout(2500);

 const T=async()=>(await p.innerText('body')).replace(/\n+/g,' | ').slice(0,350);
 await p.goto('http://localhost:8766/#/painel/clientes'); await p.waitForTimeout(1500); console.log('clientes:',await T());
 await p.getByText('Mariana Teste').first().click(); await p.waitForTimeout(800); console.log('ficha:',await T());
 for (const t of ['Termos']) { const l=p.getByText(t,{exact:true}); if(await l.count()){ await l.first().click(); await p.waitForTimeout(500); console.log('aba',t); break; } }
 console.log('apos aba:',await T());
 const nt=p.getByText(/Novo termo/); console.log('novo termo btn:',await nt.count()); if(await nt.count()){ await nt.first().click(); await p.waitForTimeout(800);}

 await p.waitForTimeout(500);
 const modals=()=>p.locator('.modal-bg').count();
 console.log('modais abertos:',await modals());
 const m=p.locator('.modal').last(); const bb=await m.boundingBox(); console.log('modal box',JSON.stringify(bb));
 const foot=p.locator('.modal-foot').last(); console.log('footer box',JSON.stringify(await foot.boundingBox()));
 await p.screenshot({path:process.env.S+'/h2.png'});
 // desenha assinatura
 const cv=p.locator('canvas').first(); await cv.scrollIntoViewIfNeeded(); const cb=await cv.boundingBox();
 await p.mouse.move(cb.x+40,cb.y+40); await p.mouse.down(); await p.mouse.move(cb.x+120,cb.y+90,{steps:8}); await p.mouse.move(cb.x+200,cb.y+50,{steps:8}); await p.mouse.up(); await p.waitForTimeout(300);
 console.log('botoes salvar:',await p.getByRole('button',{name:/Salvar/}).count(), '| textos:', JSON.stringify(await p.getByRole('button',{name:/Salvar/}).allInnerTexts()));
 await p.screenshot({path:process.env.S+'/h3.png'});
 await p.mouse.click(4,4); await p.waitForTimeout(500);
 console.log('apos clique fora, modal do termo ainda aberto:', await p.getByText(/Termo de consentimento ·/).count());

 await b.close();})();
