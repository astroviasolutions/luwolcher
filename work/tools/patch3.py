p='/home/user/luwolcher/work/site/assets/index-B-Eix5hJ.js'
s=open(p,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(s.count(old),old[:70])
    s=s.replace(old,new)
# PDF comprimido (de ~3,4 MB para poucas dezenas de KB)
rep("new TS({unit:`mm`,format:`a4`})","new TS({unit:`mm`,format:`a4`,compress:!0})")
# upload: renova a sessão antes e tenta de novo em falha de rede/token vencido
rep("async uploadClientFile(e,t,i){let a=`${e}/${Date.now()}-${t.name.normalize(`NFD`).replace(/[^\\w.-]+/g,`_`)}`;return r(await n.storage.from(`anexos`).upload(a,t,{contentType:t.type||`application/octet-stream`})),",
    "async uploadClientFile(e,t,i){await n.auth.getSession().catch(()=>{});let a=`${e}/${Date.now()}-${t.name.normalize(`NFD`).replace(/[^\\w.-]+/g,`_`)}`;for(let k=0;;k++)try{r(await n.storage.from(`anexos`).upload(a,t,{contentType:t.type||`application/octet-stream`}));break}catch(x){if(k>=2)throw x;if(/jwt|expired|401/i.test(x.message))await n.auth.refreshSession().catch(()=>{});else if(!/fetch|network|timeout|failed|load/i.test(x.message))throw x;await new Promise(z=>setTimeout(z,1e3*(k+1)))}return ")
open(p,'w',encoding='utf-8').write(s); print('ok')
