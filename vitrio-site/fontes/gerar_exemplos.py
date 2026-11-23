#!/usr/bin/env python3
"""Gera as lojas de exemplo por nicho a partir de fontes/nicho.html.
Uso: python3 fontes/gerar_exemplos.py   ->  exemplos/<nicho>/index.html
"""
import json, os, urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(AQUI, "..")
BASE = open(os.path.join(AQUI, "nicho.html"), encoding="utf-8").read()

EXEMPLOS = {
 "hamburgueria": {
  "visual": dict(NOME="Brasa & Pão", MARCA_HTML="Brasa <span>&amp;</span> Pão",
     DESCRICAO="Hamburgueria artesanal. Peça pelo site e receba o pedido pronto no WhatsApp.",
     FONTES_URL="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;600;700;800&display=swap",
     FONTE_TITULO='"Anton","Impact",sans-serif', FONTE_TEXTO='"Inter",system-ui,sans-serif', TITULO_PESO="400", TITULO_ESPACO=".01em",
     COR_FUNDO="#141010", COR_CARTAO="#1E1817", COR_POCO="#2A211F", COR_TEXTO="#F7EFE6", COR_SUAVE="#B8A99C", COR_LINHA="#3A2E2B",
     COR_DESTAQUE="#FF8A1F", COR_DESTAQUE_TEXTO="#1A0E04", COR_DESTAQUE_SUAVE="#3C2414", ESQUEMA="dark", RAIO="20px", PROPORCAO_FOTO="1/1",
     TXT_SACOLA="Pedido", TXT_PEDIDO="Seu pedido",
     HERO_EYEBROW="Hambúrguer artesanal na brasa", HERO_TITULO="Fome de verdade pede lanche de verdade.",
     HERO_TEXTO="Monte seu pedido, escolha os adicionais e mande direto para o nosso WhatsApp. Sem aplicativo e sem taxa escondida.",
     HERO_CHIPS="<span>🛵 Entrega em 40 min</span><span>🍔 Blend de 150 g</span><span>💳 Pix, cartão ou dinheiro</span>",
     ENDERECO="Rua Exemplo, 100 · Curitiba - PR", HORARIO_TXT="Terça a domingo, das 18h às 23h30"),
  "config": {
   "slug":"hamburgueria","nome":"Brasa & Pão","heroArte":"burger","heroExtra":True,"txtPedido":"Pedido","txtVazio":"Seu pedido está vazio",
   "horario":{"0":["18:00","23:30"],"2":["18:00","23:30"],"3":["18:00","23:30"],"4":["18:00","23:30"],"5":["18:00","23:59"],"6":["18:00","23:59"]},
   "obsDica":"Ex.: sem cebola, carne ao ponto",
   "heroFoto":"burger.jpg",
   "categorias":[{"id":"lanches","nome":"Lanches"},{"id":"porcoes","nome":"Porções"},{"id":"bebidas","nome":"Bebidas"}],
   "adicionais":[["Bacon",5],["Cheddar extra",4],["Ovo",3],["Cebola caramelizada",4],["Carne extra 150 g",12]],
   "entrega":[["Retirar no balcão","",0],["Entrega","",7]],
   "pagamentos":["Pix","Cartão na entrega","Dinheiro"],
   "produtos":[
    {"id":"b1","cat":"lanches","nome":"Brasa Cheddar Bacon","desc":"Pão brioche, blend 150 g, cheddar cremoso, bacon crocante, alface e molho da casa.","preco":38.9,"foto":"burger.jpg","adicionais":True,"tag":"Mais pedido"},
    {"id":"b4","cat":"lanches","nome":"Dog Especial","desc":"Pão com gergelim, salsicha, carne desfiada, ketchup e mostarda.","preco":24.9,"foto":"hotdog.jpg","adicionais":True},
    {"id":"p1","cat":"porcoes","nome":"Fritas da casa","desc":"Batata crocante na cestinha. Serve 2.","preco":22.9,"foto":"fritas.jpg","tag":"Novo"},
    {"id":"d1","cat":"bebidas","nome":"Refrigerante lata","desc":"350 ml. Coca-Cola, Fanta, Sprite ou Guaraná.","preco":7,"foto":"refri.jpg"},
    {"id":"d2","cat":"bebidas","nome":"Milkshake de morango","desc":"400 ml, com morangos frescos.","preco":19.9,"foto":"shake-morango.jpg"},
    {"id":"d3","cat":"bebidas","nome":"Milkshake de chocolate","desc":"400 ml, com calda e raspas de chocolate.","preco":19.9,"foto":"shake-chocolate.jpg"}
   ]}
 },
 "moda": {
  "visual": dict(NOME="Ateliê Lis", MARCA_HTML="Ateliê <span>Lis</span>",
     DESCRICAO="Moda feminina com curadoria. Escolha tamanho e cor e finalize pelo WhatsApp.",
     FONTES_URL="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Manrope:wght@400;600;700;800&display=swap",
     FONTE_TITULO='"DM Serif Display",Georgia,serif', FONTE_TEXTO='"Manrope",system-ui,sans-serif', TITULO_PESO="400", TITULO_ESPACO="-.01em",
     COR_FUNDO="#FBF7F3", COR_CARTAO="#FFFFFF", COR_POCO="#F1E8E1", COR_TEXTO="#2A1F1C", COR_SUAVE="#7D6A63", COR_LINHA="#E7DCD4",
     COR_DESTAQUE="#9E3B4E", COR_DESTAQUE_TEXTO="#FFFFFF", COR_DESTAQUE_SUAVE="#F6E1E5", ESQUEMA="light", RAIO="6px", PROPORCAO_FOTO="4/5",
     TXT_SACOLA="Sacola", TXT_PEDIDO="Sua sacola",
     HERO_EYEBROW="Nova coleção · Verão", HERO_TITULO="Peças leves para dias que pedem cor.",
     HERO_TEXTO="Escolha o tamanho, monte sua sacola e finalize com a gente pelo WhatsApp. Trocas em até 7 dias.",
     HERO_CHIPS="<span>Até 3x sem juros</span><span>Troca grátis</span><span>Envio para todo o Brasil</span>",
     ENDERECO="Rua Exemplo, 200 · Curitiba - PR", HORARIO_TXT="Segunda a sábado, das 10h às 19h"),
  "config": {
   "slug":"moda","nome":"Ateliê Lis","heroArte":"vestido","heroCor":"#C9566B","txtPedido":"Sacola","txtVazio":"Sua sacola está vazia","parcelas":3,
   "horario":{"1":["10:00","19:00"],"2":["10:00","19:00"],"3":["10:00","19:00"],"4":["10:00","19:00"],"5":["10:00","19:00"],"6":["10:00","19:00"]},
   "obsDica":"Ex.: é para presente",
   "heroFoto":"vestido-floral.jpg",
   "categorias":[{"id":"vestidos","nome":"Vestidos"}],
   "entrega":[["Retirar na loja","",0],["Motoboy em Curitiba","",12],["Correios","",25]],
   "pagamentos":["Pix","Cartão em até 3x","Link de pagamento"],
   "produtos":[
    {"id":"v2","cat":"vestidos","nome":"Vestido Curto Flor","desc":"Estampa floral, alças finas e saia rodada.","preco":249.9,"foto":"vestido-floral.jpg","tamanhos":["P","M","G"],"tag":"Mais vendido"},
    {"id":"v1","cat":"vestidos","nome":"Vestido Midi Alfaiataria","desc":"Gola alfaiataria, botões e cinto. Ideal para trabalho e eventos.","preco":289.9,"foto":"vestido-midi.jpg","tamanhos":["P","M","G","GG"],"tag":"Novo"}
   ]}
 }
}

for slug, ex in EXEMPLOS.items():
    v = dict(ex["visual"])
    v["TXT_VITRIO"] = urllib.parse.quote(f"Olá! Vi o exemplo de site para {slug} da Vitrio e quero um assim para a minha loja.")
    v["CONFIG_JSON"] = json.dumps(ex["config"], ensure_ascii=False)
    s = BASE
    for k, val in v.items():
        s = s.replace("{{" + k + "}}", val)
    assert "{{" not in s, [l for l in s.splitlines() if "{{" in l][:3]
    os.makedirs(os.path.join(SITE, "exemplos", slug), exist_ok=True)
    open(os.path.join(SITE, "exemplos", slug, "index.html"), "w", encoding="utf-8").write(s)
    print("ok", slug)
