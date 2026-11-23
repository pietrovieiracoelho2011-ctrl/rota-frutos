#!/usr/bin/env python3
"""Publica uma loja gerada (sites/<slug>) como Worker na Cloudflare.

Uso:  CLOUDFLARE_ACCOUNT_ID=... CLOUDFLARE_API_TOKEN=... python3 publicar.py <slug> [nome-do-worker]
O site fica em https://<nome-do-worker>.<seu-subdominio>.workers.dev
(um domínio próprio pode ser ligado depois no painel da Cloudflare).
"""
import base64, json, os, sys, uuid, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
API = "https://api.cloudflare.com/client/v4"


def req(method, path, body=None, ctype="application/json"):
    r = urllib.request.Request(API + path, data=body, method=method)
    r.add_header("Authorization", "Bearer " + os.environ.get("CLOUDFLARE_API_TOKEN", ""))
    if body is not None:
        r.add_header("Content-Type", ctype)
    with urllib.request.urlopen(r) as resp:
        return json.load(resp)


def publicar(slug, nome):
    conta = os.environ["CLOUDFLARE_ACCOUNT_ID"]
    pasta = os.path.join(AQUI, "sites", slug)
    html = open(os.path.join(pasta, "index.html"), encoding="utf-8").read()
    imgs = {}
    if os.path.isdir(os.path.join(pasta, "img")):
        for f in sorted(os.listdir(os.path.join(pasta, "img"))):
            imgs["/img/" + f] = base64.b64encode(open(os.path.join(pasta, "img", f), "rb").read()).decode()
    js = ("const HTML=" + json.dumps(html) + ";\nconst IMG=" + json.dumps(imgs) + ";\n"
          "export default{async fetch(req){const p=new URL(req.url).pathname;"
          "if(IMG[p]){const b=Uint8Array.from(atob(IMG[p]),c=>c.charCodeAt(0));"
          "return new Response(b,{headers:{'content-type':p.endsWith('.png')?'image/png':'image/jpeg','cache-control':'public, max-age=86400'}})}"
          "return new Response(HTML,{headers:{'content-type':'text/html; charset=utf-8','cache-control':'public, max-age=300'}})}};\n")
    meta = json.dumps({"main_module": "worker.js", "compatibility_date": "2025-01-01"})
    b = uuid.uuid4().hex
    corpo = (f'--{b}\r\nContent-Disposition: form-data; name="metadata"; filename="meta.json"\r\nContent-Type: application/json\r\n\r\n{meta}\r\n'
             f'--{b}\r\nContent-Disposition: form-data; name="worker.js"; filename="worker.js"\r\nContent-Type: application/javascript+module\r\n\r\n{js}\r\n--{b}--\r\n').encode()
    r = req("PUT", f"/accounts/{conta}/workers/scripts/{nome}", corpo, "multipart/form-data; boundary=" + b)
    if not r.get("success"):
        sys.exit(r)
    req("POST", f"/accounts/{conta}/workers/scripts/{nome}/subdomain", json.dumps({"enabled": True, "previews_enabled": False}).encode())
    sub = req("GET", f"/accounts/{conta}/workers/subdomain")["result"]["subdomain"]
    print(f"Publicado: https://{nome}.{sub}.workers.dev")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    publicar(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else sys.argv[1])
