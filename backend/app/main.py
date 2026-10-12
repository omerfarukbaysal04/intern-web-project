from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
def check_backend():
    return {"status" : "ok"}


