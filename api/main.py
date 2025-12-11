"""
API FastAPI pour l'application de gestion d'imprimerie
Point d'entrée principal de l'API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from api.routers import auth, transactions, caisse, rapports, stats
from api.config import API_VERSION, APP_NAME, APP_DESCRIPTION

# Créer l'application FastAPI
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=API_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configuration CORS pour permettre les requêtes depuis mobile
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(auth.router, prefix=f"/api/{API_VERSION}/auth", tags=["Authentification"])
app.include_router(transactions.router, prefix=f"/api/{API_VERSION}/transactions", tags=["Transactions"])
app.include_router(caisse.router, prefix=f"/api/{API_VERSION}/caisse", tags=["Caisse"])
app.include_router(rapports.router, prefix=f"/api/{API_VERSION}/rapports", tags=["Rapports"])
app.include_router(stats.router, prefix=f"/api/{API_VERSION}/stats", tags=["Statistiques"])

@app.get("/")
async def root():
    """Point d'entrée racine de l'API"""
    return {
        "message": "API Gestion Imprimerie",
        "version": API_VERSION,
        "docs": "/api/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "version": API_VERSION
    }

# Gestionnaire d'erreurs global
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Erreur interne du serveur"}
    )

if __name__ == "__main__":
    # Lancer le serveur en mode développement
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
