from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.routes.auth_routes import router as auth_router
from api.v1.routes.predict_routes import router as predict_router

app = FastAPI(title="TechCareer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(predict_router, prefix="/api/v1")
app.include_router(skills_router, prefix="/api/v1/skills")
