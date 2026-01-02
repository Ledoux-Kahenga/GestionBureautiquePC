"""
Configuration de l'application
"""
import os
import sys

# Chemin de la base de données
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'imprimerie.db')

# Configuration de l'interface
WINDOW_TITLE = "Gestion Bureautique"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# Configuration des couleurs
COLOR_PRIMARY = "#2E86AB"
COLOR_SECONDARY = "#A23B72"
COLOR_SUCCESS = "#06A77D"
COLOR_DANGER = "#D62246"
COLOR_BG = "#F7F7F7"

# Configuration des polices
IS_WINDOWS = sys.platform == 'win32'

# Tailles de police (augmentées pour meilleure lisibilité)
FONT_SIZE_XS = 9       # Très petit
FONT_SIZE_SM = 10      # Petit
FONT_SIZE_MD = 11      # Moyen
FONT_SIZE_LG = 12      # Grand
FONT_SIZE_XL = 14      # Très grand
FONT_SIZE_XXL = 16     # Titre
FONT_SIZE_HUGE = 20    # Très grand nombre
FONT_SIZE_GIANT = 24   # Valeurs principales
FONT_SIZE_MEGA = 32    # Solde principal

# Nom de la police personnalisée (Poppins du dossier fonts/)
FONT_FAMILY = "Poppins"
FONT_FAMILY_FALLBACK = "Segoe UI" if IS_WINDOWS else "Arial"
