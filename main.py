"""
Application de gestion d'imprimerie
Point d'entrée principal
"""
import sys
from PyQt5.QtWidgets import QApplication
from gui import ImprimerieApp
from models.transaction_model import TransactionModel


def main():
    """Fonction principale"""
    # Initialiser la base de données
    db = TransactionModel()
    db.create_tables()
    
    # Créer et lancer l'application
    app = QApplication(sys.argv)
    window = ImprimerieApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
