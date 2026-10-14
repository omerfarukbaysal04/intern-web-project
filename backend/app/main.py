from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from app.data.posts import POSTS
import html
from app.config import SAFE_MODE


app = FastAPI()

@app.get("/api/posts")
def get_posts():
    return {"items" : POSTS}

@app.get("/api/posts/{slug}")
def get_post(slug: str):
    for post in POSTS:
        if post["slug"]==slug:
            return post
    raise HTTPException(status_code=404, detail="Yazı bulunamadı")

# --- Sunucu-render'li arama sayfasinin stili (duz string: CSS suslu parantezleri
SEARCH_STYLES = """
<style>
  :root{--bg:#0b1210;--panel:#121b16;--border:#212e26;--border-hover:#30463a;
    --text:#dce5e0;--muted:#8a9a91;--faint:#637469;--green:#3fa06b;--green-soft:#58b982;
    --green-deep:#1d6b45;--green-dim:#16281e;}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.6}
  .wrap{max-width:1040px;margin:0 auto;padding:0 24px}
  .top{border-bottom:1px solid var(--border);background:rgba(11,18,16,.88)}
  .top .inner{height:64px;display:flex;align-items:center;gap:20px}
  .logo{display:flex;align-items:center;gap:9px;font-weight:600;font-size:18px;color:var(--text);text-decoration:none}
  .logo .mark{width:11px;height:11px;border-radius:3px;background:var(--green)}
  .sform{margin-left:auto;position:relative}
  .sform input{background:var(--panel);border:1px solid var(--border);color:var(--text);
    border-radius:9px;padding:9px 12px 9px 34px;font-size:14px;width:260px;outline:none}
  .sform input:focus{border-color:var(--green-deep)}
  .sform .ic{position:absolute;left:11px;top:50%;transform:translateY(-50%);color:var(--faint)}
  h1.res{font-size:26px;font-weight:700;letter-spacing:-.02em;margin:40px 0 4px}
  h1.res .q{color:var(--green-soft)}
  .sub{color:var(--muted);font-size:14px;margin-bottom:26px}
  .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;padding-bottom:48px}
  @media(max-width:860px){.grid{grid-template-columns:repeat(2,1fr)}}
  @media(max-width:560px){.grid{grid-template-columns:1fr}}
  .card{background:var(--panel);border:1px solid var(--border);border-radius:14px;overflow:hidden;
    text-decoration:none;color:inherit;transition:border-color .15s,transform .15s;display:block}
  .card:hover{border-color:var(--border-hover);transform:translateY(-2px)}
  .thumb{height:96px;border-bottom:1px solid var(--border);display:flex;align-items:flex-end;padding:12px}
  .thumb.t1{background:#12231a}.thumb.t2{background:#141f12}.thumb.t3{background:#102021}
  .thumb.t4{background:#1d1711}.thumb.t5{background:#1a121c}.thumb.t6{background:#111526}
  .chip{font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:.06em;padding:4px 10px;
    border-radius:7px;background:var(--green-dim);color:var(--green-soft);border:1px solid var(--green-deep)}
  .cbody{padding:15px 16px}
  .cbody h3{font-size:16px;font-weight:600;line-height:1.3}
  .cbody p{margin-top:8px;color:var(--muted);font-size:13px}
  .meta{margin-top:13px;color:var(--faint);font-size:12px}
  .empty{color:var(--muted);padding:8px 0 48px}
  .xss-flash{position:fixed;inset:0;background:#ff1e1e;z-index:99998;pointer-events:none;opacity:0;animation:xssflash 1.3s ease-out forwards}
  @keyframes xssflash{0%{opacity:0}10%{opacity:.7}26%{opacity:.12}42%{opacity:.5}100%{opacity:0}}
  .xss-bg{position:fixed;inset:0;background:rgba(5,8,7,.85);z-index:99999;display:flex;align-items:center;justify-content:center;padding:20px;animation:xssfade .25s ease-out}
  @keyframes xssfade{from{opacity:0}to{opacity:1}}
  .xss-card{max-width:560px;width:100%;background:#121b16;border:1px solid #3a1414;border-top:4px solid #ff4d4d;border-radius:14px;padding:26px 30px}
  .xss-card h2{color:#ff6b6b;font-size:22px;margin:0 0 12px}
  .xss-card h3{color:#dce5e0;font-size:15px;margin:18px 0 6px}
  .xss-card p{color:#aab8b0;font-size:14px;margin:0}
  .xss-card b{color:#cdd8d1}
  .xss-card code{background:#0b1210;padding:2px 6px;border-radius:5px;color:#58b982;font-size:13px}
  .xss-card .close{margin-top:22px;background:#1d6b45;color:#eafff3;border:none;padding:10px 18px;border-radius:9px;font-size:14px;cursor:pointer}
  .xss-card .close:hover{background:#238a57}
</style>
"""


