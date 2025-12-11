# Application de Gestion d'Imprimerie

Application desktop Python pour la gestion complète d'une imprimerie avec suivi des dépenses, recettes et statistiques financières.

## 📋 Fonctionnalités

- ✅ Enregistrement des recettes journalières
- ✅ Enregistrement des dépenses journalières
- ✅ Affichage du solde disponible en temps réel
- ✅ Affichage des totaux (recettes et dépenses)
- ✅ Historique complet des transactions
- ✅ Suppression de transactions
- ✅ Interface graphique intuitive avec tkinter
- ✅ Base de données SQLite pour la persistance des données

## 🚀 Installation

### Prérequis

- Python 3.7 ou supérieur
- tkinter (généralement inclus avec Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
   ```bash
   cd /home/doux/Projets/Bureautique
   ```

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Linux/Mac
   # ou
   venv\Scripts\activate  # Sur Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Utilisation

### Lancer l'application

```bash
python main.py
```

### Utilisation de l'interface

1. **Ajouter une transaction**
   - Sélectionnez le type (Recette ou Dépense)
   - Entrez le montant
   - Ajoutez une description (optionnel)
   - Cliquez sur "➕ Ajouter la transaction"

2. **Visualiser les statistiques**
   - Le solde disponible s'affiche en haut (vert si positif, rouge si négatif)
   - Total des recettes affiché au centre
   - Total des dépenses affiché à droite

3. **Consulter l'historique**
   - Toutes les transactions sont listées dans le tableau
   - Les recettes apparaissent en vert
   - Les dépenses apparaissent en rouge

4. **Supprimer une transaction**
   - Sélectionnez une ligne dans l'historique
   - Cliquez sur "🗑️ Supprimer"
   - Confirmez la suppression

5. **Actualiser l'affichage**
   - Cliquez sur "🔄 Actualiser" pour rafraîchir les données

## 📁 Structure du Projet

```
Bureautique/
├── .github/
│   └── copilot-instructions.md    # Instructions pour GitHub Copilot
├── main.py                        # Point d'entrée de l'application
├── gui.py                         # Interface graphique (tkinter)
├── database.py                    # Gestion de la base de données
├── config.py                      # Configuration de l'application
├── requirements.txt               # Dépendances Python
├── README.md                      # Documentation
└── imprimerie.db                  # Base de données SQLite (créée automatiquement)
```

## 🛠️ Technologies Utilisées

- **Python 3** - Langage de programmation
- **tkinter** - Framework pour l'interface graphique
- **SQLite** - Base de données embarquée
- **python-dateutil** - Gestion des dates
- **Pillow** - Traitement d'images (optionnel)

## 📊 Base de Données

L'application utilise SQLite avec la structure suivante:

### Table `transactions`
- `id` (INTEGER) - Identifiant unique
- `type` (TEXT) - Type de transaction ('recette' ou 'depense')
- `montant` (REAL) - Montant de la transaction
- `description` (TEXT) - Description optionnelle
- `date` (TEXT) - Date de la transaction (YYYY-MM-DD)
- `created_at` (TEXT) - Date et heure de création

## 🎨 Personnalisation

Vous pouvez modifier les couleurs et paramètres dans `config.py`:

```python
# Configuration des couleurs
COLOR_PRIMARY = "#2E86AB"      # Couleur principale
COLOR_SECONDARY = "#A23B72"    # Couleur secondaire
COLOR_SUCCESS = "#06A77D"      # Couleur pour les recettes
COLOR_DANGER = "#D62246"       # Couleur pour les dépenses
COLOR_BG = "#F7F7F7"          # Couleur de fond

# Configuration de la fenêtre
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
```

## 🔧 Développement

### Ajouter une nouvelle fonctionnalité

1. Modifiez `database.py` pour les opérations de base de données
2. Mettez à jour `gui.py` pour l'interface utilisateur
3. Ajustez `config.py` si nécessaire

### Débogage

Pour activer le mode debug, vous pouvez ajouter des logs dans le code:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Notes

- La base de données est créée automatiquement au premier lancement
- Les montants sont affichés en FCFA (personnalisable dans le code)
- L'application gère automatiquement les connexions à la base de données
- Le solde est calculé en temps réel (recettes - dépenses)

## 🤝 Contribution

Pour contribuer au projet:
1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est libre d'utilisation pour un usage personnel ou commercial.

## 👤 Auteur

Projet créé pour la gestion d'imprimerie.

## 🆘 Support

Pour toute question ou problème:
- Vérifiez que Python 3.7+ est installé
- Assurez-vous que tkinter est disponible
- Vérifiez les permissions d'écriture dans le dossier du projet
