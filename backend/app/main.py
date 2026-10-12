from fastapi import FastAPI, HTTPException
from app.data.posts import POSTS

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

@app.get("/api/search")
def search(q: str= ""):
    results=[]
    for post in POSTS:
        if q.lower() in post["title"].lower():
            results.append(post)
    return {"items": results}
    