SEARCH_SCRIPT = """
<script>
window.caught = function () {
  if (window.__xss) return;
  window.__xss = true;
  var f = document.createElement("div");
  f.className = "xss-flash";
  document.body.appendChild(f);
  setTimeout(function () { f.remove(); }, 1300);
  setTimeout(function () {
    var bg = document.createElement("div");
    bg.className = "xss-bg";
    bg.innerHTML = `
      <div class="xss-card">
        <h2>&#9888; Az önce hacklendin!</h2>
        <p>Bu sayfada bir <b>Reflected XSS</b> açığı var ve sen de tetikledin.</p>
        <h3>Ne oldu?</h3>
        <p>Arama terimin (bu linkteki metin) sunucu tarafından hiç temizlenmeden sayfaya basıldı. İçindeki <code>&lt;script&gt;</code> kodu senin tarayıcında, bu sitenin adına çalıştı.</p>
        <h3>Gerçek bir saldırgan ne yapardı?</h3>
        <p>Oturum çerezini çalıp hesabına girebilir, senin adına işlem yapabilir ya da sahte bir giriş formu gösterip parolanı toplayabilirdi. Biz zarar vermek yerine sadece bu uyarıyı gösterdik.</p>
        <h3>Nasıl korunulur?</h3>
        <p>Kullanıcı girdisi ekrana basılmadan önce <b>escape</b> edilmeli (<code>&lt;</code> &rarr; <code>&amp;lt;</code>). React bunu otomatik yapar; sunucuda <code>html.escape()</code> ile yapılır. Bu sitede "güvenli mod" açıkken tam da bu devrededir.</p>
        <button class="close" onclick="this.closest('.xss-bg').remove()">Anladım, kapat</button>
      </div>`;
    document.body.appendChild(bg);
  }, 400);
};
</script>
"""


@app.get("/search", response_class=HTMLResponse)
def search_page(q: str = ""):

    goster = html.escape(q) if SAFE_MODE else q
    saldiri_var = ("<" in q) and  (not SAFE_MODE)
    uyari = "<script>caught()</script>" if saldiri_var else "" #saldırı varsa uyarı gönder, caught() ile
    sonuclar = [p for p in POSTS if q.lower() in (p["title"] + p["excerpt"] + p["category"]).lower()]
    if sonuclar:
        kartlar = "".join(
            f"""<a class="card" href="/post/{p["slug"]}">
              <div class="thumb {p["tone"]}"><span class="chip">{p["category"]}</span></div>
              <div class="cbody">
                <h3>{p["title"]}</h3>
                <p>{p["excerpt"]}</p>
                <div class="meta">{p["author"]} · {p["date"]} · {p["read_minutes"]} dk</div>
              </div>
            </a>"""
            for p in sonuclar
        )
    else:
        kartlar = '<p class="empty">Aramanıza uygun sonuç bulunamadı.</p>'

    return f"""<!doctype html>
<html lang="tr">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Arama · Teknopanorama</title>{SEARCH_STYLES}{SEARCH_SCRIPT}</head>
<body>
  <header class="top"><div class="wrap"><div class="inner">
    <a href="/" class="logo"><span class="mark"></span>Teknopanorama</a>
    <form class="sform" method="get" action="/search">
      <span class="ic">⌕</span>
      <input name="q" value="{goster}" placeholder="Haberlerde ara...">
    </form>
  </div></div></header>

  <div class="wrap">
    <h1 class="res">"<span class="q">{goster}</span>" için sonuçlar</h1>
    <div class="sub">{len(sonuclar)} sonuç bulundu</div>
    <div class="grid">{kartlar}</div>
  </div>
  {uyari}
</body>
</html>"""
    
