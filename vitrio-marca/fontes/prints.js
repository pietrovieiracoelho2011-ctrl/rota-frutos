const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
const U='file:///home/user/rota-frutos/modelo-loja/sites/demo/index.html';
const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});
const hide=async()=>p.addStyleTag({content:'.demo-bar,.wa-float{display:none!important}'});
await p.goto(U);await hide();await p.waitForTimeout(1800);await p.screenshot({path:'fontes/print-home.png'});
await p.goto(U+'#loja-seminovos');await hide();await p.waitForTimeout(900);await p.evaluate(()=>window.scrollTo(0,520));await p.waitForTimeout(400);await p.screenshot({path:'fontes/print-loja.png'});
await p.goto(U+'#parcelamento');await hide();await p.waitForTimeout(800);await p.selectOption('#simProd','n17pm|0');await p.fill('#simEntrada','1000');await p.click('[data-n="18"]');await p.evaluate(()=>window.scrollTo(0,document.querySelector('.sim-res').getBoundingClientRect().top+scrollY-130));await p.waitForTimeout(400);await p.screenshot({path:'fontes/print-sim.png'});
await p.goto(U+'#ideal');await hide();await p.waitForTimeout(600);for(const v of ['5500','camera','normal','tanto']){await p.click(`[data-qv="${v}"]`);await p.waitForTimeout(150)}await p.waitForTimeout(800);await p.evaluate(()=>window.scrollTo(0,document.querySelector('#quizBox').getBoundingClientRect().top+scrollY-120));await p.waitForTimeout(300);await p.screenshot({path:'fontes/print-quiz.png'});
await b.close()})();
