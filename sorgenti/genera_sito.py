#!/usr/bin/env python3
"""Genera il sito di IDQ Monitor User (index.html e privacy.html, in 5 lingue) nella cartella principale del repository.
Uso: python3 sorgenti/genera_sito.py   (i file da scaricare stanno in downloads/<versione>/ e downloads/idq-monitor-server.zip)"""
import os, sys, html, json
sys.path.insert(0, os.path.dirname(__file__))
from testi import T
from privacy_testi import PRIV
RADICE = os.path.join(os.path.dirname(__file__), "..")
LING = [("it", "Italiano"), ("en", "English"), ("fr", "Français"), ("de", "Deutsch"), ("es", "Español")]
VERSIONE = "1.1"
# Link di donazione (lasciare vuoto finche' non sono pronti: il pulsante mostra "a breve"). Esempi: "https://paypal.me/NOME", "https://revolut.me/NOME"
DONA = {"PayPal": "https://paypal.me/IDQdeveloper", "Revolut": "https://revolut.me/paolox0hv"}
# (chiave testo sistema, chiave nota, file, icona)
FILE = [   # (chiave etichetta, icona, file; None = popup "presto su Google Play")
 ("per_win", "win", f"downloads/{VERSIONE}/IDQ-Monitor-User-Setup-Windows.exe"),
 ("per_linux", "linux", f"downloads/{VERSIONE}/idq-monitor-user_{VERSIONE}_amd64.deb"),
 ("per_rpi", "rpi", f"downloads/{VERSIONE}/idq-monitor-user_{VERSIONE}_arm64.deb", "sub_rpi"),
 ("per_mac1", "mac", f"downloads/{VERSIONE}/IDQ-Monitor-User-macOS-arm64.zip"),
 ("per_mac2", "mac", f"downloads/{VERSIONE}/IDQ-Monitor-User-macOS-x64.zip"),
 ("per_android", "android", None),
 ("per_ios", "ios", f"downloads/{VERSIONE}/IDQ-Monitor-User-iOS-non-firmato.ipa"),
 ("per_srv", "srv", "downloads/idq-monitor-server.zip", "sub_srv"),
]
ICONE = {   # icone semplici disegnate a mano (nessuna risorsa esterna)
 "win": '<svg viewBox="0 0 48 48"><path d="M5 9l17-2.4V23H5zM25 6.2L43 3.5V23H25zM5 25h17v16.4L5 39zM25 25h18v19.6L25 42z"/></svg>',
 "linux": '<svg viewBox="0 0 48 48"><rect x="4" y="8" width="40" height="32" rx="5" fill="none" stroke="currentColor" stroke-width="3.5"/><path d="M12 19l8 5-8 5M24 31h12" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "rpi": '<svg viewBox="0 0 48 48"><circle cx="17" cy="27" r="7"/><circle cx="31" cy="27" r="7"/><circle cx="24" cy="35" r="7"/><circle cx="24" cy="21" r="7"/><path d="M24 14c-1-5-5-8-9-8 1 5 4 8 9 8zM24 14c1-5 5-8 9-8-1 5-4 8-9 8z"/></svg>',
 "mac": '<svg viewBox="0 0 48 48"><path d="M33 25c0-4 3-6 3-6-2-3-5-3-6-3-2 0-4 1-5 1s-3-1-5-1c-4 0-8 3-8 9 0 7 5 14 8 14 2 0 3-1 5-1s3 1 5 1c3 0 7-6 7-9 0 0-4-2-4-5zM29 12c1-1 2-3 2-5-2 0-4 1-5 3-1 1-2 3-2 5 2 0 4-1 5-3z"/></svg>',
 "android": '<svg viewBox="0 0 48 48"><path d="M9 32a15 15 0 0130 0zM15 10l3 5M33 10l-3 5" fill="currentColor" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><circle cx="19" cy="25" r="1.8" fill="#fff"/><circle cx="29" cy="25" r="1.8" fill="#fff"/></svg>',
 "ios": '<svg viewBox="0 0 48 48"><rect x="13" y="3" width="22" height="42" rx="5" fill="none" stroke="currentColor" stroke-width="3.5"/><rect x="20" y="7" width="8" height="2.5" rx="1.2"/><circle cx="24" cy="39.5" r="2"/></svg>',
 "srv": '<svg viewBox="0 0 48 48"><rect x="6" y="6" width="36" height="13" rx="3"/><rect x="6" y="24" width="36" height="13" rx="3"/><circle cx="13" cy="12.5" r="2" fill="#fff"/><circle cx="13" cy="30.5" r="2" fill="#fff"/><path d="M24 37v6M16 43h16" stroke="currentColor" stroke-width="3" fill="none"/></svg>',
}
def L(chiave, tag="span"):
    return "".join('<%s class="l" data-l="%s">%s</%s>' % (tag, l, T[chiave][i], tag) for i, (l, _) in enumerate(LING))
