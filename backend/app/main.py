"""
ScriptMyIdeas - Main FastAPI Application
Modern script management platform with Back4app integration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.routes import scripts, versions, artifacts, search, integration

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 ScriptMyIdeas Backend Starting...")
    print(f"📊 Environment: {settings.ENVIRONMENT}")
    print(f"🔗 Back4app: {settings.BACK4APP_SERVER_URL}")
    yield
    # Shutdown
    print("👋 ScriptMyIdeas Backend Shutting Down...")

app = FastAPI(
    title="ScriptMyIdeas API",
    description="Modern script management platform with version control and artifact storage",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(scripts.router, prefix="/api/scripts", tags=["Scripts"])
app.include_router(versions.router, prefix="/api/versions", tags=["Versions"])
app.include_router(artifacts.router, prefix="/api/artifacts", tags=["Artifacts"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(integration.router, prefix="/api/integration", tags=["Integration"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "ScriptMyIdeas API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ScriptMyIdeas Backend"}
