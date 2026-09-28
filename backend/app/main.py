from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from prometheus_fastapi_instrumentator import Instrumentator
from .database import Base, engine
from .routes.auth import router as auth_router
from .routes.employees import router as employee_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management System",
    description="Backend-only Employee Management API with authentication, CRUD and Prometheus monitoring.",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(employee_router)
Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"service": "employee-backend", "version": "1.0.0", "docs": "/docs", "metrics": "/metrics"}

@app.get("/health", tags=["System"])
def health():
    return {"status": "healthy", "service": "employee-backend", "version": "1.0.0"}

@app.get("/doc", include_in_schema=False)
def swagger_alias():
    return RedirectResponse("/docs")