def mb(percorso):
    try: n = os.path.getsize(os.path.join(RADICE, percorso))
    except OSError: return ""
    return ("%.1f MB" % (n / 1048576)) if n >= 1048576 else ("%d KB" % max(1, n // 1024))

CSS = """
:root{--bg:#fff;--tx:#17212b;--mu:#5b6b7a;--ac:#1d5fa8;--card:#f1f5f9;--bd:#d9e0ea;--hero:#0f1720;--ok:#177a45}
@media (prefers-color-scheme:dark){:root{--bg:#0f1720;--tx:#e8eef5;--mu:#8aa0b5;--ac:#6fa8dc;--card:#18232f;--bd:#26364a;--hero:#0a1118;--ok:#3ddc84}}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--tx);font:17px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--ac)}
header.top{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding:12px 20px;border-bottom:1px solid var(--bd)}
header.top .brand{display:flex;align-items:center;gap:10px;font-weight:700;text-decoration:none;color:var(--tx)}header.top img{width:36px;height:36px;border-radius:9px}
.lingue button{border:1px solid var(--bd);background:var(--card);color:var(--tx);border-radius:999px;padding:6px 12px;margin:2px;cursor:pointer;font:inherit;font-size:14px}.lingue button.on{background:var(--ac);color:#fff;border-color:var(--ac)}
main{max-width:980px;margin:0 auto;padding:0 20px 60px}
.hero{background:var(--hero);color:#fff;padding:56px 20px 48px;text-align:center}.hero img{width:120px;height:120px;border-radius:28px;box-shadow:0 8px 30px rgba(0,0,0,.4)}
.hero h1{font-size:clamp(30px,6vw,46px);margin:18px 0 8px}.hero p{max-width:660px;margin:0 auto;color:#cfd8ee;font-size:19px}
.cta{display:inline-block;margin:22px 8px 0;background:#1d5fa8;color:#fff;border-radius:999px;padding:12px 26px;font-weight:600;text-decoration:none}.cta.alt{background:transparent;border:2px solid #6fa8dc;color:#cfe3ff}
h2{margin:46px 0 14px;font-size:26px}h3{margin:18px 0 6px;font-size:18px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:16px 18px}.card b{display:block;margin-bottom:4px}
.shot{text-align:center}.shot img{max-width:100%;width:380px;border-radius:14px;border:1px solid var(--bd)}.shot small,.mu{color:var(--mu)}
table.dl{width:100%;border-collapse:separate;border-spacing:0 10px}table.dl td{background:var(--card);padding:12px 14px;vertical-align:middle}table.dl td:first-child{border-radius:14px 0 0 14px;width:56px;font-size:26px;text-align:center}table.dl td:last-child{border-radius:0 14px 14px 0;text-align:right;white-space:nowrap}
table.dl .nome{font-weight:700}table.dl .nota{color:var(--mu);font-size:14px;line-height:1.4}
.os-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin:14px 0}.os{display:flex;flex-direction:column;align-items:center;gap:6px;background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:20px 10px;text-decoration:none;color:var(--tx);text-align:center}.os:hover{border-color:var(--ac)}.os svg{width:56px;height:56px;fill:currentColor;color:var(--ac)}.os .et{font-weight:700;font-size:15px}.os small{color:var(--mu)}.os .sub{font-size:12px;line-height:1.3}
.pop{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);align-items:center;justify-content:center;z-index:9;padding:16px}.pop.on{display:flex}.pop .box{background:var(--bg);border-radius:16px;padding:22px;max-width:360px;text-align:center}.pop button{background:var(--ac);color:#fff;border:0;border-radius:10px;padding:9px 22px;font-size:16px;cursor:pointer}
.btn{display:inline-block;background:var(--ac);color:#fff;border-radius:10px;padding:9px 16px;text-decoration:none;font-weight:600}.btn small{opacity:.85;font-weight:400}
@media(max-width:640px){table.dl td:last-child{display:block;text-align:left;border-radius:0 0 14px 14px}table.dl td:nth-child(2){border-radius:0 14px 0 0}table.dl td:first-child{border-radius:14px 0 0 0;display:inline-block}table.dl tr{display:block}}
.dona{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:20px;text-align:center}.dona a{display:inline-block;margin:4px 6px;background:#e8465a;color:#fff;border-radius:999px;padding:11px 26px;font-weight:700;text-decoration:none}#dmsg{margin-top:10px;color:var(--ok);min-height:1.4em}
footer{border-top:1px solid var(--bd);padding:24px 20px;text-align:center;color:var(--mu);font-size:15px}
.l{display:none}html[data-l=it] .l[data-l=it],html[data-l=en] .l[data-l=en],html[data-l=fr] .l[data-l=fr],html[data-l=de] .l[data-l=de],html[data-l=es] .l[data-l=es]{display:inline}
html[data-l=it] div.l[data-l=it],html[data-l=en] div.l[data-l=en],html[data-l=fr] div.l[data-l=fr],html[data-l=de] div.l[data-l=de],html[data-l=es] div.l[data-l=es]{display:block}
.policy h1{margin-top:34px}.policy h2{font-size:21px;margin-top:30px}.upd{color:var(--mu);font-size:15px}
"""
JS = """(function(){var ok=["it","en","fr","de","es"],q=(location.search.match(/[?&]l=([a-z]{2})/)||[])[1],s=null;try{s=localStorage.getItem("l")}catch(e){}
var l=q||s||(navigator.language||"it").slice(0,2).toLowerCase();if(ok.indexOf(l)<0)l="en";
function imposta(x){document.documentElement.setAttribute("data-l",x);document.documentElement.lang=x;document.querySelectorAll(".lingue button").forEach(function(b){b.classList.toggle("on",b.dataset.l==x)});try{localStorage.setItem("l",x)}catch(e){}
var t=document.querySelector("title");var k=t&&t.dataset["t"+x];if(k)document.title=k;document.querySelectorAll("a[data-g]").forEach(function(a){a.href=a.dataset.g+"?l="+x})}
document.querySelectorAll(".lingue button").forEach(function(b){b.onclick=function(){imposta(b.dataset.l)}});imposta(l);
var pa=document.getElementById("os-android"),pp=document.getElementById("pop");if(pa){pa.onclick=function(e){e.preventDefault();pp.classList.add("on")};document.getElementById("pop-ok").onclick=function(){pp.classList.remove("on")};pp.onclick=function(e){if(e.target===pp)pp.classList.remove("on")}}
document.querySelectorAll(".dona a").forEach(function(d){if(d.getAttribute("href")!=="#")return;d.onclick=function(e){e.preventDefault();var m={it:%s,en:%s,fr:%s,de:%s,es:%s};document.getElementById("dmsg").textContent=m[document.documentElement.lang]||m.en}})})();"""
def testa(titolo_chiave, extra=""):
    titoli = " ".join('data-t%s="%s"' % (l, html.escape(T[titolo_chiave][i])) for i, (l, _) in enumerate(LING))
    return """<!doctype html><html lang="it" data-l="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title %s>%s</title><meta name="description" content="%s"><link rel="icon" href="icona.png"><link rel="apple-touch-icon" href="icona.png">
<style>%s</style></head><body>
<header class="top"><a class="brand" href="index.html"><img src="icona.png" alt=""><span>IDQ Monitor User</span></a><div class="lingue">%s</div></header>
""" % (titoli, html.escape(T[titolo_chiave][0]), html.escape(T["descr"][0]), CSS, "".join('<button data-l="%s">%s</button>' % (l, n) for l, n in LING))
def fine():
    dm = [json.dumps(T["m_dona"][i], ensure_ascii=False) for i in range(5)]
    return """<footer><div>© IDQ Developer · %s · <a href="mailto:info.idq.26@gmail.com">info.idq.26@gmail.com</a></div><div style="margin-top:6px"><a href="index.html">%s</a> · <a data-g="guida.html" href="guida.html">%s</a> · <a data-g="privacy.html" href="privacy.html">%s</a></div></footer>
<script>%s</script></body></html>""" % (L("footer"), L("home"), L("guida"), L("privacy"), JS % tuple(dm))

def indice():
    h = testa("titolo")
    h += '<section class="hero"><img src="icona.png" alt=""><h1>IDQ Monitor User</h1><p>%s</p><a class="cta" href="#download">%s</a><a class="cta alt" href="#prova">%s</a></section><main>' % (L("hero_p"), L("cta_scarica"), L("cta_prova"))
    h += "<h2>%s</h2><div class=\"grid\">" % L("h_funzioni")
    for n in range(1, 7): h += '<div class="card"><b>%s</b>%s</div>' % (L("f%dt" % n), L("f%d" % n))
    h += "</div>"
    h += '<h2>%s</h2><div class="shot">%s<br><small>%s</small></div>' % (L("h_screen"), "".join('<img class="l" data-l="%s" src="img/app-%s.jpg" alt="IDQ Monitor User">' % (l, l) for l, _ in LING), L("screen_n"))
    h += '<h2 id="download">%s</h2><p class="mu">%s · %s %s</p>' % (L("h_download"), L("d_intro"), L("d_versione"), VERSIONE)
    h += '<div class="os-grid">'
    for voce in FILE:
        chiave, icona, percorso = voce[:3]; sub = ('<small class="sub">%s</small>' % L(voce[3])) if len(voce) > 3 else ''
        if percorso is None: h += '<a class="os" href="#" id="os-android">%s<span class="et">%s</span><small>Google Play</small></a>' % (ICONE[icona], L(chiave))
        else: h += '<a class="os" href="%s" download="%s">%s<span class="et">%s</span>%s<small>%s</small></a>' % (percorso, os.path.basename(percorso), ICONE[icona], L(chiave), sub, mb(percorso))
    h += '</div><details class="note"><summary>%s</summary>%s</details>' % (L("note_inst"), "".join('<p><b>%s</b>: %s</p>' % (L(c), L(n)) for c, n in (("per_win", "n_win"), ("per_linux", "n_deb"), ("per_rpi", "n_rpi"), ("per_mac1", "n_mac"), ("per_ios", "n_ios"), ("per_srv", "n_srv"))))
    h += '<div class="pop" id="pop"><div class="box"><b>%s</b><p>%s</p><button id="pop-ok" type="button">%s</button></div></div>' % (L("pop_t"), L("pop_m"), L("pop_ok"))
    h += '<h2 id="prova">%s</h2><p>%s</p><h2>%s</h2><p>%s</p><p><a class="btn" data-g="guida.html" href="guida.html">%s</a></p>' % (L("h_prova"), L("p_prova"), L("h_server"), L("p_server"), L("cta_guida"))
    bt = "".join('<a id="dona-%s" href="%s"%s>%s</a> ' % (n.lower(), html.escape(u) if u else "#", ' target="_blank" rel="noopener"' if u else "", n) for n, u in DONA.items())
    h += '<h2 id="dona">%s</h2><div class="dona"><p>%s</p><p><b>%s</b></p>%s<div id="dmsg"></div></div>' % (L("h_dona"), L("p_dona"), L("b_dona"), bt)
    return h + "</main>" + fine()

def privacy():
    h = testa("privacy") + '<main class="policy">'
    for l, _ in LING:
        t, agg, sez = PRIV[l]
        h += '<div class="l" data-l="%s"><h1>%s</h1><p class="upd">%s</p>' % (l, html.escape(t), html.escape(agg))
        for n, (tit, corpo) in enumerate(sez): h += "<h2>%s</h2>%s" % (html.escape(tit), corpo)
        h += "</div>"
    return h + "</main>" + fine()

if __name__ == "__main__":
    open(os.path.join(RADICE, "index.html"), "w").write(indice())
    open(os.path.join(RADICE, "privacy.html"), "w").write(privacy())
    print("index.html e privacy.html generati")
