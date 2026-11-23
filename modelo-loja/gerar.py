#!/usr/bin/env python3
"""Gera o site de uma loja a partir do modelo (o site da Izone) e de um arquivo de configuração.

Uso:  python3 gerar.py lojas/demo.json
Saída: sites/<slug>/index.html (+ img/ se a loja tiver fotos)
"""
import json, os, re, sys, shutil, urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "..", "izone-cwb", "index.html")


def troca(s, velho, novo, minimo=1):
    n = s.count(velho)
    if n < minimo:
        sys.exit(f"Texto do modelo não encontrado: {velho[:60]!r}")
    return s.replace(velho, novo)


def gerar(cfg_path):
    c = json.load(open(cfg_path, encoding="utf-8"))
    s = open(BASE, encoding="utf-8").read()
    slug = c["slug"]

    # Nomes e textos da loja
    s = troca(s, "Izone CWB", c["nome"])
    s = troca(s, '<span class="logo-word">IZONE</span>', f'<span class="logo-word">{c["logoTexto"]}</span>', 2)
    s = troca(s, '<span class="logo-tag">CWB</span>', f'<span class="logo-tag">{c["logoTag"]}</span>' if c.get("logoTag") else "", 2)
    s = troca(s, '<span class="logo-mark">i</span>', f'<span class="logo-mark">{c["inicial"]}</span>', 2)
    s = troca(s, "Black Friday Izone", f"Black Friday {c.get('nomeCurto', c['nome'])}")
    s = troca(s, "Black Friday <span>Izone</span>", f"Black Friday <span>{c.get('nomeCurto', c['nome'])}</span>")
    s = troca(s, "Curitiba", c["cidade"])
    s = troca(s, "Batel", c["bairro"])
    s = troca(s, "izone-cart2", f"{slug}-cart")
    s = troca(s, "IZ-17PM-256", c.get("codigoEtiqueta", "17PM-256"))

    # Bloco de configuração (WhatsApp, endereço, Pix...)
    loja = {k: c.get(k, "") for k in ["whatsapp", "whatsappExibir", "instagram", "email", "endereco", "horario", "cnpj", "chavePix"]}
    bloco = "const LOJA = {\n" + "".join(f"  {k}: {json.dumps(v, ensure_ascii=False)},\n" for k, v in loja.items())
    bloco += f'  demo: {"true" if c.get("demo") else "false"},\n'
    bloco += "  parcelas: [12,18,24],\n  fator: {12:0.0958, 18:0.0687, 24:0.0559},\n"
    bloco += f'  inicioBlackFriday: "{c.get("inicioBlackFriday", "2026-11-27T00:00:00-03:00")}",\n'
    bloco += f'  fimBlackFriday: "{c.get("fimBlackFriday", "2026-11-30T23:59:59-03:00")}",\n'
    m = re.search(r"  /\* Simulador.*?\n  simulador: \{.*?\n  \}", s, flags=re.S)
    if not m:
        sys.exit("Configuração do simulador não encontrada no modelo")
    bloco += ("  simulador: " + json.dumps(c["simulador"], ensure_ascii=False)) if c.get("simulador") else m.group(0)
    bloco += "\n};"
    s, n = re.subn(r"const LOJA = \{.*?\n\};", lambda m: bloco, s, count=1, flags=re.S)
    if n != 1:
        sys.exit("Bloco LOJA não encontrado")

    # Sem número: o link do WhatsApp abre para o cliente escolher o contato (modo demonstração)
    s = troca(s, "const wa = msg => `https://wa.me/${LOJA.whatsapp}?text=${encodeURIComponent(msg)}`;",
              "const wa = msg => LOJA.whatsapp ? `https://wa.me/${LOJA.whatsapp}?text=${encodeURIComponent(msg)}` : `https://wa.me/?text=${encodeURIComponent(msg)}`;")

    # Fotos: só as que a loja tiver em lojas/<slug>-img/
    pasta_fotos = os.path.join(AQUI, "lojas", f"{slug}-img")
    fotos = sorted(f[:-4] for f in os.listdir(pasta_fotos) if f.endswith(".jpg")) if os.path.isdir(pasta_fotos) else []
    s, n = re.subn(r"const FOTOS=new Set\(\[.*?\]\);", "const FOTOS=new Set(" + json.dumps(fotos) + ");", s, count=1)
    if n != 1:
        sys.exit("Lista FOTOS não encontrada")

    # Destaque: foto própria (lojas/<slug>-img/hero.png) ou a ilustração
    hero_linhas = """$("#heroPhone").innerHTML='<img src="img/hero-17pm.png" alt="iPhone 17 Pro Max laranja-cósmico">';\n$("#heroSwatches").hidden=true;\n"""
    if os.path.isfile(os.path.join(pasta_fotos, "hero.png")):
        s = troca(s, hero_linhas, hero_linhas.replace("hero-17pm.png", "hero.png"))
    else:
        s = troca(s, hero_linhas, "")

    # Prévia de link (WhatsApp/Instagram)
    url = c.get("url", "")
    s = re.sub(r'<meta property="og:image" content="[^"]*">',
               f'<meta property="og:image" content="{url}/img/hero.png">' if url and fotos else "", s)

    # Cor principal
    cor = c.get("cor")
    if cor:
        css = f"\n:root{{--accent:{cor['clara']};--accent-soft:{cor['suaveClara']}}}\n@media (prefers-color-scheme:dark){{:root:not([data-theme=\"light\"]){{--accent:{cor['escura']};--accent-soft:{cor['suaveEscura']}}}}}\n:root[data-theme=\"dark\"]{{--accent:{cor['escura']};--accent-soft:{cor['suaveEscura']}}}\n"
        s = troca(s, "</style>", css + "</style>")
        fav = urllib.parse.quote(cor["clara"])
        s = s.replace("fill='%23E2591B'", f"fill='{fav}'")

    # Faixa de demonstração
    if c.get("demo"):
        contato = c.get("contatoVendedor", "")
        botao = f'<a href="{contato}" target="_blank" rel="noopener">Quero um site assim · {c.get("contatoExibir","")}</a>' if contato else ""
        faixa = f'''<div class="demo-bar" role="note"><div class="wrap"><span><b>Site de demonstração{(' da ' + c['marcaVendedor']) if c.get('marcaVendedor') else ''}.</b> Preços e depoimentos ilustrativos. O site da sua loja sai com o seu nome, suas cores e suas fotos.</span><span class="demo-cores" aria-label="Testar outra cor">Teste outra cor: <button type="button" data-cor="#E2591B,#FF7533,#FBE3D6,#3A2115" style="background:#E2591B" aria-label="Laranja"></button><button type="button" data-cor="#2457D6,#5B8CFF,#DCE6FB,#17244A" style="background:#2457D6" aria-label="Azul"></button><button type="button" data-cor="#0E8A5F,#2FC48D,#D4F1E4,#0F3326" style="background:#0E8A5F" aria-label="Verde"></button><button type="button" data-cor="#B0257A,#E35BB0,#F7DCEC,#3B1530" style="background:#B0257A" aria-label="Rosa"></button><button type="button" data-cor="#11151B,#EEF1F5,#E2E6EB,#2A313C" style="background:#11151B" aria-label="Grafite"></button></span>{botao}</div></div>
'''
        s = troca(s, '<div class="bf-bar" role="region"', faixa + '<div class="bf-bar" role="region"')
        css = """.demo-bar{background:var(--accent);color:var(--accent-ink);font-size:13px}
.demo-bar .wrap{display:flex;flex-wrap:wrap;gap:6px 18px;align-items:center;justify-content:center;padding-block:8px;text-align:center}
.demo-bar a{color:inherit;font-weight:800;background:rgba(0,0,0,.18);padding:4px 12px;border-radius:999px;text-decoration:none}
.demo-cores{display:inline-flex;gap:6px;align-items:center}
.demo-cores button{width:20px;height:20px;border-radius:50%;border:2px solid rgba(255,255,255,.85);cursor:pointer;padding:0}
"""
        s = troca(s, "</style>", css + "</style>")
        js = """document.querySelectorAll("[data-cor]").forEach(b=>b.onclick=()=>{const [a,ad,so,sod]=b.dataset.cor.split(",");const dark=document.documentElement.dataset.theme==="dark"||(!document.documentElement.dataset.theme&&matchMedia("(prefers-color-scheme: dark)").matches);const r=document.documentElement.style;r.setProperty("--accent",dark?ad:a);r.setProperty("--accent-soft",dark?sod:so)});\n"""
        js += """function registrarPedido(o){try{const K="vitrio-pedidos",a=JSON.parse(localStorage.getItem(K)||"[]");const n=Math.max(1042,...a.map(p=>+String(p.id).replace(/\\D/g,"")||0))+1;a.push(Object.assign({id:"P"+n,em:Date.now(),status:"novo"},o));localStorage.setItem(K,JSON.stringify(a))}catch(e){}}
document.getElementById("checkout").addEventListener("submit",()=>setTimeout(()=>{if(document.getElementById("done").hidden)return;const m=document.querySelector('input[name="pag"]:checked').value,st=subtotal();registrarPedido({loja:"Sua Loja (celulares)",cliente:document.getElementById("f-nome").value.trim(),itens:cart.map(it=>{const p=byId(it.id),op=p.arm[it.a];return{q:it.q,nome:p.nome+(op.l!=="Única"?" "+op.l:""),preco:op.p*it.q}}),total:st,entrega:document.querySelector('input[name="entrega"]:checked').value,pagamento:m==="pix"?"Pix":m==="credito"?"Cartão em "+document.getElementById("f-parc").value+"x":"Débito ou dinheiro"})},50));
"""
        s = troca(s, "hero();\n", js + "hero();\n")

    destino = os.path.join(AQUI, "sites", slug)
    os.makedirs(destino, exist_ok=True)
    open(os.path.join(destino, "index.html"), "w", encoding="utf-8").write(s)
    if fotos or os.path.isfile(os.path.join(pasta_fotos, "hero.png")):
        shutil.copytree(pasta_fotos, os.path.join(destino, "img"), dirs_exist_ok=True)
    print("Site gerado em", os.path.relpath(destino, AQUI), "| fotos:", len(fotos))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    gerar(sys.argv[1])
