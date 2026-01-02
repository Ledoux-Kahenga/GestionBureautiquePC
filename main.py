"""
Application de gestion d'imprimerie
Point d'entrée principal
"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QFontDatabase
from gui import ImprimerieApp
from models.transaction_model import TransactionModel
from config import FONT_FAMILY, FONT_FAMILY_FALLBACK, FONT_SIZE_SM


def load_custom_fonts():
    """Charger les polices personnalisées depuis le dossier fonts/"""
    fonts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
    
    if os.path.exists(fonts_dir):
        for font_file in os.listdir(fonts_dir):
            if font_file.endswith(('.ttf', '.otf')):
                font_path = os.path.join(fonts_dir, font_file)
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1:
                    families = QFontDatabase.applicationFontFamilies(font_id)
                    print(f"Police chargée: {families}")
                else:
                    print(f"Erreur chargement: {font_file}")


def main():
    """Fonction principale"""
    # Initialiser la base de données
    db = TransactionModel()
    db.create_tables()
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    # Charger les polices personnalisées
    load_custom_fonts()
    
    # Définir la police par défaut (Poppins ou fallback)
    default_font = QFont(FONT_FAMILY, FONT_SIZE_SM)
    if not default_font.exactMatch():
        default_font = QFont(FONT_FAMILY_FALLBACK, FONT_SIZE_SM)
    app.setFont(default_font)
    
    window = ImprimerieApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
