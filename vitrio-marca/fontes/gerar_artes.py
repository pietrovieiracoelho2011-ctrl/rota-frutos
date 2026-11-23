#!/usr/bin/env python3
"""Gera as artes do Instagram da Vitrio (HTML -> PNG com Playwright). Uso: python3 fontes/gerar_artes.py"""
import os, json, base64, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "..")
INK, BLUE, ICE, AMBER, MUTE = "#0E1328", "#2D5BFF", "#EAF0FF", "#FFB84D", "#5B6684"
HANDLE = "@vitriositesbr"
WHATS = "(41) 99131-2403"

def b64(nome):
    return "data:image/png;base64," + base64.b64encode(open(os.path.join(AQUI, nome), "rb").read()).decode()

def mark(size=100, bg=BLUE, fg="#fff", dot=AMBER, rx=26):
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="100" rx="{rx}" fill="{bg}"/>
<path d="M24 27h15l11 30 11-30h15L57 77H43Z" fill="{fg}"/>
<path d="M50 57 61 27h15L57 77H50Z" fill="{fg}" opacity=".62"/>
<circle cx="79" cy="20" r="7" fill="{dot}"/></svg>'''

def wordmark(size=120, cor=INK, dot=AMBER):
    # "vitrio" com os pingos dos i em âmbar
    return f'''<span class="wm" style="font-size:{size}px;color:{cor}">v<span class="i" style="--dot:{dot}">ı</span>tr<span class="i" style="--dot:{dot}">ı</span>o</span>'''

def _fonte(fam):
    p = os.path.join(AQUI, "woff", f"{fam}-800-latin.woff2")
    return "@font-face{font-family:'%s';src:url(data:font/woff2;base64,%s) format('woff2');font-weight:100 900;font-display:block}" % (fam, base64.b64encode(open(p, "rb").read()).decode())
FONTES = _fonte("Unbounded") + _fonte("Manrope")

BASE_CSS = f"""
{FONTES}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:var(--w);height:var(--h);overflow:hidden;font-family:Manrope,Arial,sans-serif;-webkit-font-smoothing:antialiased}}
.wm{{font-family:Unbounded,Arial Black,sans-serif;font-weight:800;letter-spacing:-.04em;line-height:1;display:inline-block}}
.wm .i{{position:relative;display:inline-block}}
.wm .i::after{{content:"";position:absolute;left:50%;top:-.06em;width:.2em;height:.2em;border-radius:50%;background:var(--dot);transform:translateX(-50%)}}
h1,h2{{font-family:Unbounded,Arial Black,sans-serif;font-weight:800;letter-spacing:-.025em;line-height:1.04}}
.foot{{position:absolute;left:90px;right:90px;bottom:70px;display:flex;align-items:center;justify-content:space-between;font-weight:700;font-size:28px}}
.foot .brand{{display:flex;align-items:center;gap:16px}}
.phone{{position:absolute;border-radius:64px;padding:16px;background:#0A0D18;box-shadow:0 50px 90px -30px rgba(0,0,0,.55),0 0 0 2px rgba(255,255,255,.06)}}
.phone img{{display:block;width:100%;height:100%;object-fit:cover;object-position:top;border-radius:50px}}
.phone::before{{content:"";position:absolute;top:30px;left:50%;width:110px;height:32px;border-radius:20px;background:#0A0D18;transform:translateX(-50%);z-index:2}}
.pill{{display:inline-block;font-weight:800;font-size:26px;letter-spacing:.12em;text-transform:uppercase;padding:12px 22px;border-radius:999px}}
"""

def page(w, h, body, css=""):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>:root{{--w:{w}px;--h:{h}px}}{BASE_CSS}{css}</style></head><body>{body}</body></html>"

def foot(cor, sub=None):
    return f'<div class="foot" style="color:{cor}"><span class="brand">{mark(54)}{wordmark(40, cor)}</span><span style="opacity:.75">{sub or HANDLE}</span></div>'

ARTES = {}

# ---------- Logo ----------
ARTES["logo/perfil-instagram"] = (1080, 1080, page(1080, 1080,
    f'<div style="width:1080px;height:1080px;background:{BLUE};display:grid;place-items:center">{mark(660, BLUE, "#fff", AMBER, 0)}</div>'))
ARTES["logo/logo-horizontal-claro"] = (1800, 600, page(1800, 600,
    f'<div style="width:1800px;height:600px;background:#fff;display:flex;align-items:center;justify-content:center;gap:60px">{mark(300)}{wordmark(230, INK)}</div>'))
ARTES["logo/logo-horizontal-escuro"] = (1800, 600, page(1800, 600,
    f'<div style="width:1800px;height:600px;background:{INK};display:flex;align-items:center;justify-content:center;gap:60px">{mark(300)}{wordmark(230, "#fff")}</div>'))
ARTES["logo/simbolo"] = (1000, 1000, page(1000, 1000, f'<div style="width:1000px;height:1000px;display:grid;place-items:center;background:transparent">{mark(1000)}</div>'))

# ---------- Posts (1080x1350) ----------
W, H = 1080, 1350
def post_phone(bg, fg, eyebrow, titulo, sub, img, eyecor=AMBER, subcor=None):
    return page(W, H, f'''<div style="position:relative;width:{W}px;height:{H}px;background:{bg};overflow:hidden">
