# Modelo de site para lojas de celular

O modelo usa o site da Izone (`../izone-cwb/index.html`) como base e troca nome, cidade, WhatsApp, cores e fotos.

## Montar uma loja nova
1. Copie `lojas/demo.json` para `lojas/<slug>.json` e preencha os dados. Retire `"demo": true`.
2. (Opcional) Fotos em `lojas/<slug>-img/` com o nome `<id-do-produto>-<versão>.jpg` (ex.: `n17pm-0.jpg`) e `hero.png` para o destaque.
3. Gere: `python3 gerar.py lojas/<slug>.json` → `sites/<slug>/`
4. Publique: `CLOUDFLARE_ACCOUNT_ID=... CLOUDFLARE_API_TOKEN=... python3 publicar.py <slug>`

Produtos e preços ficam no bloco `PRODUTOS` do site gerado.

## Demonstração
`lojas/demo.json` gera a loja de demonstração (sem número de WhatsApp, com faixa "Site de demonstração" e teste de cores).

## Kit de vendas
`kit-de-vendas.html`: passo a passo, mensagens, preços, objeções e contrato.
