from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users
from fastapi.responses import JSONResponse

# Crear instancia de FastAPI
app = FastAPI(
    title="JSONPlaceholder API Proxy",
    description="API intermediaria que consume JSONPlaceholder y expone endpoints limpios",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS (para permitir requests desde frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(users.router, prefix="/api/v1")

# Endpoint de health check en la raíz
@app.get("/health")
async def health_check():
    """
    Endpoint de salud del servicio
    """
    return {"status": "ok"}

# Endpoint raíz con información básica
@app.get("/")
async def root():
    """
    Endpoint raíz con información de la API
    """
    return {
        "message": "JSONPlaceholder API Proxy",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Manejo de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Manejo global de excepciones
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Something went wrong"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Solo para desarrollo
    )