<div style="position:absolute;left:90px;top:90px;right:90px">
<span class="pill" style="background:{eyecor};color:{INK}">{eyebrow}</span>
<h1 style="color:{fg};font-size:66px;margin-top:34px;max-width:820px">{titulo}</h1>
<p style="color:{subcor or fg};opacity:.8;font-size:32px;line-height:1.4;margin-top:22px;max-width:860px;font-weight:600">{sub}</p></div>
<div style="position:absolute;right:90px;top:90px">{mark(70)}</div>
<div class="phone" style="left:265px;top:640px;width:550px;height:1090px"><img src="{b64(img)}"></div></div>''')

ARTES["posts/09-capa"] = (W, H, page(W, H, f'''<div style="position:relative;width:{W}px;height:{H}px;background:{BLUE};overflow:hidden">
<div style="position:absolute;right:-260px;top:-200px;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.18),transparent 65%)"></div>
<div style="position:absolute;left:90px;top:100px;right:90px">{wordmark(120,"#fff")}
<h1 style="color:#fff;font-size:86px;margin-top:70px">Sua loja aberta 24 horas no celular do cliente.</h1>
<p style="color:#fff;opacity:.88;font-size:34px;line-height:1.4;margin-top:30px;font-weight:600;max-width:500px">Sites de vendas com preço, parcelas e pedido direto no WhatsApp.</p></div>
<div class="phone" style="left:640px;top:620px;width:420px;height:860px;transform:rotate(6deg)"><img src="{b64('print-home.png')}"></div>
<div class="foot" style="color:#fff;right:auto"><span>{HANDLE}</span></div></div>'''))

ARTES["posts/08-oferta"] = (W, H, page(W, H, f'''<div style="position:relative;width:{W}px;height:{H}px;background:{INK};overflow:hidden">
<div style="position:absolute;left:90px;top:100px;right:90px">
<span class="pill" style="background:{AMBER};color:{INK}">Lançamento</span>
<h1 style="color:#fff;font-size:76px;margin-top:40px">Só para as <span style="color:{AMBER}">3 primeiras</span> lojas.</h1>
<div style="margin-top:70px;display:grid;gap:22px">
<div style="background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.12);border-radius:32px;padding:40px 44px">
<p style="color:#9AA6C8;font-size:28px;font-weight:700;text-decoration:line-through">De R$ 1.497</p>
<p style="color:#fff;font-family:Unbounded,Arial Black,sans-serif;font-weight:800;font-size:110px;line-height:1.05">R$ 497</p>
<p style="color:#fff;font-size:34px;font-weight:700;margin-top:10px">para montar o site completo da sua loja</p></div>
<div style="background:{BLUE};border-radius:32px;padding:34px 44px;color:#fff;font-size:38px;font-weight:800">+ 1º mês de manutenção grátis</div></div>
<p style="color:#C9D1EA;font-size:32px;margin-top:50px;font-weight:600">Chame no WhatsApp: <b style="color:#fff">{WHATS}</b></p></div>
{foot("#fff")}</div>'''))

ARTES["posts/07-quanto-custa"] = (W, H, page(W, H, f'''<div style="position:relative;width:{W}px;height:{H}px;background:{ICE};overflow:hidden">
<div style="position:absolute;left:90px;top:100px;right:90px">
<h1 style="color:{INK};font-size:76px">Chega de responder <span style="color:{BLUE}">"quanto custa?"</span> no direct.</h1>
<div style="margin-top:70px;display:grid;gap:18px;font-size:32px;font-weight:600">
<div style="justify-self:start;background:#fff;border-radius:30px 30px 30px 8px;padding:22px 30px;color:{INK};box-shadow:0 8px 24px rgba(14,19,40,.08)">Quanto tá o 15 Pro?</div>
<div style="justify-self:start;background:#fff;border-radius:30px 30px 30px 8px;padding:22px 30px;color:{INK};box-shadow:0 8px 24px rgba(14,19,40,.08)">E parcela em quantas vezes?</div>
<div style="justify-self:start;background:#fff;border-radius:30px 30px 30px 8px;padding:22px 30px;color:{INK};box-shadow:0 8px 24px rgba(14,19,40,.08)">Tem outra cor?? 👀</div>
<div style="justify-self:end;background:{BLUE};border-radius:30px 30px 8px 30px;padding:26px 32px;color:#fff;max-width:760px;font-weight:700">Olá! Quero finalizar meu pedido:<br>• 1x iPhone 15 Pro 128 GB — R$ 3.590<br>Pagamento: 12x no cartão</div></div>
<p style="color:{MUTE};font-size:32px;line-height:1.4;margin-top:50px;font-weight:600;max-width:880px">Com o site, o cliente já vê preço, parcelas e cores, e o pedido chega pronto no seu WhatsApp.</p></div>
{foot(INK)}</div>'''))

ARTES["posts/06-produto"] = (W, H, post_phone(INK, "#fff", "Catálogo", "Cada produto com foto, preço e parcelas.", "O cliente escolhe versão e cor, e cada produto tem link próprio para compartilhar.", "print-loja.png"))
ARTES["posts/05-simulador"] = (W, H, post_phone(BLUE, "#fff", "Simulador", "Ele vê quanto cabe no bolso antes de perguntar.", "Entrada, usado na troca e parcelas em até 24x, calculadas na hora.", "print-sim.png"))
ARTES["posts/04-produto-ideal"] = (W, H, post_phone(ICE, INK, "Diferencial", "O site ajuda o cliente indeciso a escolher.", "Um teste de 30 segundos recomenda os produtos certos do seu estoque.", "print-quiz.png", AMBER, MUTE))

ARTES["posts/03-sem-comissao"] = (W, H, page(W, H, f'''<div style="position:relative;width:{W}px;height:{H}px;background:{INK};overflow:hidden">
<div style="position:absolute;left:90px;top:100px;right:90px">
<span class="pill" style="background:{AMBER};color:{INK}">Para lanchonetes</span>
<h1 style="color:#fff;font-size:74px;margin-top:40px">Seu cardápio com pedido no WhatsApp. <span style="color:{AMBER}">Sem comissão.</span></h1>
<div style="margin-top:70px;display:grid;grid-template-columns:1fr 1fr;gap:22px">
<div style="background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.12);border-radius:30px;padding:36px"><p style="color:#9AA6C8;font-size:28px;font-weight:700">Pedido de R$ 80 no app</p><p style="color:#FF7A6B;font-family:Unbounded,Arial Black,sans-serif;font-weight:800;font-size:64px;margin-top:14px">−R$ 21</p><p style="color:#9AA6C8;font-size:24px;margin-top:8px">com comissão de até 27%</p></div>
<div style="background:{BLUE};border-radius:30px;padding:36px"><p style="color:#DCE4FF;font-size:28px;font-weight:700">No seu site</p><p style="color:#fff;font-family:Unbounded,Arial Black,sans-serif;font-weight:800;font-size:64px;margin-top:14px">R$ 0</p><p style="color:#DCE4FF;font-size:24px;margin-top:8px">de comissão por pedido</p></div></div>
<p style="color:#C9D1EA;font-size:32px;line-height:1.4;margin-top:50px;font-weight:600">Cardápio com fotos, adicionais e o pedido chegando pronto para você.</p></div>
{foot("#fff")}</div>'''))

def lista(itens, cor_n, cor_t):
    return "".join(f'<div style="display:flex;gap:28px;align-items:flex-start"><span style="flex:0 0 76px;height:76px;border-radius:22px;background:{cor_n};color:#fff;display:grid;place-items:center;font-family:Unbounded,Arial Black,sans-serif;font-weight:800;font-size:34px">{i+1}</span><p style="color:{cor_t};font-size:36px;font-weight:700;line-height:1.3;padding-top:12px">{t}</p></div>' for i, t in enumerate(itens))

ARTES["posts/02-como-funciona"] = (W, H, page(W, H, f'''<div style="position:relative;width:{W}px;height:{H}px;background:{ICE};overflow:hidden">
<div style="position:absolute;left:90px;top:100px;right:90px">
<span class="pill" style="background:{BLUE};color:#fff">Como funciona</span>
<h1 style="color:{INK};font-size:76px;margin-top:40px">Seu site pronto em até 3 dias.</h1>
<div style="margin-top:70px;display:grid;gap:40px">{lista(["Você manda as fotos e a lista de preços que já usa.","A gente monta o site com o nome e as cores da sua loja.","Você coloca o link na bio e no WhatsApp.","Mudou o preço? A gente atualiza para você."], BLUE, INK)}</div></div>
{foot(INK)}</div>'''))

ARTES["posts/01-cinco-motivos"] = (W, H, page(W, H, f'''<div style="position:relative;width:{W}px;height:{H}px;background:{BLUE};overflow:hidden">
<div style="position:absolute;left:90px;top:100px;right:90px">
<h1 style="color:#fff;font-size:72px">5 motivos para sua loja ter site próprio</h1>
<div style="margin-top:60px;display:grid;gap:34px">{lista(["Passa confiança em compras de valor alto.","O cliente vê o preço sem precisar perguntar.","Cada produto tem um link para postar e mandar.","O pedido chega pronto no seu WhatsApp.","Nenhuma comissão por venda."], INK, "#fff")}</div></div>
{foot("#fff")}</div>'''))

# ---------- Capas dos destaques ----------
ICONES = {
 "demo": '<rect x="34" y="14" width="32" height="72" rx="8" fill="none" stroke="#fff" stroke-width="6"/><circle cx="50" cy="76" r="3.5" fill="#fff"/>',
 "planos": '<rect x="16" y="26" width="68" height="48" rx="10" fill="none" stroke="#fff" stroke-width="6"/><path d="M16 42h68" stroke="#fff" stroke-width="6"/><path d="M28 60h18" stroke="#FFB84D" stroke-width="6" stroke-linecap="round"/>',
 "como-funciona": '<circle cx="50" cy="50" r="32" fill="none" stroke="#fff" stroke-width="6"/><path d="M50 32v20l12 8" stroke="#FFB84D" stroke-width="6" stroke-linecap="round" fill="none"/>',
 "clientes": '<path d="M50 18l9.4 19 21 3-15.2 14.8 3.6 20.9L50 65.8 31.2 75.7l3.6-20.9L19.6 40l21-3Z" fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="round"/>',
 "contato": '<path d="M50 16a33 33 0 0 0-28.6 49.5L17 83l18-4.6A33 33 0 1 0 50 16Z" fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="round"/><circle cx="38" cy="50" r="4" fill="#FFB84D"/><circle cx="50" cy="50" r="4" fill="#FFB84D"/><circle cx="62" cy="50" r="4" fill="#FFB84D"/>'
}
for nome, svg in ICONES.items():
    ARTES[f"destaques/{nome}"] = (1080, 1080, page(1080, 1080, f'<div style="width:1080px;height:1080px;background:{BLUE};display:grid;place-items:center"><svg width="520" height="520" viewBox="0 0 100 100">{svg}</svg></div>'))

# ---------- Stories (1080x1920) ----------
# Área segura: nada importante nos 250 px de cima (barra do Instagram) nem nos 340 px de baixo (campo de resposta).
SW, SH = 1080, 1920
def story(bg, fg, corpo, marca=True):
    topo = f'<div style="position:absolute;left:90px;top:270px;display:flex;align-items:center;gap:16px">{mark(58)}{wordmark(42, fg)}</div>' if marca else ""
    return page(SW, SH, f'<div style="position:relative;width:{SW}px;height:{SH}px;background:{bg};overflow:hidden">{topo}{corpo}</div>')

def story_phone(bg, fg, eyebrow, titulo, img, rodape, eyecor=AMBER):
    return story(bg, fg, f'''<div style="position:absolute;left:90px;right:90px;top:390px">
