from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.v1.routes.auth_routes import router as auth_router
from backend.api.v1.routes.predict_routes import router as predict_router
from backend.api.v1.routes.analyze_routes import router as analyze_router
from backend.api.v1.routes.salary_routes import router as salary_router

# ❌ chat desactivado
# from backend.api.v1.routes.chat_routes import router as chat_router

app = FastAPI(
    title="TechCareer API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])
app.include_router(predict_router, prefix="/api/v1", tags=["Predict"])
app.include_router(analyze_router, prefix="/api/v1", tags=["Analyze CV"])
app.include_router(salary_router, prefix="/api/v1", tags=["Salary"])


# ❌ NO incluir chat
# app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])


@app.get("/health")
def health():
    return {"status": "ok"}
