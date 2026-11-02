from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from app.data.posts import POSTS, KATEGORILER, kategoriye_gore, kategori_adi
import html
import re
import secrets
from app.config import SAFE_MODE
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi import Form
from fastapi.responses import RedirectResponse
from app.data.users import USERS
from app.data.comments import yorumlar, yorum_ekle
from app.sanitize import temizle


KOK = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(KOK/"templates"))
app = FastAPI()

# Sunucu-render'li sayfalarin ortak stili (bkz. static/ortak.css).
# Vite bu yolu da :8000'e proxy'liyor, yani tarayici icin tek origin.
app.mount("/static", StaticFiles(directory=str(KOK/"static")), name="static")

def kullanici_oturum(request: Request):
     kullanici=request.cookies.get("oturum")
     if kullanici and kullanici in USERS:
          return kullanici
     return None


# --- CSRF TOKEN (SAFE_MODE savunmasi) -----------------------------------
# Token kullanici kaydinda (sunucuda) tutulur; forma gizli alan olarak basilir.
# Saldirgan baska bir sayfadan form gonderebilir ama bu degeri OKUYAMAZ
# (same-origin policy), bu yuzden dogrulama patlar.
def csrf_token_al(kullanici: str) -> str:
     """Kullanicinin CSRF token'ini dondurur; yoksa uretir."""
     u = USERS.get(kullanici)
     if not u:
          return ""
     if not u.get("csrf_token"):
          u["csrf_token"] = secrets.token_urlsafe(32)
     return u["csrf_token"]


def csrf_gecerli(kullanici: str, token: str) -> bool:
     """SAFE_MODE kapaliyken dogrulama yapilmaz (zafiyet bilerek acik)."""
     if not SAFE_MODE:
          return True
     beklenen = USERS.get(kullanici, {}).get("csrf_token") or ""
     return bool(token) and secrets.compare_digest(token, beklenen)


def csrf_engellendi(request: Request, islem: str):
     """Token dogrulamasi basarisiz: islemi yapmadan farkindalik sayfasi don."""
     return templates.TemplateResponse(
          request,
          "csrf_engellendi.html",
          {"islem": islem},
          status_code=403,
     )

@app.get("/api/posts")
def get_posts(kategori: str = ""):
    # kategori verilirse o kategorinin yazilari, verilmezse hepsi (Gundem)
    items = kategoriye_gore(kategori) if kategori else POSTS
    return {"items" : items}


@app.get("/api/kategoriler")
def get_kategoriler():
    return {"items": KATEGORILER}


@app.get("/api/kategori/{kategori_slug}")
def get_kategori(kategori_slug: str):
    ad = kategori_adi(kategori_slug)
    if ad is None:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    return {"slug": kategori_slug, "ad": ad, "items": kategoriye_gore(kategori_slug)}

@app.get("/api/posts/{slug}")
def get_post(slug: str):
    for post in POSTS:
        if post["slug"]==slug:
            return post
    raise HTTPException(status_code=404, detail="Yazı bulunamadı")

# Arama girdisinde GERCEKTEN calisabilir bir payload var mi?
# Ilk surumde sadece "<" aranıyordu; bu, zararsiz bir "2 < 3" aramasinda da
# "hacklendin" ekranini aciyordu. Artik calistirilabilir kaliplari ariyoruz.
XSS_KALIP = re.compile(
    # 1) kod calistirmakta kullanilan etiketler
    r"<\s*(script|img|svg|iframe|body|video|audio|object|embed|details)\b"
    # 2) herhangi bir etiket + olay niteligi (onerror=, onload=, onclick=...)
    r"|<\s*[a-z][a-z0-9]*[^>]*\son[a-z]+\s*="
    # 3) javascript: semasi
    r"|javascript\s*:",
    re.IGNORECASE,
)