<span class="pill" style="background:{eyecor};color:{INK}">{eyebrow}</span>
<h1 style="color:{fg};font-size:68px;margin-top:30px">{titulo}</h1>
<p style="color:{fg};opacity:.85;font-size:40px;font-weight:700;margin-top:22px">{rodape}</p></div>
<div class="phone" style="left:250px;top:880px;width:580px;height:1180px"><img src="{b64(img)}"></div>''')

def story_texto(bg, fg, eyebrow, titulo, sub="", espaco="", eyecor=AMBER, subcor=None):
    return story(bg, fg, f'''<div style="position:absolute;left:90px;right:90px;top:430px">
<span class="pill" style="background:{eyecor};color:{INK}">{eyebrow}</span>
<h1 style="color:{fg};font-size:84px;margin-top:40px">{titulo}</h1>
{f'<p style="color:{subcor or fg};opacity:.85;font-size:40px;line-height:1.4;margin-top:34px;font-weight:600">{sub}</p>' if sub else ""}</div>{espaco}''')

ARTES["stories/terca-1-chegamos"] = (SW, SH, story(BLUE, "#fff", f'''
<div style="position:absolute;left:90px;right:90px;top:520px">
<p style="color:#fff;opacity:.85;font-size:44px;font-weight:700">Prazer, somos a</p>
<div style="margin-top:20px">{wordmark(190, "#fff")}</div>
<h1 style="color:#fff;font-size:72px;margin-top:70px">Criamos sites de vendas para lojas.</h1>
<p style="color:#fff;opacity:.88;font-size:42px;line-height:1.4;margin-top:34px;font-weight:600">Seu cliente vê o preço, as parcelas e manda o pedido pronto no seu WhatsApp.</p></div>''', marca=False))
ARTES["stories/terca-2-enquete"] = (SW, SH, story_texto(INK, "#fff", "Enquete", "Sua loja tem site próprio?", "Responde aqui embaixo 👇", ""))
ARTES["stories/terca-3-demo"] = (SW, SH, story_phone(BLUE, "#fff", "Demonstração", "Veja como fica uma loja feita pela Vitrio.", "print-home.png", "Toque no link para testar 👇"))
ARTES["stories/quarta-1-catalogo"] = (SW, SH, story_phone(INK, "#fff", "Bastidores", "Cada produto com foto, preço e parcelas.", "print-loja.png", "E um link para cada produto"))
ARTES["stories/quarta-2-perguntas"] = (SW, SH, story_texto(ICE, INK, "Caixa de perguntas", "Pergunte qualquer coisa sobre ter um site para a sua loja.", "Eu respondo todas aqui nos stories.", "", BLUE, MUTE).replace(f'background:{BLUE};color:{INK}">Caixa', f'background:{BLUE};color:#fff">Caixa'))
ARTES["stories/quarta-3-simulador"] = (SW, SH, story_phone(BLUE, "#fff", "Simulador", "Seu cliente simula as parcelas sozinho.", "print-sim.png", "Entrada, troca e até 24x"))
ARTES["stories/quinta-1-quiz"] = (SW, SH, story_texto(INK, "#fff", "Quiz", "Quanto o aplicativo de delivery pode cobrar por pedido?", "Responde no quiz 👇", ""))
ARTES["stories/quinta-2-resposta"] = (SW, SH, story(INK, "#fff", f'''<div style="position:absolute;left:90px;right:90px;top:430px">
<span class="pill" style="background:{AMBER};color:{INK}">Resposta</span>
<p style="color:{AMBER};font-family:Unbounded,Arial Black,sans-serif;font-weight:800;font-size:230px;line-height:1;margin-top:50px">27%</p>
<h1 style="color:#fff;font-size:64px;margin-top:30px">de comissão em alguns planos.</h1>
<p style="color:#C9D1EA;font-size:40px;line-height:1.4;margin-top:34px;font-weight:600">Com um cardápio próprio, o pedido chega no seu WhatsApp e a comissão é zero.</p></div>'''))
ARTES["stories/quinta-3-oferta"] = (SW, SH, story(INK, "#fff", f'''<div style="position:absolute;left:90px;right:90px;top:420px">
<span class="pill" style="background:{AMBER};color:{INK}">Lançamento</span>
<h1 style="color:#fff;font-size:76px;margin-top:40px">Só <span style="color:{AMBER}">3 vagas</span> com preço de lançamento.</h1>
<div style="margin-top:60px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.12);border-radius:36px;padding:44px">
<p style="color:#9AA6C8;font-size:32px;font-weight:700;text-decoration:line-through">De R$ 1.497</p>
<p style="color:#fff;font-family:Unbounded,Arial Black,sans-serif;font-weight:800;font-size:130px;line-height:1.05">R$ 497</p>
<p style="color:#fff;font-size:38px;font-weight:700;margin-top:10px">+ 1º mês de manutenção grátis</p></div>
<p style="color:#C9D1EA;font-size:40px;margin-top:50px;font-weight:600">Chame no WhatsApp:<br><b style="color:#fff;font-size:52px">{WHATS}</b></p></div>'''))
ARTES["stories/sexta-1-black-friday"] = (SW, SH, story(INK, "#fff", f'''<div style="position:absolute;left:90px;right:90px;top:520px">
<p style="color:{AMBER};font-family:Unbounded,Arial Black,sans-serif;font-weight:800;font-size:120px;line-height:1">BLACK<br>FRIDAY</p>
<h1 style="color:#fff;font-size:70px;margin-top:60px">Boas vendas hoje, lojistas!</h1>
<p style="color:#C9D1EA;font-size:42px;line-height:1.4;margin-top:34px;font-weight:600">Que o caixa encha e o estoque esvazie. 🖤</p></div>'''))
ARTES["stories/sexta-2-reflexao"] = (SW, SH, story_texto(BLUE, "#fff", "Para pensar", "Quantos clientes perguntaram o preço hoje e foram embora sem resposta?", "Com um site, o preço está lá 24 horas, até na loja fechada.", ""))
# Stories para os destaques
ARTES["stories/destaque-como-funciona"] = (SW, SH, story(ICE, INK, f'''<div style="position:absolute;left:90px;right:90px;top:430px">
<span class="pill" style="background:{BLUE};color:#fff">Como funciona</span>
<h1 style="color:{INK};font-size:78px;margin-top:40px">Seu site pronto em até 3 dias.</h1>
<div style="margin-top:70px;display:grid;gap:44px">{lista(["Você manda as fotos e a lista de preços.","A gente monta com o nome e as cores da sua loja.","Você coloca o link na bio e no WhatsApp.","Mudou o preço? A gente atualiza."], BLUE, INK)}</div></div>'''))
ARTES["stories/destaque-planos"] = (SW, SH, story(INK, "#fff", f'''<div style="position:absolute;left:90px;right:90px;top:420px">
<span class="pill" style="background:{AMBER};color:{INK}">Planos</span>
<div style="margin-top:44px;display:grid;gap:22px">
<div style="background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.12);border-radius:30px;padding:34px 38px"><p style="color:#fff;font-size:40px;font-weight:800">Essencial</p><p style="color:#fff;font-family:Unbounded,Arial Black,sans-serif;font-weight:800;font-size:54px;margin-top:8px">R$ 997 <span style="font-family:Manrope;font-size:28px;color:#9AA6C8">+ R$ 99/mês</span></p><p style="color:#C9D1EA;font-size:28px;margin-top:8px">Até 60 produtos · 1 atualização por semana</p></div>
<div style="background:{BLUE};border-radius:30px;padding:34px 38px"><p style="color:#fff;font-size:40px;font-weight:800">Completo</p><p style="color:#fff;font-family:Unbounded,Arial Black,sans-serif;font-weight:800;font-size:54px;margin-top:8px">R$ 1.497 <span style="font-family:Manrope;font-size:28px;color:#DCE4FF">+ R$ 149/mês</span></p><p style="color:#DCE4FF;font-size:28px;margin-top:8px">Produtos ilimitados · domínio próprio · atualizações sempre</p></div>
<div style="background:{AMBER};border-radius:30px;padding:34px 38px"><p style="color:{INK};font-size:40px;font-weight:800">Lançamento: 3 vagas</p><p style="color:{INK};font-family:Unbounded,Arial Black,sans-serif;font-weight:800;font-size:54px;margin-top:8px">R$ 497</p><p style="color:{INK};font-size:28px;margin-top:8px;font-weight:700">Plano Completo + 1º mês grátis</p></div></div>
<p style="color:#C9D1EA;font-size:32px;margin-top:40px;font-weight:600">A implantação pode ser parcelada em 3x.</p></div>'''))
ARTES["stories/destaque-contato"] = (SW, SH, story(BLUE, "#fff", f'''<div style="position:absolute;left:90px;right:90px;top:430px">
<span class="pill" style="background:{AMBER};color:{INK}">Contato</span>
<h1 style="color:#fff;font-size:80px;margin-top:40px">Vamos montar o site da sua loja?</h1>
<div style="margin-top:70px;display:grid;gap:30px;color:#fff;font-size:44px;font-weight:700">
<p>WhatsApp<br><b style="font-family:Unbounded,Arial Black,sans-serif;font-size:58px">{WHATS}</b></p>
<p>Instagram<br><b style="font-size:52px">{HANDLE}</b></p>
<p style="opacity:.85;font-size:36px;font-weight:600">Atendemos Curitiba e todo o Brasil.</p></div></div>'''))

# ---------- Render ----------
jobs = []
for nome, (w, h, html) in ARTES.items():
    caminho = os.path.join(OUT, nome + ".png"); os.makedirs(os.path.dirname(caminho), exist_ok=True)
    tmp = os.path.join(AQUI, "_tmp_" + nome.replace("/", "_") + ".html"); open(tmp, "w", encoding="utf-8").write(html)
    jobs.append({"html": tmp, "png": caminho, "w": w, "h": h, "transp": nome == "logo/simbolo"})
open(os.path.join(AQUI, "_jobs.json"), "w").write(json.dumps(jobs))
js = """const {chromium}=require('playwright');const jobs=require(process.argv[2]);(async()=>{const b=await chromium.launch();
for(const j of jobs){const p=await b.newPage({viewport:{width:j.w,height:j.h}});await p.goto('file://'+j.html,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:j.png,omitBackground:j.transp});await p.close()}await b.close()})();"""
open(os.path.join(AQUI, "_render.js"), "w").write(js)
subprocess.run(["node", os.path.join(AQUI, "_render.js"), os.path.join(AQUI, "_jobs.json")], check=True)
for j in jobs: os.remove(j["html"])
os.remove(os.path.join(AQUI, "_jobs.json")); os.remove(os.path.join(AQUI, "_render.js"))
print(len(jobs), "artes geradas")
