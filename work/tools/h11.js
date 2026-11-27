const {chromium}=require('playwright');
const b64=o=>Buffer.from(JSON.stringify(o)).toString('base64url');
const uid='11111111-1111-1111-1111-111111111111';
const jwt=b64({alg:'HS256',typ:'JWT'})+'.'+b64({sub:uid,role:'authenticated',aud:'authenticated',exp:Math.floor(Date.now()/1000)+36000,email:'t@t.com'})+'.sig';
const sess={access_token:jwt,refresh_token:'r',expires_in:36000,expires_at:Math.floor(Date.now()/1000)+36000,token_type:'bearer',user:{id:uid,aud:'authenticated',role:'authenticated',email:'t@t.com',app_metadata:{},user_metadata:{}}};
const client={id:'c1',name:'Mariana Teste',phone:'41999990000',birthday:null,anamnese:{},created_at:new Date().toISOString(),updated_at:new Date().toISOString()};
(async()=>{
 const b=await chromium.launch(); const ctx=await b.newContext({viewport:{width:740,height:800}}); const p=await ctx.newPage();
 const errs=[]; p.on('pageerror',e=>errs.push(e.message+' '+(e.stack||'').split('\n').slice(1,3).join(' '))); p.on('console',m=>{if(m.type()==='error')errs.push('console: '+m.text().slice(0,150))});
 await ctx.addInitScript(([k,v])=>localStorage.setItem(k,v),['sb-xdvnoxliymhtayvsljlj-auth-token',JSON.stringify(sess)]);

 const today=new Date().toISOString().slice(0,10); const calls=[];const H={0:null,1:['09:00','19:00'],2:['09:00','19:00'],3:['09:00','19:00'],4:['09:00','19:00'],5:['09:00','19:00'],6:['09:00','13:00']};const sale={id:'v1',date:today,time:'10:00',barber_id:'b1',client_id:'c1',client_name:'Mariana Teste',items:[{type:'service',refId:'sv1',name:'Corte',price:100,qty:1,commissionRate:60,commission:48}],subtotal:100,discount:20,total:80,payment:'pix',commission_total:48,created_at:new Date().toISOString()};
 const appts=[{id:'a1',date:today,time:'10:00',duration:60,barber_id:'b1',service_ids:['sv1'],client_id:'c1',client_name:'Mariana Teste',client_phone:'41999990000',total:85,status:'agendado',notes:'',source:'balcao',created_at:new Date().toISOString()},
              {id:'a2',date:today,time:'11:00',duration:45,barber_id:'b2',service_ids:['sv2'],client_id:'c1',client_name:'Mariana Teste',client_phone:'41999990000',total:47,status:'agendado',notes:'',source:'balcao',created_at:new Date().toISOString()}];
 await p.route(/supabase\.co/,async r=>{
  const u=r.request().url(), m=r.request().method(), h={'access-control-allow-origin':'*','access-control-allow-headers':'*','access-control-allow-methods':'*','content-type':'application/json'};
  if(m==='OPTIONS') return r.fulfill({status:200,headers:h,body:''});
  const single=/vnd.pgrst.object/.test(r.request().headers()['accept']||'');
  if(u.includes('/auth/v1/user')) return r.fulfill({status:200,headers:h,body:JSON.stringify(sess.user)});
  if(u.includes('/rest/v1/rpc/create_sale')){calls.push(JSON.parse(r.request().postData()));return r.fulfill({status:200,headers:h,body:JSON.stringify('sale-'+calls.length)});}
  if(u.includes('/rest/v1/staff')){const row={id:'s1',user_id:uid,role:'admin',name:'Teste',barber_id:null,email:'t@t.com'};return r.fulfill({status:200,headers:h,body:JSON.stringify(single?row:[row])});}
  if(u.includes('/rest/v1/settings')) return r.fulfill({status:200,headers:h,body:JSON.stringify(single?{hours:H}:[{hours:H}])});
  if(u.includes('/rest/v1/services')) return r.fulfill({status:200,headers:h,body:JSON.stringify([{id:'sv1',name:'Escova cabelo longo',price:85,commission:60,duration:60,active:true,online:true,order:1,category:'Cabelo'},{id:'sv2',name:'Pedicure',price:47,commission:80,duration:45,active:true,online:true,order:2,category:'Unhas'}])});
  if(u.includes('/rest/v1/barbers')) return r.fulfill({status:200,headers:h,body:JSON.stringify([{id:'b1',name:'Luciane Wolcher',active:true,sort:1},{id:'b2',name:'Ana Souza',active:true,sort:2}])});
  if(u.includes('/rest/v1/clients')) return r.fulfill({status:200,headers:h,body:JSON.stringify([client])});
  if(u.includes('/rest/v1/sales')&&m==='GET') return r.fulfill({status:200,headers:h,body:JSON.stringify([sale])});
  if(u.includes('/rest/v1/appointments')&&m==='GET') return r.fulfill({status:200,headers:h,body:JSON.stringify(appts)});
  if(u.includes('/rest/v1/rpc/server_now')) return r.fulfill({status:200,headers:h,body:JSON.stringify(new Date().toISOString())});
  if(u.includes('/rest/v1/')) return r.fulfill({status:200,headers:h,body:single?'null':'[]'});
  return r.fulfill({status:200,headers:h,body:'{}'});
 });
 await p.goto('http://localhost:8766/#/painel',{waitUntil:'networkidle'}); await p.waitForTimeout(2000);
 await p.goto('http://localhost:8766/#/painel/comissoes'); await p.waitForTimeout(2500);
 console.log((await p.innerText('body')).replace(/\n+/g,' | ').slice(0,500));
 const btn=p.getByText('Luciane Wolcher').first(); await btn.click().catch(e=>console.log('noclick')); await p.waitForTimeout(1000);
 console.log('MODAL:',(await p.locator('.modal-body').innerText().catch(()=>'sem modal')).replace(/\n+/g,' | ').slice(0,700));
 await p.screenshot({path:'/tmp/s/h11.png'});
 await p.goto('http://localhost:8766/#/painel/relatorios'); await p.waitForTimeout(3000);
 console.log('ERRS-REL',errs.slice(0,3));console.log('REL:',(await p.innerText('body')).replace(/\n+/g,' | ').slice(0,300));
 const [dl]=await Promise.all([p.waitForEvent('download',{timeout:20000}).catch(()=>null),p.getByRole('button',{name:/Extrato/}).first().click()]);
 if(dl){await dl.saveAs('/tmp/s/extrato.pdf');console.log('PDF salvo');}else console.log('sem download');
 console.log('ERRS',errs.slice(0,4)); await b.close();})();
