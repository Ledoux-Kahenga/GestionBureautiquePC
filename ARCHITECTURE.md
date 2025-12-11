# Structure MVC du Projet

## Architecture

Le projet a été restructuré selon le pattern MVC (Model-View-Controller) pour une meilleure organisation et séparation des responsabilités.

```
Bureautique/
├── models/                    # Couche Modèle (Données)
│   ├── __init__.py
│   └── transaction_model.py   # Gestion de la base de données SQLite
│
├── views/                     # Couche Vue (Interface modulaire)
│   ├── __init__.py
│   ├── accueil_tab.py        # Onglet Accueil (Dashboard + Transactions)
│   ├── rapports_tab.py       # Onglet Rapports (Filtres + Statistiques)
│   └── caisse_tab.py         # Onglet Caisse (Dépenses spéciales + Apports)
│
├── controllers/               # Couche Contrôleur (Logique métier)
│   ├── __init__.py
│   └── transaction_controller.py  # Logique métier des transactions
│
├── utils/                     # Utilitaires
│   ├── __init__.py
│   ├── config.py             # Configuration de l'application
│   └── pdf_generator.py      # Génération de rapports PDF
│
├── gui.py                    # Interface graphique principale PyQt5
├── main.py                   # Point d'entrée de l'application
├── database.py               # (Ancien fichier, à supprimer)
├── rapport_pdf.py            # (Ancien fichier, à supprimer)
└── config.py                 # (Ancien fichier, à supprimer)
```

## Responsabilités

### Models (models/)
- **transaction_model.py**: Gère toutes les opérations de base de données
  - Connexion/déconnexion SQLite
  - CRUD des transactions
  - Calculs de solde et statistiques
  - Gestion des rapports clôturés
  - Gestion de la caisse

### Controllers (controllers/)
- **transaction_controller.py**: Contient la logique métier
  - Validation des données
  - Orchestration des opérations complexes
  - Gestion des règles métier (ex: clôture automatique)
  - Interface entre la vue et le modèle

### Views (views/)
- **accueil_tab.py**: Onglet principal de l'application
  - Dashboard avec indicateurs (Solde, Recettes, Dépenses)
  - Formulaire d'ajout de transactions
  - Tableau d'historique des transactions journalières
  - Actualisation en temps réel
  
- **rapports_tab.py**: Onglet de visualisation des rapports
  - Filtres de période (Tout, Aujourd'hui, Semaine, Mois, Année, Date spécifique)
  - Tableau des statistiques par jour
  - Affichage des rapports clôturés
  - Export PDF
  
- **caisse_tab.py**: Onglet de gestion de la caisse
  - Affichage du montant total en caisse
  - Composition détaillée (Soldes clôturés, Dépenses spéciales, Apports)
  - Formulaire d'ajout de dépenses spéciales
  - Formulaire d'ajout d'apports en capital
  - Historique complet des mouvements de caisse

### Utils (utils/)
- **config.py**: Constantes et configuration
- **pdf_generator.py**: Génération de rapports PDF
  - Mise en forme des documents
  - Styles et tableaux

### GUI (gui.py)
- Interface graphique PyQt5
- Gestion des événements utilisateur
- Affichage des données

## Migration

Les anciens fichiers peuvent être supprimés:
- `database.py` → remplacé par `models/transaction_model.py`
- `rapport_pdf.py` → remplacé par `utils/pdf_generator.py`
- `config.py` (racine) → remplacé par `utils/config.py`

Un fichier `database_compat.py` a été créé pour assurer la compatibilité temporaire.

## Avantages de la Structure Modulaire

1. **Séparation des responsabilités**: Chaque composant a un rôle clair et défini
2. **Maintenabilité**: Plus facile à maintenir et déboguer grâce à la modularisation
3. **Testabilité**: Chaque couche et module peut être testé indépendamment
4. **Évolutivité**: Facilite l'ajout de nouvelles fonctionnalités sans impacter l'existant
5. **Réutilisabilité**: Les composants peuvent être réutilisés dans d'autres projets
6. **Lisibilité**: Code mieux organisé, fichiers plus courts et ciblés
7. **Collaboration**: Plusieurs développeurs peuvent travailler sur différents modules
8. **Performance**: Chargement optimisé des modules au besoin

## Communication entre les Couches

```
┌─────────────┐
│   main.py   │  ← Point d'entrée
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   gui.py    │  ← Fenêtre principale, gestion des onglets
└──────┬──────┘
       │
       ├──────┐ Charge les vues
       │      │
       ▼      ▼      ▼
┌──────────┬──────────┬──────────┐
│ accueil  │ rapports │  caisse  │  ← Composants d'interface
└────┬─────┴────┬─────┴────┬─────┘
     │          │          │
     └──────────┴──────────┘
                │
                ▼ Utilise le contrôleur
     ┌──────────────────────┐
     │TransactionController │  ← Logique métier
     └──────────┬───────────┘
                │
                ▼ Manipule le modèle
     ┌──────────────────────┐
     │  TransactionModel    │  ← Accès aux données
     └──────────┬───────────┘
                │
                ▼
        ┌───────────────┐
        │  Database     │  ← SQLite
        └───────────────┘
```
