# API FastAPI - Gestion Imprimerie

API REST complète pour l'application de gestion d'imprimerie.

## 🚀 Installation

### 1. Installer les dépendances

```bash
pip install -r requirements-api.txt
```

### 2. Configuration

Créer un fichier `.env` (optionnel) :

```env
SECRET_KEY=votre-cle-secrete-ultra-securisee
DATABASE_PATH=/chemin/vers/imprimerie.db
```

## 📝 Lancement de l'API

### Mode Développement

```bash
cd api
python main.py
```

ou

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Mode Production

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

L'API sera accessible sur : `http://localhost:8000`

## 📚 Documentation

Une fois l'API lancée, la documentation interactive est disponible sur :

- **Swagger UI** : http://localhost:8000/api/docs
- **ReDoc** : http://localhost:8000/api/redoc

## 🔐 Authentification

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

Réponse :
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "username": "admin",
    "full_name": "Administrateur"
  }
}
```

### Utiliser le Token

Pour toutes les requêtes suivantes, ajouter le header :

```
Authorization: Bearer <votre_token>
```

Exemple :
```bash
curl -X GET "http://localhost:8000/api/v1/transactions" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 📋 Endpoints Disponibles

### Authentification
- `POST /api/v1/auth/login` - Connexion
- `POST /api/v1/auth/logout` - Déconnexion
- `GET /api/v1/auth/me` - Infos utilisateur

### Transactions
- `GET /api/v1/transactions` - Liste des transactions
- `GET /api/v1/transactions/{id}` - Détail d'une transaction
- `POST /api/v1/transactions` - Créer une transaction
- `PUT /api/v1/transactions/{id}` - Modifier une transaction
- `DELETE /api/v1/transactions/{id}` - Supprimer une transaction

### Caisse
- `GET /api/v1/caisse/montant` - Montant en caisse
- `GET /api/v1/caisse/composition` - Composition de la caisse
- `GET /api/v1/caisse/historique` - Historique des mouvements

### Rapports
- `GET /api/v1/rapports` - Liste des rapports
- `GET /api/v1/rapports/{date}` - Détail d'un rapport
- `POST /api/v1/rapports/cloturer` - Clôturer un rapport
- `GET /api/v1/rapports/pdf/{date}` - Télécharger PDF

### Statistiques
- `GET /api/v1/stats/dashboard` - Stats du dashboard
- `GET /api/v1/stats/periode` - Stats sur une période

## 🔧 Exemples d'Utilisation

### Créer une Transaction

```bash
curl -X POST "http://localhost:8000/api/v1/transactions" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "recette",
    "montant": 5000,
    "description": "Vente produits",
    "date": "2025-12-09",
    "type_depense": "normale"
  }'
```

### Obtenir le Montant en Caisse

```bash
curl -X GET "http://localhost:8000/api/v1/caisse/montant" \
  -H "Authorization: Bearer <token>"
```

### Clôturer un Rapport

```bash
curl -X POST "http://localhost:8000/api/v1/rapports/cloturer" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-12-09"
  }'
```

### Obtenir les Stats du Dashboard

```bash
curl -X GET "http://localhost:8000/api/v1/stats/dashboard" \
  -H "Authorization: Bearer <token>"
```

## 🌐 Déploiement

### Render.com (Gratuit)

1. Créer un compte sur [render.com](https://render.com)
2. Créer un nouveau "Web Service"
3. Connecter votre repository Git
4. Configuration :
   - **Build Command** : `pip install -r requirements-api.txt`
   - **Start Command** : `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
5. Ajouter les variables d'environnement
6. Déployer

### Railway.app

1. Créer un compte sur [railway.app](https://railway.app)
2. Créer un nouveau projet depuis GitHub
3. Railway détecte automatiquement FastAPI
4. Ajouter les variables d'environnement
5. Déployer

## 🔒 Sécurité

### En Production

1. **Changer le SECRET_KEY** dans `.env`
2. **Hasher les mots de passe** avec bcrypt
3. **Utiliser HTTPS** uniquement
4. **Limiter les CORS** aux domaines autorisés
5. **Activer le rate limiting**
6. **Utiliser une vraie base de données** utilisateurs

### Exemple avec Bcrypt

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hasher un mot de passe
hashed = pwd_context.hash("admin123")

# Vérifier un mot de passe
pwd_context.verify("admin123", hashed)
```

## 📊 Monitoring

### Logs

Les logs sont affichés dans la console. En production, configurer un système de logging :

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Health Check

```bash
curl http://localhost:8000/health
```

## 🐛 Débogage

### Activer le mode debug

```python
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )
```

### Tester les endpoints

Utiliser la documentation interactive Swagger UI : http://localhost:8000/api/docs

## 📝 Notes

- Le token JWT expire après 24 heures
- Les rapports clôturés ne peuvent pas être modifiés
- Les dates doivent être au format `YYYY-MM-DD`
- Les montants doivent être positifs
- Les descriptions sont obligatoires (min 3 caractères)

## 🤝 Support

Pour toute question ou problème, consulter :
- Documentation Swagger : `/api/docs`
- Cahier des charges : `CAHIER_DE_CHARGE_MOBILE.md`
