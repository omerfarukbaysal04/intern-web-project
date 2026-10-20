from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from app.data.posts import POSTS
import html
from app.config import SAFE_MODE
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi import Form
from fastapi.responses import RedirectResponse
from app.data.users import USERS
from app.data.comments import yorumlar, yorum_ekle


templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent/"templates"))
app = FastAPI()

def kullanici_oturum(request: Request):
     kullanici=request.cookies.get("oturum")
     if kullanici and kullanici in USERS:
          return kullanici
     return None

@app.get("/api/posts")
def get_posts():
    return {"items" : POSTS}

@app.get("/api/posts/{slug}")
def get_post(slug: str):
    for post in POSTS:
        if post["slug"]==slug:
            return post
    raise HTTPException(status_code=404, detail="Yazı bulunamadı")

@app.get("/search", response_class=HTMLResponse)
def search_page(request: Request, q: str=""):
    goster = html.escape(q) if SAFE_MODE else q
    saldiri_var = ("<" in q) and (not SAFE_MODE)
    sonuclar = [p for p in POSTS if q.lower() in (p["title"] + p["excerpt"] + p["category"]).lower()]
    return templates.TemplateResponse("search.html", {
        "request": request,
        "goster": goster,
        "saldiri": saldiri_var,
        "sonuclar": sonuclar
    })
    
@app.get("/hesap", response_class=HTMLResponse)
def hesap(request: Request):
    kullanici=kullanici_oturum(request)
    if not kullanici:
         return RedirectResponse(url="/giris",status_code=303)
    resp = templates.TemplateResponse("hesap.html",{
        "request":request,
        "kullanici": kullanici,
        "user": USERS[kullanici],
        })
    if SAFE_MODE:
        resp.headers["X-Frame-Options"]="DENY"
    return resp

@app.get("/giris",response_class=HTMLResponse)
def giris(request : Request):
    return templates.TemplateResponse("giris.html",{"request": request})

@app.post("/giris")
def giris_yap(request: Request, kullanici: str=Form(),parola: str=Form()):
    u = USERS.get(kullanici)
    if u and u["parola"]==parola:
        resp=RedirectResponse(url="/hesap",status_code=303)
        resp.set_cookie("oturum",kullanici)
        return resp
    return templates.TemplateResponse(
        "giris.html",
        {"request": request,"hata":"Kullanıcı adı veya parola hatalı"},
    )

@app.post("/hesap/email")
def email_guncelle(request:Request, email:str=Form()):
    kullanici=kullanici_oturum(request)
    if not kullanici:
        return RedirectResponse(url="/giris",status_code=303)
    USERS[kullanici]["email"]=email
    return RedirectResponse(url="/hesap",status_code=303)

@app.post("/hesap/sil")
def hesap_sil(request:Request):
    kullanici=kullanici_oturum(request)
    if not kullanici:
        return RedirectResponse(url="/giris",status_code=303)
    USERS.pop(kullanici,None) #kullanıcıyı sil
    resp = templates.TemplateResponse("silindi.html", {"request":request})
    resp.delete_cookie("oturum")
    return resp

@app.get("/cikis")
def cikis():
    resp = RedirectResponse(url="/", status_code=303)
    resp.delete_cookie("oturum")
    return resp

@app.get("/saldirgan", response_class=HTMLResponse)
def saldirgan(request:Request):
    return templates.TemplateResponse("saldirgan.html", {"request":request})

@app.get("/clickjack-ders", response_class=HTMLResponse)
def clickjack_ders(request:Request):
    return templates.TemplateResponse("clickjack_ders.html",{"request":request})

@app.get("/csrf-saldirgan", response_class=HTMLResponse)
def csrf_saldirgan(request: Request):
    return templates.TemplateResponse("csrf_saldirgan.html",{"request":request})

@app.get("/api/yorumlar/{slug}")
def get_yorumlar(slug:str):
    items = yorumlar(slug)
    if SAFE_MODE:
        items = [{**c, "metin": html.escape(c["metin"])} for c in items]
    return {"items":items}

@app.post("/api/yorum")
def post_yorum(request: Request, slug: str = Form(), metin: str = Form(), resim: str = Form(default="")):
    yazar= kullanici_oturum(request) or "anonim"
    yorum_ekle(slug,yazar,metin,resim)
    return {"ok":True}

@app.get("/hesap/email-degistir")
def email_degistir_get(request:Request, email: str=""):
    kullanici= kullanici_oturum(request)
    if not kullanici:
        return RedirectResponse(url="/giris",status_code=303)
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