@app.get("/search", response_class=HTMLResponse)
def search_page(request: Request, q: str=""):
    goster = html.escape(q) if SAFE_MODE else q
    saldiri_var = bool(XSS_KALIP.search(q)) and (not SAFE_MODE)
    sonuclar = [p for p in POSTS if q.lower() in (p["title"] + p["excerpt"] + p["category"]).lower()]
    return templates.TemplateResponse(request, "search.html", {
        "goster": goster,
        "saldiri": saldiri_var,
        "sonuclar": sonuclar
    })
    
@app.get("/hesap", response_class=HTMLResponse)
def hesap(request: Request):
    kullanici=kullanici_oturum(request)
    if not kullanici:
         return RedirectResponse(url="/giris",status_code=303)
    resp = templates.TemplateResponse(request, "hesap.html",{
        "kullanici": kullanici,
        "user": USERS[kullanici],
        "csrf_token": csrf_token_al(kullanici) if SAFE_MODE else "",
        })
    if SAFE_MODE:
        # CLICKJACKING SAVUNMASI: sayfa hicbir iframe'e girmesin.
        # X-Frame-Options eski tarayicilar icin, frame-ancestors modern karsiligi.
        resp.headers["X-Frame-Options"]="DENY"
        resp.headers["Content-Security-Policy"]="frame-ancestors 'none'"
    return resp

@app.get("/giris",response_class=HTMLResponse)
def giris(request : Request):
    return templates.TemplateResponse(request, "giris.html")

@app.post("/giris")
def giris_yap(request: Request, kullanici: str=Form(),parola: str=Form()):
    u = USERS.get(kullanici)
    if u and u["parola"]==parola:
        resp=RedirectResponse(url="/hesap",status_code=303)
        # DIKKAT (demo): cerez bilerek imzasiz ve httponly DEGIL -- XSS ile
        # calinabildigini gosterebilmek icin. samesite="lax" ise tarayicinin
        # varsayilanini acikca yaziyor: saldirgan sayfalari bu demoda ayni
        # origin'de barindirmak zorunda olmamizin nedeni de bu (bkz. README).
        resp.set_cookie("oturum",kullanici,samesite="lax")
        csrf_token_al(kullanici)   # oturumla birlikte token da hazirlanir
        return resp
    return templates.TemplateResponse(
        request,
        "giris.html",
        {"hata":"Kullanıcı adı veya parola hatalı"},
    )

@app.post("/hesap/email")
def email_guncelle(request:Request, email:str=Form(), csrf_token:str=Form(default="")):
    kullanici=kullanici_oturum(request)
    if not kullanici:
        return RedirectResponse(url="/giris",status_code=303)
    if not csrf_gecerli(kullanici, csrf_token):
        return csrf_engellendi(request, "e-posta degistirme")
    USERS[kullanici]["email"]=email
    return RedirectResponse(url="/hesap",status_code=303)

@app.post("/hesap/sil")
def hesap_sil(request:Request, csrf_token:str=Form(default="")):
    kullanici=kullanici_oturum(request)
    if not kullanici:
        return RedirectResponse(url="/giris",status_code=303)
    if not csrf_gecerli(kullanici, csrf_token):
        return csrf_engellendi(request, "hesap silme")
    USERS.pop(kullanici,None) #kullanıcıyı sil
    resp = templates.TemplateResponse(request, "silindi.html")
    resp.delete_cookie("oturum")
    return resp

@app.get("/cikis")
def cikis():
    resp = RedirectResponse(url="/", status_code=303)
    resp.delete_cookie("oturum")
    return resp

@app.get("/saldirgan", response_class=HTMLResponse)
def saldirgan(request:Request):
    return templates.TemplateResponse(request, "saldirgan.html")

@app.get("/clickjack-ders", response_class=HTMLResponse)
def clickjack_ders(request:Request):
    return templates.TemplateResponse(request, "clickjack_ders.html")

