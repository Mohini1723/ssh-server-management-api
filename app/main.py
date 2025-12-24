from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.servers import router as servers_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(servers_router)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Auth with MongoDB"}
