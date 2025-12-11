"""
Configuration de l'API
"""
import os
from pathlib import Path

# Informations de l'API
API_VERSION = "v1"
APP_NAME = "Gestion Imprimerie API"
APP_DESCRIPTION = """
API REST pour l'application de gestion d'imprimerie.

Permet de gérer:
* Les transactions (recettes, dépenses, apports)
* La caisse
* Les rapports journaliers
* Les statistiques

Documentation complète disponible sur /api/docs
"""

# Chemins
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "imprimerie.db"

# Configuration JWT
SECRET_KEY = os.getenv("SECRET_KEY", "votre-cle-secrete-a-changer-en-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 heures

# Utilisateurs (à remplacer par une vraie base de données en production)
USERS_DB = {
    "admin": {
        "username": "admin",
        "password": "admin123",  # À hasher en production avec bcrypt
        "full_name": "Administrateur",
        "disabled": False
    }
}

# Configuration de pagination
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 100