@app.get("/csrf-saldirgan", response_class=HTMLResponse)
def csrf_saldirgan(request: Request):
    return templates.TemplateResponse(request, "csrf_saldirgan.html")

@app.get("/api/yorumlar/{slug}")
def get_yorumlar(slug:str):
    items = yorumlar(slug)
    if SAFE_MODE:
        # STORED XSS SAVUNMASI: yorumu bastan sona escape etmek yerine beyaz-liste
        # ile temizliyoruz (bkz. sanitize.py). Boylece <img onerror> dusuyor ama
        # <a> linkleri kaliyor -- open redirect / tabnabbing / DOM XSS tuzaklari
        # da kendi savunmalariyla karsilasiyor, "gizlenerek" sonmuyorlar.
        items = [{**c, "metin": temizle(c["metin"])} for c in items]
    return {"items":items}

@app.post("/api/yorum")
def post_yorum(request: Request, slug: str = Form(), metin: str = Form(), resim: str = Form(default="")):
    yazar= kullanici_oturum(request) or "anonim"
    yorum_ekle(slug,yazar,metin,resim)
    return {"ok":True}

# --- CSRF: durumu GET ile degistiren zafiyetli endpoint ---
# Yorumdaki sahte "resim" URL'si tam burayi cagiriyor.
@app.get("/hesap/email-degistir")
def email_degistir_get(request:Request, email: str=""):
    kullanici= kullanici_oturum(request)
    if not kullanici:
        return RedirectResponse(url="/giris",status_code=303)
    if SAFE_MODE:
        # CSRF SAVUNMASI (1): GET guvenli bir metottur, durum degistirmemeli.
        # Tarayici <img src> gibi istekleri kullanicinin onayi olmadan atar;
        # bu yuzden boyle bir islem GET ile hic sunulmamali.
        return {"ok": False, "neden": "GET ile durum degistirilemez (CSRF savunmasi)"}
    if email:
        USERS[kullanici]["email"] = email
        USERS[kullanici]["csrf_uyari"] = True
    return {"ok":True}

@app.get("/api/csrf-uyari")
def csrf_uyari(request: Request):
    kullanici = kullanici_oturum(request)
    uyari = bool(kullanici and USERS.get(kullanici, {}).get("csrf_uyari"))
    if uyari:
        USERS[kullanici]["csrf_uyari"] = False   # bir kez göster, sonra temizle
    return {"uyari": uyari}


# --- OPEN REDIRECT ---
@app.get("/git")
def git(url: str = "/"):
    if SAFE_MODE:
        # savunma: sadece site-ici (goreli) adreslere izin ver; dis adresi reddet
        if url.startswith("/") and not url.startswith("//"):
            return RedirectResponse(url=url, status_code=303)
        return RedirectResponse(url="/", status_code=303)
    # zafiyetli: ne verilirse oraya yonlendir (dis sitelere bile)
    return RedirectResponse(url=url, status_code=303)


@app.get("/sahte-giris", response_class=HTMLResponse)
def sahte_giris(request: Request):
    return templates.TemplateResponse(request, "sahte_giris.html")


# --- REVERSE TABNABBING ---
@app.get("/tab-saldirgan", response_class=HTMLResponse)
def tab_saldirgan(request: Request):
    return templates.TemplateResponse(request, "tab_saldirgan.html")


@app.get("/tab-sahte-giris", response_class=HTMLResponse)
def tab_sahte_giris(request: Request):
    return templates.TemplateResponse(request, "tab_sahte_giris.html")


# React'in SAFE_MODE durumunu ogrenebilmesi icin (DOM XSS savunmasi client tarafinda)
@app.get("/api/safe-mode")
def api_safe_mode():
    return {"safe_mode": SAFE_MODE}


# --- MALVERTISING: sahte odeme (phishing) sayfasi ---
@app.get("/premium-odeme", response_class=HTMLResponse)
def premium_odeme(request: Request):
    return templates.TemplateResponse(request, "sahte_odeme.html")
