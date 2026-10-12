from fastapi import FastAPI
from app.data.posts import POSTS

app = FastAPI()

@app.get("/api/health")
def check_backend():
    return {"status" : "ok"}

@app.get("/api/posts")
def get_posts():
    return {"items" : POSTS}
