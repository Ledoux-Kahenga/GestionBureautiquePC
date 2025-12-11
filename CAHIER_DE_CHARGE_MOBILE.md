# CAHIER DE CHARGES - APPLICATION MOBILE GESTION IMPRIMERIE

## 📋 INFORMATIONS GÉNÉRALES

### Projet
**Nom** : Gestion Imprimerie Mobile  
**Version** : 1.0  
**Date** : 9 Décembre 2025  
**Type** : Application mobile iOS/Android  
**Backend** : API REST FastAPI (Python)

### Contexte
Extension mobile de l'application desktop de gestion d'imprimerie existante. L'application permet de gérer les transactions financières quotidiennes, la caisse et les rapports journaliers.

---

## 🎯 OBJECTIFS DU PROJET

### Objectifs Principaux
1. Permettre la gestion complète des transactions depuis mobile
2. Consulter l'état de la caisse en temps réel
3. Accéder aux rapports journaliers et mensuels
4. Clôturer les rapports en déplacement
5. Synchronisation en temps réel avec la base de données SQLite

### Objectifs Secondaires
- Interface intuitive et rapide
- Mode hors ligne avec synchronisation différée
- Notifications pour les alertes de caisse
- Export PDF des rapports

---

## 🎨 CHARTE GRAPHIQUE

### Couleurs Principales
```
COLOR_PRIMARY (Bleu)     : #2E86AB
COLOR_SUCCESS (Vert)     : #06A77D
COLOR_DANGER (Rouge)     : #D62246
COLOR_WARNING (Orange)   : #F77F00
COLOR_BACKGROUND (Blanc) : #FFFFFF
COLOR_LIGHT (Gris clair) : #F8F9FA
COLOR_BORDER (Gris)      : #E0E0E0
COLOR_TEXT (Noir)        : #212529
```

### Typographie
- **Police principale** : Arial ou équivalent (Roboto pour Android, SF Pro pour iOS)
- **Titres principaux** : 20pt, Bold
- **Titres secondaires** : 16pt, Bold
- **Corps de texte** : 14pt, Regular
- **Labels** : 12pt, Medium
- **Montants importants** : 32-48pt, Bold

### Iconographie
- 💰 Apport en capital
- 💸 Dépense spéciale
- 📊 Recettes journalières
- 🛒 Dépenses normales
- 📅 Rapport journalier
- 📋 Historique
- ⚙️ Paramètres
- 🔒 Clôture
- ✅ Validé
- ⚠️ Alerte

---

## 📱 SPÉCIFICATIONS FONCTIONNELLES

### 1. ÉCRAN D'ACCUEIL (Dashboard)

#### Layout
```
┌─────────────────────────────────┐
│  💰 Montant en Caisse           │
│     XXXXXX FC (36pt)            │
├─────────────────────────────────┤
│  📋 Rapport du Jour             │
│  9 Décembre 2025                │
├─────────────────────────────────┤
│ ┌─────────┬─────────┬─────────┐ │
│ │📊 Recettes│🛒 Dépenses│💵 Solde│ │
│ │ XXXX FC │ XXXX FC │ XXXX FC│ │
│ └─────────┴─────────┴─────────┘ │
├─────────────────────────────────┤
│  📋 Composition Caisse          │
│ ┌─────────┬─────────┬─────────┐ │
│ │✅ Soldes │💰 Apports│💸 Dépenses│ │
│ │ XXXX FC │ XXXX FC │ XXXX FC│ │
│ └─────────┴─────────┴─────────┘ │
├─────────────────────────────────┤
│  Transactions Récentes          │
│  [Liste scrollable]             │
└─────────────────────────────────┘
```

#### Fonctionnalités
- Affichage du montant en caisse (header fixe)
- 3 cartes indicateurs (Recettes, Dépenses, Solde)
- 3 cartes composition caisse (Soldes, Apports, Dépenses)
- Liste des 10 dernières transactions
- Bouton flottant "+" pour ajouter transaction
- Pull-to-refresh pour actualiser

#### Interactions
- Tap sur carte → Détails de la catégorie
- Tap sur transaction → Modifier/Supprimer (si rapport non clôturé)
- Long press sur transaction → Menu contextuel
- Bouton "+" → Modal de création

---

### 2. ÉCRAN TRANSACTIONS

