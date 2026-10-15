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


templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent/"templates"))
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
    kullanici=request.cookies.get("oturum")
    if not kullanici or kullanici not in USERS:
        return RedirectResponse(url="/giris",status_code=303)
    return templates.TemplateResponse("hesap.html",{
        "request":request,
        "kullanici": kullanici,
        "user": USERS[kullanici],
        })

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
    kullanici=request.cookies.get("oturum")
    if not kullanici or kullanici not in USERS:
            return RedirectResponse(url="/giris",status_code=303)
    USERS[kullanici]["email"]=email
    return RedirectResponse(url="/hesap",status_code=303)

@app.post("/hesap/sil")
def hesap_sil(request:Request):
    kullanici=request.cookies.get("oturum")
    if not kullanici or kullanici not in USERS:
            return RedirectResponse(url="/giris",status_code=303)
    USERS.pop(kullanici,None) #kullanıcıyı sil
    resp=RedirectResponse(url="/giris",status_code=303)
    resp.delete_cookie("oturum")
    return resp

    

