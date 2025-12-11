"""
Configuration de l'application
"""
import os

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
