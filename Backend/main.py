from fastapi import FastAPI
from router import event_router
from router import auth_router
app = FastAPI()


@app.get("/")
def home():
    return {"message": "Fastapi is running!"}

app.include_router(event_router.router)
app.include_router(auth_router.router)

