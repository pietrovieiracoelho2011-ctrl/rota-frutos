// Tira as capturas de tela (tamanho celular) de cada exemplo e salva em vitrio-site/img/ex-<nome>.jpg
// Uso, a partir da pasta vitrio-site:  node fontes/prints.js
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');
const SITE = path.resolve(__dirname, '..');
(async () => {
  const b = await chromium.launch();
  for (const n of ['celular', 'tech', 'painel', 'hamburgueria', 'cafe', 'moda']) {
    const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    await p.goto(pathToFileURL(path.join(SITE, 'exemplos', n, 'index.html')).href);
    await p.addStyleTag({ content: '.demo,.demo-bar,.wa-float,.floatcart{display:none!important}' });
    await p.waitForTimeout(1600);
    await p.screenshot({ path: path.join(SITE, 'img', `ex-${n}.jpg`), type: 'jpeg', quality: 80 });
    await p.close();
  }
  await b.close();
})();
