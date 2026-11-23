const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
for(const n of ['celular','tech','painel','hamburgueria','cafe','moda']){const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});
await p.goto(`file:///home/user/rota-frutos/vitrio-site/exemplos/${n}/index.html`);await p.addStyleTag({content:'.demo,.demo-bar,.wa-float,.floatcart{display:none!important}'});await p.waitForTimeout(1600);
await p.screenshot({path:`img/ex-${n}.jpg`,type:'jpeg',quality:80});await p.close()}await b.close()})();
