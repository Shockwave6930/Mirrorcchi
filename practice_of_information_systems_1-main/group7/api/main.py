from fastapi import FastAPI
from api.routers import user, history


app = FastAPI()
app.include_router(user.router)
app.include_router(history.router)