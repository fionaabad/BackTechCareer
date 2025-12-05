from fastapi import FastAPI
from backend.api.v1.routes.auth_routes import router as auth_router


print("esta ejecutandose")
app = FastAPI(title="TechCareer API")

app.include_router(auth_router)