#### Types de Transactions
1. **Recette** (vert #06A77D)
2. **Dépense normale** (rouge #D62246)
3. **Dépense spéciale** (rouge foncé)
4. **Apport** (vert clair)

#### Formulaire d'Ajout
```
┌─────────────────────────────────┐
│  Nouvelle Transaction           │
├─────────────────────────────────┤
│  Type : [Dropdown]              │
│  □ Recette                      │
│  □ Dépense                      │
│  □ Dépense Spéciale             │
│  □ Apport                       │
├─────────────────────────────────┤
│  Montant (FC) :                 │
│  [_____________]                │
├─────────────────────────────────┤
│  Description :                  │
│  [_____________]                │
├─────────────────────────────────┤
│  Date : [Date Picker]           │
│  Heure : [Time Picker]          │
├─────────────────────────────────┤
│ [Annuler]  [Enregistrer]        │
└─────────────────────────────────┘
```

#### Validation
- Montant : obligatoire, numérique, > 0
- Description : obligatoire, min 3 caractères
- Date : par défaut aujourd'hui
- Alerte si dépense > 50% de la caisse

#### Feedback
- Animation de succès (checkmark vert)
- Toast notification
- Actualisation automatique du dashboard

---

### 3. ÉCRAN CAISSE

#### Onglets
1. **Vue d'ensemble**
2. **Historique**

#### Vue d'ensemble
```
┌─────────────────────────────────┐
│  Filtres : [Ce mois ▼]          │
├─────────────────────────────────┤
│  💵 Recettes Mensuelles         │
│     XXXXX FC                    │
├─────────────────────────────────┤
│  💰 Apports                     │
│     XXXXX FC                    │
├─────────────────────────────────┤
│  💸 Dépenses Spéciales          │
│     XXXXX FC                    │
├─────────────────────────────────┤
│  Graphique (optionnel)          │
│  [Diagramme en barres/ligne]    │
└─────────────────────────────────┘
```

#### Filtres Disponibles
- Aujourd'hui
- Cette semaine
- Ce mois
- Mois spécifique (Janvier à Décembre)
- Toutes

#### Historique
- Liste des mouvements de caisse
- Filtres : Type (Apport/Dépense), Période
- Alternance de couleurs (lignes paires/impaires)
- Format : Date | Heure | Type | Description | Montant

---

### 4. ÉCRAN RAPPORTS

#### Liste des Rapports
```
┌─────────────────────────────────┐
│  Filtres : [Mois ▼] [Année ▼]   │
├─────────────────────────────────┤
│  📅 9 Décembre 2025             │
│  Recettes: 15000 FC             │
│  Dépenses: 8000 FC              │
│  Solde: 7000 FC    [Non clôturé]│
├─────────────────────────────────┤
│  📅 8 Décembre 2025             │
│  Recettes: 12000 FC             │
│  Dépenses: 6000 FC              │
│  Solde: 6000 FC         [✅]    │
├─────────────────────────────────┤
│  [Load more...]                 │
└─────────────────────────────────┘
```

#### Détails d'un Rapport
```
┌─────────────────────────────────┐
│  📅 Rapport du 9 Décembre 2025  │
│  [🔒 Clôturer]                   │
├─────────────────────────────────┤
│  📊 Recettes : XXXXX FC         │
│  🛒 Dépenses : XXXXX FC         │
│  💵 Solde    : XXXXX FC         │
├─────────────────────────────────┤
│  Transactions (XX)              │
│  [Liste complète]               │
├─────────────────────────────────┤
│  [📄 Exporter PDF]              │
└─────────────────────────────────┘
```

#### Fonctionnalités
- Filtrage par mois/année
- Affichage solde uniquement si clôturé
- Badge "Non clôturé" ou "✅"
- Bouton clôturer (confirmation requise)
- Export PDF du rapport
- Interdiction de modification si clôturé

---

### 5. NAVIGATION

#### Menu Principal (Bottom Navigation)
```
┌─────┬─────┬─────┬─────┬─────┐
│ 🏠  │ 💰  │ 📋  │ 📊  │ ⚙️  │
│Accueil│Trans│Caisse│Rapports│Params│
└─────┴─────┴─────┴─────┴─────┘
```

#### Header
- Titre de la page actuelle
- Montant en caisse (visible sur toutes les pages)
- Bouton retour (si applicable)

---

## 🔌 API FASTAPI - SPÉCIFICATIONS TECHNIQUES

### Architecture Backend

#### Structure de l'API
```
/api/v1/
├── /auth
│   ├── POST /login
│   └── POST /logout
├── /transactions
│   ├── GET /
│   ├── GET /{id}
│   ├── POST /
│   ├── PUT /{id}
│   └── DELETE /{id}
├── /caisse
│   ├── GET /montant
│   ├── GET /composition
│   └── GET /historique
├── /rapports
│   ├── GET /
│   ├── GET /{date}
│   ├── POST /cloturer
│   └── GET /pdf/{date}
└── /stats
    ├── GET /dashboard
    └── GET /periode
```

### Endpoints Détaillés

#### 1. Authentification

**POST /api/v1/auth/login**
```json
Request:
{
  "username": "string",
  "password": "string"
}

Response (200):
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin"
  }
}
```

#### 2. Transactions

**GET /api/v1/transactions**
```json
Query Params:
- date: string (format: YYYY-MM-DD, optionnel)
- type: string (recette|depense|apport, optionnel)
- limit: int (défaut: 50)
- offset: int (défaut: 0)

Response (200):
{
  "total": 100,
  "data": [
    {
      "id": 1,
      "type": "recette",
      "montant": 5000.0,
      "description": "Vente produits",
      "date": "2025-12-09",
      "heure": "14:30",
      "type_depense": "normale",
      "created_at": "2025-12-09 14:30:25"
    }
  ]
}
```

**POST /api/v1/transactions**
```json
Request:
{
  "type": "recette",
  "montant": 5000.0,
  "description": "Vente produits",
  "date": "2025-12-09",
  "type_depense": "normale"
}

Response (201):
{
  "id": 1,
  "type": "recette",
  "montant": 5000.0,
  "description": "Vente produits",
  "date": "2025-12-09",
  "heure": "14:30",
  "type_depense": "normale",
  "created_at": "2025-12-09 14:30:25",
  "message": "Transaction ajoutée avec succès"
}
```

**PUT /api/v1/transactions/{id}**
```json
Request:
{
  "montant": 5500.0,
  "description": "Vente produits (modifié)"
}

Response (200):
{
  "id": 1,
  "message": "Transaction modifiée avec succès"
}

Error (403):
{
  "detail": "Impossible de modifier une transaction d'un rapport clôturé"
}
```

**DELETE /api/v1/transactions/{id}**
```json
Response (200):
{
  "message": "Transaction supprimée avec succès"
}

Error (403):
{
  "detail": "Impossible de supprimer une transaction d'un rapport clôturé"
}
```

#### 3. Caisse

**GET /api/v1/caisse/montant**
```json
Response (200):
{
  "montant": 125000.0,
  "devise": "FC",
  "derniere_mise_a_jour": "2025-12-09 15:45:30"
}
```

**GET /api/v1/caisse/composition**
```json
Query Params:
- periode: string (aujourd_hui|cette_semaine|ce_mois|toutes)
- mois: int (1-12, optionnel si periode=mois_specifique)

Response (200):
{
  "periode": "ce_mois",
  "solde_cloture": 100000.0,
  "apports": 30000.0,
  "depenses_speciales": 5000.0,
  "total": 125000.0
}
```

**GET /api/v1/caisse/historique**
```json
Query Params:
- type: string (apport|depense, optionnel)
- date_debut: string (YYYY-MM-DD, optionnel)
- date_fin: string (YYYY-MM-DD, optionnel)
- limit: int (défaut: 50)

Response (200):
{
  "total": 25,
  "data": [
    {
      "id": 1,
      "type": "apport",
      "montant": 10000.0,
      "description": "Apport capital",
      "date": "2025-12-09",
      "heure": "10:00"
    }
  ]
}
```

#### 4. Rapports

**GET /api/v1/rapports**
```json
Query Params:
- mois: int (1-12, optionnel)
- annee: int (optionnel)
- limit: int (défaut: 30)

Response (200):
{
  "total": 30,
  "data": [
    {
      "date": "2025-12-09",
      "recettes": 15000.0,
      "depenses": 8000.0,
      "solde": 7000.0,
      "cloture": false,
      "nombre_transactions": 12
    }
  ]
}
```

**GET /api/v1/rapports/{date}**
```json
Response (200):
{
  "date": "2025-12-09",
  "recettes": 15000.0,
  "depenses": 8000.0,
  "solde": 7000.0,
  "cloture": false,
  "transactions": [
    {
      "id": 1,
      "type": "recette",
      "montant": 5000.0,
      "description": "Vente",
      "heure": "10:30"
    }
  ]
}
```

**POST /api/v1/rapports/cloturer**
```json
Request:
{
  "date": "2025-12-09"
}

Response (200):
{
  "date": "2025-12-09",
  "cloture": true,
  "heure_cloture": "23:59:00",
  "message": "Rapport clôturé avec succès"
}

Error (400):
{
  "detail": "Le rapport du 2025-12-09 est déjà clôturé"
}
```

**GET /api/v1/rapports/pdf/{date}**
```json
Response (200):
Content-Type: application/pdf
[Binary PDF data]

Error (404):
{
  "detail": "Aucun rapport trouvé pour cette date"
}
```

#### 5. Statistiques

**GET /api/v1/stats/dashboard**
```json
Response (200):
{
  "caisse": {
    "montant": 125000.0,
    "variation_24h": 7000.0,
    "pourcentage_variation": 5.9
  },
  "rapport_jour": {
    "date": "2025-12-09",
    "recettes": 15000.0,
    "depenses": 8000.0,
    "solde": 7000.0,
    "cloture": false
  },
  "derniere_transactions": [
    {
      "id": 1,
      "type": "recette",
      "montant": 5000.0,
      "description": "Vente",
      "date": "2025-12-09",
      "heure": "14:30"
    }
  ]
}
```

**GET /api/v1/stats/periode**
```json
Query Params:
- date_debut: string (YYYY-MM-DD)
- date_fin: string (YYYY-MM-DD)

Response (200):
{
  "periode": {
    "debut": "2025-12-01",
    "fin": "2025-12-09"
  },
  "total_recettes": 135000.0,
  "total_depenses": 72000.0,
  "solde_net": 63000.0,
  "nombre_transactions": 45,
  "moyenne_quotidienne": 7000.0
}
```

### Codes d'Erreur

```
200 OK - Requête réussie
201 Created - Ressource créée
400 Bad Request - Données invalides
401 Unauthorized - Non authentifié
403 Forbidden - Action interdite
404 Not Found - Ressource non trouvée
500 Internal Server Error - Erreur serveur
```

### Authentification

**Type** : JWT (JSON Web Token)

**Header** :
```
Authorization: Bearer <token>
```

**Durée de validité** : 24 heures

### Format des Dates
- Date : `YYYY-MM-DD` (ex: 2025-12-09)
- DateTime : `YYYY-MM-DD HH:MM:SS` (ex: 2025-12-09 14:30:25)
- Heure : `HH:MM` (ex: 14:30)

---

## 📊 SPÉCIFICATIONS TECHNIQUES MOBILE

### Plateformes Cibles
- **Android** : Version minimale 6.0 (API 23)
- **iOS** : Version minimale 12.0

### Framework Recommandé
**Flutter** (Dart) ou **React Native** (JavaScript/TypeScript)

### Librairies Requises

#### Réseau & API
- HTTP client (dio pour Flutter, axios pour React Native)
- JWT decoder
- Gestion cache/offline

#### UI
- Charts/Graphs pour statistiques
- Date/Time pickers
- Pull-to-refresh
- Skeleton loaders

#### Storage
- Secure storage pour token
- SQLite local pour cache offline

#### PDF
- PDF viewer
- PDF generator (optionnel)

### Architecture Recommandée
```
lib/
├── core/
│   ├── api/
│   │   ├── api_client.dart
│   │   └── endpoints.dart
│   ├── models/
│   │   ├── transaction.dart
│   │   ├── rapport.dart
│   │   └── caisse.dart
│   └── services/
│       ├── auth_service.dart
│       └── storage_service.dart
├── features/
│   ├── dashboard/
│   ├── transactions/
│   ├── caisse/
│   └── rapports/
├── shared/
│   ├── widgets/
│   ├── theme/
│   └── utils/
└── main.dart
```

---

## 🔒 SÉCURITÉ

### Authentification
- Login avec username/password
- Token JWT stocké en secure storage
- Auto-logout après expiration du token
- Refresh token automatique

### Validation des Données
- Validation côté client ET serveur
- Sanitization des inputs
- Protection contre injection SQL
- Limite de taux de requêtes (rate limiting)

### Permissions
- Pas d'accès aux données sans authentification
- Modification/suppression uniquement si rapport non clôturé
- Logs d'audit pour actions critiques

---

## ⚡ PERFORMANCES

### Optimisations Requises
- Pagination des listes (50 items max par page)
- Lazy loading des images/PDF
- Cache des données fréquentes
- Debounce sur recherches
- Compression des images

### Mode Offline
- Cache des dernières données consultées
- Queue des actions à synchroniser
- Indicateur visuel du statut de connexion
- Synchronisation automatique au retour en ligne

---

## 🎨 UX/UI GUIDELINES

### Principes
1. **Simplicité** : Maximum 3 taps pour toute action
2. **Feedback** : Toujours confirmer les actions
3. **Prévention** : Alertes avant actions destructives
4. **Cohérence** : Mêmes patterns dans toute l'app
5. **Accessibilité** : Contraste suffisant, tailles tactiles 44x44

### Animations
- Transitions fluides (300ms)
- Loading spinners
- Skeleton screens pour chargement
- Micro-interactions sur boutons

### Messages
- Succès : Toast vert avec icône ✅
- Erreur : Toast rouge avec icône ❌
- Avertissement : Toast orange avec icône ⚠️
- Info : Toast bleu avec icône ℹ️

### États Vides
- Illustration + message explicatif
- Call-to-action clair
- Pas de pages complètement blanches

---

## 📦 LIVRABLES ATTENDUS

### Phase 1 : MVP (4 semaines)
- [ ] Authentification
- [ ] Dashboard avec indicateurs
- [ ] CRUD transactions
- [ ] Liste des rapports
- [ ] Consultation caisse

### Phase 2 : Fonctionnalités Avancées (3 semaines)
- [ ] Clôture rapports
- [ ] Filtres avancés
- [ ] Mode offline
- [ ] Export PDF

### Phase 3 : Optimisations (2 semaines)
- [ ] Tests unitaires/intégration
- [ ] Optimisation performances
- [ ] Documentation
- [ ] Déploiement stores

### Documentation Requise
1. README avec instructions d'installation
2. Documentation API (auto-générée par FastAPI)
3. Guide utilisateur mobile
4. Documentation technique architecture

### Tests
- Tests unitaires (couverture > 70%)
- Tests d'intégration API
- Tests UI critiques
- Tests sur devices réels (Android + iOS)

---

## 🚀 DÉPLOIEMENT

### Backend (API FastAPI)
**Options gratuites** :
1. **Render.com** (Recommandé)
   - Plan gratuit : 750h/mois
   - Auto-deploy depuis Git
   - HTTPS gratuit

2. **Railway.app**
   - $5 de crédits gratuits/mois
   - Facile à configurer

3. **PythonAnywhere**
   - 500MB gratuit
   - Support Python natif

### Base de Données
- SQLite (fichier sur serveur)
- PostgreSQL gratuit (Render, Railway)

### Mobile Apps
- **Android** : Google Play Store
- **iOS** : Apple App Store
- **Beta** : TestFlight (iOS), Google Play Internal Testing

---

## 📞 SUPPORT & MAINTENANCE

### Post-Déploiement
- Corrections bugs critiques : 24h
- Corrections bugs mineurs : 1 semaine
- Nouvelles fonctionnalités : à planifier

### Monitoring
- Logs erreurs API
- Analytics usage mobile
- Crash reports
- Métriques performances

---

## 💰 BUDGET ESTIMÉ

### Développement
- Backend API FastAPI : 1-2 semaines
- Application Mobile MVP : 4-6 semaines
- Tests & Optimisations : 2 semaines

### Hébergement (par mois)
- API : Gratuit (Render.com)
- Base de données : Gratuit (SQLite/PostgreSQL)
- Stores : $25 (Google) + $99/an (Apple)

---

## 📝 NOTES IMPORTANTES

### Contraintes Techniques
1. Pas de modification des rapports clôturés
2. Auto-clôture à 23h59
3. Montants en Francs Congolais (FC)
4. Dates au format DD/MM/YYYY pour affichage
5. Conservation historique complet

### Règles Métier
1. Solde = Recettes - Dépenses normales
2. Caisse = Soldes clôturés + Apports - Dépenses spéciales
3. Alerte si dépense > 50% de la caisse
4. Alerte si caisse devient négative

### Points d'Attention
- La clôture est irréversible
- Les dates ne peuvent pas être futures
- Les montants doivent être positifs
- Les descriptions sont obligatoires

---

## 📧 CONTACTS

**Propriétaire du Projet** : [À remplir]  
**Chef de Projet** : [À remplir]  
**Développeur Backend** : [À remplir]  
**Développeur Mobile** : [À remplir]

---

## ✅ CRITÈRES D'ACCEPTATION

### Critères Fonctionnels
- ✅ Toutes les fonctionnalités du cahier des charges implémentées
- ✅ Synchronisation temps réel avec backend
- ✅ Mode offline fonctionnel
- ✅ Aucune perte de données

### Critères Techniques
- ✅ Code propre et documenté
- ✅ Tests unitaires > 70% couverture
- ✅ Performances : < 2s chargement initial
- ✅ Compatible Android 6.0+ et iOS 12.0+

### Critères UX/UI
- ✅ Interface conforme à la charte graphique
- ✅ Navigation intuitive
- ✅ Feedbacks visuels pour toutes les actions
- ✅ Gestion erreurs claire

---

**Version** : 1.0  
**Date** : 9 Décembre 2025  
**Statut** : En attente de validation
