"""
Interface graphique de l'application avec PyQt5
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QLineEdit, QRadioButton, 
                             QTableWidget, QTableWidgetItem, QFrame, QButtonGroup,
                             QMessageBox, QHeaderView, QComboBox, QTabWidget, QDialog, QFileDialog, QScrollArea, QDateEdit)
from PyQt5.QtCore import Qt, QTimer, QTime, QDate
from PyQt5.QtGui import QFont, QColor, QPixmap
from datetime import datetime, timedelta
from models.transaction_model import TransactionModel as Database
from utils.pdf_generator import PDFGenerator as GenerateurRapportPDF
from views.caisse_tab import CaisseTab
from views.accueil_tab import AccueilTab
from views.rapports_tab import RapportsTab
from config import *
import os


class ImprimerieApp(QMainWindow):
    """Classe principale de l'interface graphique"""
    
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.jour_courant = datetime.now().strftime("%Y-%m-%d")
        self.verifier_nouveau_jour()  # Vérifier si c'est un nouveau jour au démarrage
        self.setup_window()
        self.create_widgets()
        self.actualiser_affichage()
        self.actualiser_dashboard()
        self.actualiser_caisse()
        self.setup_auto_cloture()  # Configurer la clôture automatique
        
    def setup_window(self):
        """Configurer la fenêtre principale"""
        self.setWindowTitle(WINDOW_TITLE)
        
        # Obtenir la taille de l'écran
        from PyQt5.QtWidgets import QApplication, QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        
        # Calculer 80% de la taille de l'écran
        width = int(screen.width() * 0.6)
        height = int(screen.height() * 0.9)
        
        # Centrer la fenêtre
        x = (screen.width() - width) // 2
        y = (screen.height() - height) // 2
        
        self.setGeometry(x, y, width, height)
        
        # Fixer la taille de la fenêtre (bloquer le redimensionnement)
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)
        
        self.setStyleSheet(f"background-color: {COLOR_BG};")
    
    def setup_auto_cloture(self):
        """Configurer le timer pour la clôture automatique à 23h59"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.verifier_heure_cloture)
        # Vérifier toutes les minutes
        self.timer.start(60000)  # 60000 ms = 1 minute
    
    def verifier_heure_cloture(self):
        """Vérifier si c'est l'heure de clôturer automatiquement (23h59)"""
        heure_actuelle = QTime.currentTime()
        date_actuelle = datetime.now().strftime("%Y-%m-%d")
        
        # Vérifier si on a changé de jour
        if date_actuelle != self.jour_courant:
            self.verifier_nouveau_jour()
            self.jour_courant = date_actuelle
            # Actualiser l'affichage après le changement de jour
            self.actualiser_affichage()
            self.actualiser_dashboard()
            self.actualiser_caisse()
            return
        
        # Clôture automatique à 23h59
        if heure_actuelle.hour() == 23 and heure_actuelle.minute() == 59:
            date_jour = datetime.now().strftime("%Y-%m-%d")
            est_cloture = self.db.verifier_cloture(date_jour)
            
            if not est_cloture:
                # Vérifier s'il y a des recettes avant de clôturer
                stats = self.db.calculer_solde(date_jour)
                
                if stats['recettes'] > 0:
                    # Clôturer automatiquement seulement s'il y a des recettes
                    self.db.cloturer_rapport(date_jour)
                    self.actualiser_affichage()
                    self.actualiser_dashboard()
                    self.actualiser_caisse()
                    
                    QMessageBox.information(
                        self,
                        "Clôture Automatique",
                        f"Le rapport du {datetime.now().strftime('%d/%m/%Y')} a été clôturé automatiquement à 23h59."
                    )
                else:
                    # Ne pas clôturer si recettes = 0
                    print(f"Clôture automatique annulée : Aucune recette pour le {date_jour}")
    
    def verifier_nouveau_jour(self):
        """Vérifier si c'est un nouveau jour et clôturer le rapport précédent si nécessaire"""
        # Récupérer la date du dernier rapport non clôturé
        derniers_rapports = self.db.obtenir_rapports_non_clotures()
        
        if derniers_rapports:
            date_actuelle = datetime.now().strftime("%Y-%m-%d")
            
            for rapport in derniers_rapports:
                date_rapport = rapport[0]
                
                # Si le rapport n'est pas d'aujourd'hui, vérifier s'il peut être clôturé
                if date_rapport != date_actuelle:
                    # Vérifier s'il y a des recettes pour ce jour
                    stats = self.db.calculer_solde(date_rapport)
                    
                    if stats['recettes'] > 0:
                        # Clôturer automatiquement seulement s'il y a des recettes
                        self.db.cloturer_rapport(date_rapport)
                        print(f"Rapport du {date_rapport} clôturé automatiquement (nouveau jour détecté)")
                    else:
                        # Supprimer les transactions du jour sans recette
                        print(f"Rapport du {date_rapport} ignoré (aucune recette, journée néant)")
        
    def create_widgets(self):
        """Créer les widgets de l'interface"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
       
      
        central_widget.setLayout(main_layout)
        
        # En-tête avec logo et titre
        header_layout = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            # Redimensionner le logo (hauteur de 60px)
            scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        else:
            # Si le logo n'existe pas, afficher un emoji
            logo_label.setText("🖨️")
            logo_label.setFont(QFont("Arial", 40))
        
        logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(logo_label)
        
        # Titre et date
        title_date_layout = QVBoxLayout()
        title_date_layout.setSpacing(5)
        
        title_label = QLabel("Bureautique")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet(f"color: {COLOR_PRIMARY}; background-color: transparent;")
        title_date_layout.addWidget(title_label)
        
        date_label = QLabel(f"{datetime.now().strftime('%A %d %B %Y')}")
        date_label.setFont(QFont("Arial", 12))
        date_label.setStyleSheet(f"color: {COLOR_SECONDARY}; background-color: transparent;")
        title_date_layout.addWidget(date_label)
        
        header_layout.addLayout(title_date_layout)
        header_layout.addStretch()
        
        # Montant en caisse dans le coin droit haut
        self.caisse_container = QWidget()
        self.caisse_container.setStyleSheet("background-color: transparent;")
        caisse_layout = QVBoxLayout()
        caisse_layout.setContentsMargins(0, 0, 0, 0)
        caisse_layout.setSpacing(0)
        
        # Montant
        self.rapport_montant_caisse = QLabel("0.00 FC")
        self.rapport_montant_caisse.setFont(QFont("Arial", 40, QFont.Bold))
        self.rapport_montant_caisse.setStyleSheet("color: #2E86AB; background-color: transparent;")
        self.rapport_montant_caisse.setAlignment(Qt.AlignRight)
        caisse_layout.addWidget(self.rapport_montant_caisse)
        
        self.caisse_container.setLayout(caisse_layout)
        header_layout.addWidget(self.caisse_container)
        
        # Masquer le montant en caisse par défaut (onglet Accueil)
        self.caisse_container.setVisible(False)
        
        main_layout.addLayout(header_layout)
        
        # Créer les onglets
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: transparent;
            }
            QTabBar::tab {
                background-color: white;
                color: #666;
                padding: 10px 20px;
                margin-right: 5px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-size: 12px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #2E86AB;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #B3D9FF;
            }
        """)
        
        # Onglet Principal (Accueil)
        main_tab = QWidget()
        main_tab_layout = QVBoxLayout()
        main_tab_layout.setContentsMargins(0, 0, 0, 0)
        main_tab.setLayout(main_tab_layout)
        
        # Utiliser la classe AccueilTab
        self.accueil_tab_widget = AccueilTab(self.db, self)
        main_tab_layout.addWidget(self.accueil_tab_widget)
        
        # Onglet Rapports
        rapports_tab = QWidget()
        rapports_scroll = QScrollArea()
        rapports_scroll.setWidgetResizable(True)
        rapports_scroll.setFrameShape(QFrame.NoFrame)
        
        rapports_content = QWidget()
        rapports_layout = QVBoxLayout()
        rapports_layout.setContentsMargins(0, 0, 0, 0)
        rapports_layout.setSpacing(0)
        rapports_content.setLayout(rapports_layout)
        
        # Utiliser la classe RapportsTab
        self.rapports_tab_widget = RapportsTab(self.db, self)
        rapports_layout.addWidget(self.rapports_tab_widget)
        
        rapports_scroll.setWidget(rapports_content)
        
        rapports_main_layout = QVBoxLayout()
        rapports_main_layout.setContentsMargins(0, 0, 0, 0)
        rapports_main_layout.addWidget(rapports_scroll)
        rapports_tab.setLayout(rapports_main_layout)
        
        # Onglet Caisse
        caisse_tab = QWidget()
        caisse_scroll = QScrollArea()
        caisse_scroll.setWidgetResizable(True)
        caisse_scroll.setFrameShape(QFrame.NoFrame)
        
        caisse_content = QWidget()
        caisse_layout = QVBoxLayout()
        caisse_layout.setContentsMargins(0, 0, 0, 0)
        caisse_layout.setSpacing(20)
        caisse_content.setLayout(caisse_layout)
        
        # Utiliser la classe CaisseTab
        self.caisse_tab_widget = CaisseTab(self.db, self)
        caisse_layout.addWidget(self.caisse_tab_widget)
        
        caisse_scroll.setWidget(caisse_content)
        
        caisse_main_layout = QVBoxLayout()
        caisse_main_layout.setContentsMargins(0, 0, 0, 0)
        caisse_main_layout.addWidget(caisse_scroll)
        caisse_tab.setLayout(caisse_main_layout)
        
        # Ajouter les onglets
        self.tabs.addTab(main_tab, "🏠 Accueil")
        self.tabs.addTab(rapports_tab, "📊 Rapports")
        self.tabs.addTab(caisse_tab, "💰 Caisse")
        
        # Toolbar avec boutons à côté des onglets
        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)
        
        # Bouton pour afficher/masquer le formulaire de nouvelle transaction
        self.toggle_form_button = QPushButton("➕ Transaction")
        self.toggle_form_button.setFont(QFont("Arial", 9, QFont.Bold))
        self.toggle_form_button.setCursor(Qt.PointingHandCursor)
        self.toggle_form_button.setFixedSize(120, 35)
        self.toggle_form_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_SUCCESS};
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #058A65;
            }}
        """)
        self.toggle_form_button.clicked.connect(self.toggle_transaction_form)
        toolbar_layout.addWidget(self.toggle_form_button)
        
        # Affichage du montant en caisse (visible uniquement dans l'onglet Caisse)
        self.caisse_header_widget = QWidget()
        caisse_header_layout = QHBoxLayout(self.caisse_header_widget)
        caisse_header_layout.setContentsMargins(15, 0, 15, 0)
        caisse_header_layout.setSpacing(10)
        
        
        self.caisse_header_montant = QLabel("0 FC")
        self.caisse_header_montant.setFont(QFont("Arial", 36, QFont.Bold))
        self.caisse_header_montant.setStyleSheet(f"color: {COLOR_PRIMARY};")
        self.caisse_header_montant.setAlignment(Qt.AlignVCenter)
        caisse_header_layout.addWidget(self.caisse_header_montant)
        
        self.caisse_header_widget.setVisible(False)
        toolbar_layout.addWidget(self.caisse_header_widget, 0, Qt.AlignVCenter)
        
        toolbar_widget.setLayout(toolbar_layout)
        
        # Stocker le toolbar_widget pour pouvoir le gérer
        self.toolbar_widget = toolbar_widget
        
        # Connecter le changement d'onglet pour afficher/masquer les boutons
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
        # Positionner la toolbar en haut à droite des onglets
        self.tabs.setCornerWidget(toolbar_widget, Qt.TopRightCorner)
        
        # Connecter le changement d'onglet pour gérer la visibilité des boutons
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
        main_layout.addWidget(self.tabs)
        
    def create_stats_frame(self, parent_layout):
        """Créer le frame des statistiques"""
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)
        
        # Solde disponible
        self.solde_frame = QFrame()
        self.solde_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_SUCCESS};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        solde_layout = QVBoxLayout()
        
        solde_title = QLabel("💰 Solde Disponible")
        solde_title.setFont(QFont("Arial", 12, QFont.Bold))
        solde_title.setStyleSheet("color: white; background-color: transparent;")
        solde_title.setAlignment(Qt.AlignCenter)
        
        self.solde_label = QLabel("0.00 FC")
        self.solde_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.solde_label.setStyleSheet("color: white; background-color: transparent;")
        self.solde_label.setAlignment(Qt.AlignCenter)
        
        solde_layout.addWidget(solde_title)
        solde_layout.addWidget(self.solde_label)
        self.solde_frame.setLayout(solde_layout)
        stats_layout.addWidget(self.solde_frame)
        
        # Total recettes
        recettes_frame = QFrame()
        recettes_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_PRIMARY};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        recettes_layout = QVBoxLayout()
        
        recettes_title = QLabel("📈 Recette")
        recettes_title.setFont(QFont("Arial", 12, QFont.Bold))
        recettes_title.setStyleSheet("color: white; background-color: transparent;")
        recettes_title.setAlignment(Qt.AlignCenter)
        
        self.recettes_label = QLabel("0.00 FC")
        self.recettes_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.recettes_label.setStyleSheet("color: white; background-color: transparent;")
        self.recettes_label.setAlignment(Qt.AlignCenter)
        
        recettes_layout.addWidget(recettes_title)
        recettes_layout.addWidget(self.recettes_label)
        recettes_frame.setLayout(recettes_layout)
        stats_layout.addWidget(recettes_frame)
        
        # Total dépenses
        depenses_frame = QFrame()
        depenses_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_DANGER};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        depenses_layout = QVBoxLayout()
        
        depenses_title = QLabel("📉 Dépenses")
        depenses_title.setFont(QFont("Arial", 12, QFont.Bold))
        depenses_title.setStyleSheet("color: white; background-color: transparent;")
        depenses_title.setAlignment(Qt.AlignCenter)
        
        self.depenses_label = QLabel("0.00 FC")
        self.depenses_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.depenses_label.setStyleSheet("color: white; background-color: transparent;")
        self.depenses_label.setAlignment(Qt.AlignCenter)
        
        depenses_layout.addWidget(depenses_title)
        depenses_layout.addWidget(self.depenses_label)
        depenses_frame.setLayout(depenses_layout)
        stats_layout.addWidget(depenses_frame)
        
        parent_layout.addLayout(stats_layout)
        
        # Bouton de clôture/réouverture du rapport journalier
        cloture_layout = QHBoxLayout()
        cloture_layout.setSpacing(10)
        
        self.cloture_button = QPushButton("🔒 Clôturer le rapport du jour")
        self.cloture_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.cloture_button.setCursor(Qt.PointingHandCursor)
        self.cloture_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_SECONDARY};
                color: white;
                padding: 12px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #8B2F5E;
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """)
        self.cloture_button.clicked.connect(self.toggle_cloture_rapport)
        cloture_layout.addWidget(self.cloture_button)
        
        self.cloture_status = QLabel("")
        self.cloture_status.setFont(QFont("Arial", 11))
        self.cloture_status.setStyleSheet("background-color: transparent;")
        cloture_layout.addWidget(self.cloture_status)
        
        cloture_layout.addStretch()
        parent_layout.addLayout(cloture_layout)
        
    def create_transaction_frame(self, parent_layout):
        """Créer le frame pour l'ajout de transactions"""
        self.transaction_frame = QFrame()
        self.transaction_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #ddd;
            }
        """)
        self.transaction_frame.setVisible(False)  # Masqué par défaut
        
        transaction_layout = QVBoxLayout()
        transaction_layout.setContentsMargins(20, 20, 20, 20)
        transaction_layout.setSpacing(15)
        
        # Titre
        title = QLabel("Nouvelle Transaction")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet(f"color: {COLOR_PRIMARY}; background-color: transparent; border: none;")
        transaction_layout.addWidget(title)
        
        # Type de transaction
        type_layout = QHBoxLayout()
        type_label = QLabel("Type:")
        type_label.setFont(QFont("Arial", 11))
        type_label.setStyleSheet("background-color: transparent; border: none;")
        type_layout.addWidget(type_label)
        
        self.type_group = QButtonGroup()
        self.recette_radio = QRadioButton("Recette")
        self.depense_radio = QRadioButton("Dépense")
        self.recette_radio.setChecked(True)
        self.recette_radio.setFont(QFont("Arial", 10))
        self.depense_radio.setFont(QFont("Arial", 10))
        self.recette_radio.setStyleSheet(f"background-color: transparent; border: none; color: {COLOR_SUCCESS};")
        self.depense_radio.setStyleSheet(f"background-color: transparent; border: none; color: {COLOR_DANGER};")
        
        self.type_group.addButton(self.recette_radio, 1)
        self.type_group.addButton(self.depense_radio, 2)
        
        type_layout.addWidget(self.recette_radio)
        type_layout.addWidget(self.depense_radio)
        type_layout.addStretch()
        transaction_layout.addLayout(type_layout)
        
        # Montant
        montant_layout = QHBoxLayout()
        montant_label = QLabel("Montant:")
        montant_label.setFont(QFont("Arial", 11))
        montant_label.setStyleSheet("background-color: transparent; border: none;")
        montant_label.setFixedWidth(100)
        montant_layout.addWidget(montant_label)
        
        self.montant_entry = QLineEdit()
        self.montant_entry.setFont(QFont("Arial", 11))
        self.montant_entry.setPlaceholderText("Entrez le montant")
        self.montant_entry.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2E86AB;
            }
        """)
        montant_layout.addWidget(self.montant_entry)
        transaction_layout.addLayout(montant_layout)
        
        # Description
        desc_layout = QHBoxLayout()
        desc_label = QLabel("Description:")
        desc_label.setFont(QFont("Arial", 11))
        desc_label.setStyleSheet("background-color: transparent; border: none;")
        desc_label.setFixedWidth(100)
        desc_layout.addWidget(desc_label)
        
        self.description_entry = QLineEdit()
        self.description_entry.setFont(QFont("Arial", 11))
        self.description_entry.setPlaceholderText("Description (optionnel)")
        self.description_entry.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2E86AB;
            }
        """)
        desc_layout.addWidget(self.description_entry)
        transaction_layout.addLayout(desc_layout)
        
        # Bouton d'ajout
        add_button = QPushButton("➕ Ajouter la transaction")
        add_button.setFont(QFont("Arial", 12, QFont.Bold))
        add_button.setCursor(Qt.PointingHandCursor)
        add_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                padding: 12px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #236B8E;
            }}
            QPushButton:pressed {{
                background-color: #1A5270;
            }}
        """)
        add_button.clicked.connect(self.ajouter_transaction)
        transaction_layout.addWidget(add_button)
        
        self.transaction_frame.setLayout(transaction_layout)
        parent_layout.addWidget(self.transaction_frame)
    
    def on_tab_changed(self, index):
        """Gérer le changement d'onglet pour afficher/masquer les boutons de la toolbar"""
        # index 0 = Accueil, 1 = Rapports, 2 = Caisse
        if index == 0:  # Onglet Accueil uniquement
            # Afficher les boutons dans l'onglet Accueil
            self.toggle_form_button.setVisible(True)
            # Masquer le montant en caisse
            self.caisse_container.setVisible(False)
        elif index == 1:  # Onglet Rapports
            # Masquer les boutons
            self.toggle_form_button.setVisible(False)
            # Afficher le montant en caisse
            self.caisse_container.setVisible(True)
        else:  # Onglet Caisse
            # Masquer les boutons
            self.toggle_form_button.setVisible(False)
            # Masquer le montant en caisse
            self.caisse_container.setVisible(False)
    
    def toggle_transaction_form(self):
        """Afficher/masquer les formulaires de transaction"""
        # Utiliser la méthode du widget AccueilTab
        if hasattr(self, 'accueil_tab_widget'):
            self.accueil_tab_widget.toggle_transaction_form()
    
    def on_tab_changed(self, index):
        """Gérer le changement d'onglet pour afficher/masquer les boutons appropriés"""
        # Masquer tous les boutons par défaut
        self.toggle_form_button.setVisible(False)
        self.caisse_header_widget.setVisible(False)
        
        # Afficher les boutons selon l'onglet actif
        if index == 0:  # Onglet Accueil
            self.toggle_form_button.setVisible(True)
        elif index == 2:  # Onglet Caisse
            self.caisse_header_widget.setVisible(True)
            self.actualiser_caisse_header()
    
    def create_history_frame(self, parent_layout):
        """Créer le frame pour l'historique des transactions"""
        history_frame = QFrame()
        history_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #ddd;
            }
        """)
        
        history_layout = QVBoxLayout()
        history_layout.setContentsMargins(20, 20, 20, 20)
        history_layout.setSpacing(10)
        
        # Titre
        title = QLabel("Historique des Transactions")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet(f"color: {COLOR_PRIMARY}; background-color: transparent; border: none;")
        history_layout.addWidget(title)
        
        # Barre d'outils
        toolbar_layout = QHBoxLayout()
        
        refresh_button = QPushButton("Actualiser")
        refresh_button.setFont(QFont("Arial", 10, QFont.Bold))
        refresh_button.setCursor(Qt.PointingHandCursor)
        refresh_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                border: none;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: #236B8E;
            }}
        """)
        refresh_button.clicked.connect(self.actualiser_affichage)
        toolbar_layout.addWidget(refresh_button)
        
        modify_button = QPushButton("Modifier")
        modify_button.setFont(QFont("Arial", 10, QFont.Bold))
        modify_button.setCursor(Qt.PointingHandCursor)
        modify_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_SECONDARY};
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                border: none;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: #8B2F5E;
            }}
        """)
        modify_button.clicked.connect(self.modifier_transaction)
        toolbar_layout.addWidget(modify_button)
        
        delete_button = QPushButton("Supprimer")
        delete_button.setFont(QFont("Arial", 10, QFont.Bold))
        delete_button.setCursor(Qt.PointingHandCursor)
        delete_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_DANGER};
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                border: none;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: #B01C3A;
            }}
        """)
        delete_button.clicked.connect(self.supprimer_transaction)
        toolbar_layout.addWidget(delete_button)
        
        toolbar_layout.addStretch()
        history_layout.addLayout(toolbar_layout)
        
        # Table des transactions
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Type", "Montant (FC)", "Description", "Date", "Heure"])
        self.table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #2E86AB;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                gridline-color: #ddd;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #B3D9FF;
                color: black;
            }
        """)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        
        # Ajuster la largeur des colonnes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        history_layout.addWidget(self.table)
        
        history_frame.setLayout(history_layout)
        parent_layout.addWidget(history_frame)
        
    def ajouter_transaction(self):
        """Ajouter une nouvelle transaction"""
        try:
            # Vérifier si le rapport affiché est clôturé
            date_rapport = self.accueil_tab_widget.date_courante
            est_cloture = self.db.verifier_cloture(date_rapport)
            
            # Vérifier si c'est aujourd'hui
            date_aujourdhui = datetime.now().strftime("%Y-%m-%d")
            est_aujourdhui = date_rapport == date_aujourdhui
            
            if not est_aujourdhui:
                QMessageBox.warning(
                    self,
                    "Rapport archivé",
                    "Vous consultez un rapport archivé. Impossible d'ajouter des transactions.\n\nRetournez au rapport du jour pour ajouter des transactions."
                )
                return False
            
            if est_cloture:
                QMessageBox.warning(
                    self,
                    "Rapport clôturé",
                    "Le rapport du jour est clôturé. Impossible d'ajouter des transactions journalières.\n\nVeuillez rouvrir le rapport si vous souhaitez modifier les données du jour."
                )
                return False
            
            # Récupérer les valeurs depuis AccueilTab
            if hasattr(self, 'accueil_tab_widget') and hasattr(self.accueil_tab_widget, 'recette_radio'):
                type_transaction = "recette" if self.accueil_tab_widget.recette_radio.isChecked() else "depense"
                montant_text = self.accueil_tab_widget.montant_entry.text().strip()
            else:
                # Fallback si les champs ne sont pas disponibles
                QMessageBox.warning(self, "Erreur", "Le formulaire de transaction n'est pas disponible")
                return False
            
            if not montant_text:
                QMessageBox.warning(self, "Attention", "Veuillez entrer un montant")
                return False
                
            montant = float(montant_text)
            description = self.accueil_tab_widget.description_entry.text().strip()
            
            # Vérifier que la description est remplie
            if not description:
                QMessageBox.warning(self, "Attention", "Veuillez entrer une description")
                return False
            
            # Les transactions de l'onglet Accueil sont toujours normales (journalières)
            type_depense = "normale"
            
            if montant <= 0:
                QMessageBox.critical(self, "Erreur", "Le montant doit être supérieur à 0")
                return False
            
            # Ajouter dans la base de données
            self.db.ajouter_transaction(type_transaction, montant, description, type_depense)
            
            # Réinitialiser les champs
            self.accueil_tab_widget.montant_entry.clear()
            self.accueil_tab_widget.description_entry.clear()
            self.accueil_tab_widget.recette_radio.setChecked(True)
            
            # Actualiser l'affichage
            self.actualiser_affichage()
            self.actualiser_dashboard()
            self.actualiser_caisse()
            
            QMessageBox.information(self, "Succès", "Transaction ajoutée avec succès!")
            return True
            
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer un montant valide")
            return False
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {str(e)}")
            return False
            
    def actualiser_affichage(self):
        """Actualiser l'affichage des statistiques et de l'historique"""
        # Déléguer à AccueilTab
        if hasattr(self, 'accueil_tab_widget'):
            self.accueil_tab_widget.actualiser_affichage()
        
    def modifier_transaction(self):
        """Modifier la transaction sélectionnée"""
        # Utiliser le tableau de AccueilTab
        if not hasattr(self, 'accueil_tab_widget') or not hasattr(self.accueil_tab_widget, 'table'):
            QMessageBox.warning(self, "Erreur", "Le tableau des transactions n'est pas disponible")
            return
            
        current_row = self.accueil_tab_widget.table.currentRow()
        
        if current_row < 0:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner une transaction à modifier")
            return
        
        try:
            # Récupérer l'ID de la transaction (stocké dans Qt.UserRole)
            transaction_id = self.accueil_tab_widget.table.item(current_row, 0).data(Qt.UserRole)
            
            # Obtenir les détails de la transaction
            transaction = self.db.obtenir_transaction(transaction_id)
            
            if not transaction:
                QMessageBox.warning(self, "Erreur", "Transaction introuvable")
                return
            
            # Vérifier si c'est une transaction normale (journalière)
            type_depense = transaction[6] if len(transaction) > 6 else "normale"
            
            if type_depense == "normale":
                # Vérifier si le rapport affiché est clôturé
                date_rapport = self.accueil_tab_widget.date_courante
                est_cloture = self.db.verifier_cloture(date_rapport)
                
                # Vérifier si c'est aujourd'hui
                date_aujourdhui = datetime.now().strftime("%Y-%m-%d")
                est_aujourdhui = date_rapport == date_aujourdhui
                
                if not est_aujourdhui:
                    QMessageBox.warning(
                        self,
                        "Rapport archivé",
                        "Vous consultez un rapport archivé. Impossible de modifier les transactions.\n\nRetournez au rapport du jour pour modifier des transactions."
                    )
                    return
                
                if est_cloture:
                    QMessageBox.warning(
                        self,
                        "Rapport clôturé",
                        "Le rapport du jour est clôturé. Impossible de modifier les transactions journalières.\n\nVeuillez rouvrir le rapport si vous souhaitez modifier les données du jour."
                    )
                    return
            
            # Ouvrir une fenêtre de dialogue pour modifier
            dialog = ModifierTransactionDialog(self, transaction)
            
            if dialog.exec_() == QDialog.Accepted:
                # Récupérer les nouvelles valeurs
                type_trans, montant, description, type_depense = dialog.get_values()
                
                # Mettre à jour dans la base de données
                self.db.modifier_transaction(transaction_id, type_trans, montant, description, type_depense)
                
                # Actualiser l'affichage
                self.actualiser_affichage()
                self.actualiser_dashboard()
                self.actualiser_caisse()
                
                QMessageBox.information(self, "Succès", "Transaction modifiée avec succès!")
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {str(e)}")
        
    def supprimer_transaction(self):
        """Supprimer la transaction sélectionnée"""
        # Utiliser le tableau de AccueilTab
        if not hasattr(self, 'accueil_tab_widget') or not hasattr(self.accueil_tab_widget, 'table'):
            QMessageBox.warning(self, "Erreur", "Le tableau des transactions n'est pas disponible")
            return
            
        current_row = self.accueil_tab_widget.table.currentRow()
        
        if current_row < 0:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner une transaction à supprimer")
            return
        
        try:
            # Récupérer l'ID de la transaction (stocké dans Qt.UserRole)
            transaction_id = self.accueil_tab_widget.table.item(current_row, 0).data(Qt.UserRole)
            
            # Obtenir les détails de la transaction pour vérifier le type
            transaction = self.db.obtenir_transaction(transaction_id)
            
            if not transaction:
                QMessageBox.warning(self, "Erreur", "Transaction introuvable")
                return
            
            # Vérifier si c'est une transaction normale (journalière)
            type_depense = transaction[6] if len(transaction) > 6 else "normale"
            
            if type_depense == "normale":
                # Vérifier si le rapport affiché est clôturé
                date_rapport = self.accueil_tab_widget.date_courante
                est_cloture = self.db.verifier_cloture(date_rapport)
                
                # Vérifier si c'est aujourd'hui
                date_aujourdhui = datetime.now().strftime("%Y-%m-%d")
                est_aujourdhui = date_rapport == date_aujourdhui
                
                if not est_aujourdhui:
                    QMessageBox.warning(
                        self,
                        "Rapport archivé",
                        "Vous consultez un rapport archivé. Impossible de supprimer les transactions.\n\nRetournez au rapport du jour pour supprimer des transactions."
                    )
                    return
                
                if est_cloture:
                    QMessageBox.warning(
                        self,
                        "Rapport clôturé",
                        "Le rapport du jour est clôturé. Impossible de supprimer les transactions journalières.\n\nVeuillez rouvrir le rapport si vous souhaitez modifier les données du jour."
                    )
                    return
            
            # Confirmer la suppression
            reply = QMessageBox.question(
                self, 
                "Confirmation", 
                "Voulez-vous vraiment supprimer cette transaction?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Supprimer de la base de données
                self.db.supprimer_transaction(transaction_id)
                
                # Actualiser l'affichage
                self.actualiser_affichage()
                self.actualiser_dashboard()
                self.actualiser_caisse()
                
                QMessageBox.information(self, "Succès", "Transaction supprimée avec succès!")
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {str(e)}")
                
    def toggle_cloture_rapport(self):
        """Clôturer ou rouvrir le rapport de la journée"""
        # Utiliser la date courante de l'onglet accueil
        date_rapport = self.accueil_tab_widget.date_courante
        est_cloture = self.db.verifier_cloture(date_rapport)
        
        # Adapter le message selon la date
        est_aujourdhui = date_rapport == datetime.now().strftime("%Y-%m-%d")
        date_format = datetime.strptime(date_rapport, "%Y-%m-%d").strftime("%d/%m/%Y")
        
        if est_cloture:
            # Rouvrir le rapport
            message = f"Voulez-vous rouvrir le rapport du {date_format}?\n\nCela permettra de modifier les transactions et le solde ne sera plus visible dans la caisse."
            reply = QMessageBox.question(
                self,
                "Confirmation de réouverture",
                message,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                try:
                    self.db.rouvrir_rapport(date_rapport)
                    QMessageBox.information(self, "Succès", f"Le rapport du {date_format} a été rouvert avec succès!")
                    self.actualiser_affichage()
                    self.actualiser_dashboard()
                    self.actualiser_caisse()
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {str(e)}")
        else:
            # Clôturer le rapport
            # Vérifier s'il y a des transactions pour cette date
            transactions = self.db.obtenir_transactions(date_rapport)
            
            if not transactions:
                QMessageBox.warning(self, "Attention", f"Aucune transaction pour le {date_format}. Impossible de clôturer le rapport.")
                return
            
            # Vérifier s'il y a des recettes
            stats = self.db.calculer_solde(date_rapport)
            
            if stats['recettes'] == 0:
                QMessageBox.warning(
                    self, 
                    "Journée sans recette", 
                    "La recette du jour est égale à 0.\n\nLa journée est considérée comme néant et ne peut pas être clôturée.\n\nSupprimez les transactions si nécessaire."
                )
                return
            
            # Demander confirmation
            message = f"Voulez-vous clôturer le rapport du jour?\n\n"
            message += f"Recettes: {stats['recettes']:,.0f} FC\n"
            message += f"Dépenses: {stats['depenses']:,.0f} FC\n"
            message += f"Solde: {stats['solde']:,.0f} FC\n\n"
            message += "Une fois clôturé, le solde sera ajouté à la caisse."
            
            reply = QMessageBox.question(
                self,
                "Confirmation de clôture",
                message,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                try:
                    self.db.cloturer_rapport(date_rapport)
                    QMessageBox.information(self, "Succès", f"Le rapport du {date_format} a été clôturé avec succès!")
                    self.actualiser_affichage()
                    self.actualiser_dashboard()
                    self.actualiser_caisse()
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {str(e)}")
                
    def create_rapports_tab(self, parent_layout):
        """Créer l'onglet des rapports avec statistiques et génération PDF"""
        # Section 1: Statistiques par période
        self.create_stats_period_section(parent_layout)
        
        # Section 2: Génération de rapports PDF
        self.create_generation_pdf_section(parent_layout)
        
        parent_layout.addStretch()
    
    def create_stats_period_section(self, parent_layout):
        """Créer la section des statistiques par période"""
        # Frame pour les filtres
        filter_frame = QFrame()
        filter_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #ddd;
            }
        """)
        
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(20, 15, 20, 15)
        filter_layout.setSpacing(15)
        
        # Label période
        filter_label = QLabel("Période:")
        filter_label.setFont(QFont("Arial", 11, QFont.Bold))
        filter_label.setStyleSheet("background-color: transparent; border: none;")
        filter_layout.addWidget(filter_label)
        
        # ComboBox pour le filtre de période
        self.period_filter = QComboBox()
        self.period_filter.addItems(["Aujourd'hui", "Cette semaine", "Ce mois", "Cette année", "Tout"])
        self.period_filter.setFont(QFont("Arial", 10))
        self.period_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 150px;
            }
            QComboBox:hover {
                border: 2px solid #2E86AB;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.period_filter.currentTextChanged.connect(self.on_period_filter_changed)
        filter_layout.addWidget(self.period_filter)
        
        # Séparateur
        separator = QLabel("|")
        separator.setFont(QFont("Arial", 14))
        separator.setStyleSheet("color: #ddd; background-color: transparent; border: none;")
        filter_layout.addWidget(separator)
        
        # Label mois
        month_label = QLabel("Mois:")
        month_label.setFont(QFont("Arial", 11, QFont.Bold))
        month_label.setStyleSheet("background-color: transparent; border: none;")
        filter_layout.addWidget(month_label)
        
        # ComboBox pour le filtre de mois
        self.month_filter = QComboBox()
        mois = [
            "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
        ]
        self.month_filter.addItems(mois)
        # Sélectionner le mois actuel par défaut
        self.month_filter.setCurrentIndex(datetime.now().month - 1)
        self.month_filter.setFont(QFont("Arial", 10))
        self.month_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 120px;
            }
            QComboBox:hover {
                border: 2px solid #2E86AB;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.month_filter.currentIndexChanged.connect(self.on_month_filter_changed)
        filter_layout.addWidget(self.month_filter)
        
        # Année pour le filtre de mois
        self.year_filter = QComboBox()
        annee_actuelle = datetime.now().year
        for year in range(annee_actuelle - 5, annee_actuelle + 1):
            self.year_filter.addItem(str(year))
        self.year_filter.setCurrentText(str(annee_actuelle))
        self.year_filter.setFont(QFont("Arial", 10))
        self.year_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 80px;
            }
            QComboBox:hover {
                border: 2px solid #2E86AB;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.year_filter.currentIndexChanged.connect(self.on_month_filter_changed)
        filter_layout.addWidget(self.year_filter)
        
        # Séparateur
        separator2 = QLabel("|")
        separator2.setFont(QFont("Arial", 14))
        separator2.setStyleSheet("color: #ddd; background-color: transparent; border: none;")
        filter_layout.addWidget(separator2)
        
        # Label date spécifique
        date_label = QLabel("Date spécifique:")
        date_label.setFont(QFont("Arial", 11, QFont.Bold))
        date_label.setStyleSheet("background-color: transparent; border: none;")
        filter_layout.addWidget(date_label)
        
        # DateEdit pour sélectionner une date spécifique
        from PyQt5.QtWidgets import QDateEdit
        from PyQt5.QtCore import QDate
        
        self.date_filter = QDateEdit()
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setFont(QFont("Arial", 10))
        self.date_filter.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 150px;
            }
            QDateEdit:hover {
                border: 2px solid #2E86AB;
            }
        """)
        self.date_filter.dateChanged.connect(self.on_date_filter_changed)
        filter_layout.addWidget(self.date_filter)
        
        # Bouton pour afficher la date sélectionnée
        show_date_button = QPushButton("📅 Afficher")
        show_date_button.setFont(QFont("Arial", 10, QFont.Bold))
        show_date_button.setCursor(Qt.PointingHandCursor)
        show_date_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #236B8E;
            }}
        """)
        show_date_button.clicked.connect(self.afficher_rapport_date)
        filter_layout.addWidget(show_date_button)
        
        filter_layout.addStretch()
        filter_frame.setLayout(filter_layout)
        parent_layout.addWidget(filter_frame)
        
        # Frame pour les statistiques
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            }
        """)
        
        stats_layout = QVBoxLayout()
        stats_layout.setContentsMargins(20, 20, 20, 20)
        stats_layout.setSpacing(15)
        
        # Titre
        stats_title = QLabel("Résumé de la période")
        stats_title.setFont(QFont("Arial", 14, QFont.Bold))
        stats_title.setStyleSheet(f"color: {COLOR_PRIMARY}; background-color: transparent; border: none;")
        stats_layout.addWidget(stats_title)
        
        # Stats en ligne
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(15)
        
        # Total Recettes
        recettes_card = QFrame()
        recettes_card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #10b981, stop:1 {COLOR_SUCCESS});
                border-radius: 12px;
                padding: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
        """)
        recettes_card_layout = QVBoxLayout()
        recettes_card_layout.setSpacing(8)
        
        recettes_title = QLabel("💰 Recette")
        recettes_title.setFont(QFont("Arial", 11, QFont.Bold))
        recettes_title.setStyleSheet("color: rgba(255, 255, 255, 0.95); background-color: transparent;")
        recettes_card_layout.addWidget(recettes_title)
        
        self.dashboard_recettes = QLabel("0.00 FC")
        self.dashboard_recettes.setFont(QFont("Arial", 20, QFont.Bold))
        self.dashboard_recettes.setStyleSheet("color: white; background-color: transparent;")
        recettes_card_layout.addWidget(self.dashboard_recettes)
        
        recettes_card.setLayout(recettes_card_layout)
        summary_layout.addWidget(recettes_card)
        
        # Total Dépenses
        depenses_card = QFrame()
        depenses_card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ef4444, stop:1 {COLOR_DANGER});
                border-radius: 12px;
                padding: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
        """)
        depenses_card_layout = QVBoxLayout()
        depenses_card_layout.setSpacing(8)
        
        depenses_title = QLabel("💸 Dépenses")
        depenses_title.setFont(QFont("Arial", 11, QFont.Bold))
        depenses_title.setStyleSheet("color: rgba(255, 255, 255, 0.95); background-color: transparent;")
        depenses_card_layout.addWidget(depenses_title)
        
        self.dashboard_depenses = QLabel("0.00 FC")
        self.dashboard_depenses.setFont(QFont("Arial", 20, QFont.Bold))
        self.dashboard_depenses.setStyleSheet("color: white; background-color: transparent;")
        depenses_card_layout.addWidget(self.dashboard_depenses)
        
        depenses_card.setLayout(depenses_card_layout)
        summary_layout.addWidget(depenses_card)
        
        # Résultat
        resultat_card = QFrame()
        resultat_card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b82f6, stop:1 {COLOR_PRIMARY});
                border-radius: 12px;
                padding: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
        """)
        resultat_card_layout = QVBoxLayout()
        resultat_card_layout.setSpacing(8)
        
        resultat_title = QLabel("📈 Solde")
        resultat_title.setFont(QFont("Arial", 11, QFont.Bold))
        resultat_title.setStyleSheet("color: rgba(255, 255, 255, 0.95); background-color: transparent;")
        resultat_card_layout.addWidget(resultat_title)
        
        self.dashboard_resultat = QLabel("0.00 FC")
        self.dashboard_resultat.setFont(QFont("Arial", 20, QFont.Bold))
        self.dashboard_resultat.setStyleSheet("color: white; background-color: transparent;")
        resultat_card_layout.addWidget(self.dashboard_resultat)
        
        resultat_card.setLayout(resultat_card_layout)
        summary_layout.addWidget(resultat_card)
        
        stats_layout.addLayout(summary_layout)
        
        # Tableau des jours
        self.dashboard_table = QTableWidget()
        self.dashboard_table.setColumnCount(4)
        self.dashboard_table.setHorizontalHeaderLabels(["Date", "Recettes", "Dépenses", "Solde"])
        self.dashboard_table.horizontalHeader().setFont(QFont("Arial", 10, QFont.Bold))
        self.dashboard_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                gridline-color: #f0f0f0;
                alternate-background-color: #f8f9fc;
            }
            QHeaderView::section {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3498db, stop:1 #2E86AB);
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #f5f5f5;
            }
            QTableWidget::item:selected {
                background-color: #d4e8f5;
                color: #1a1a1a;
            }
        """)
        self.dashboard_table.horizontalHeader().setStretchLastSection(False)
        self.dashboard_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.dashboard_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.dashboard_table.setAlternatingRowColors(True)
        self.dashboard_table.verticalHeader().setVisible(False)
        
        # Configurer les colonnes pour qu'elles restent statiques et occupent toute la largeur
        header = self.dashboard_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Date - flexible
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Recettes - flexible
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Dépenses - flexible
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # Solde - flexible
        header.setStretchLastSection(True)
        
        # Agrandir le tableau pour plus de visibilité
        self.dashboard_table.setMinimumHeight(500)
        
        stats_layout.addWidget(self.dashboard_table)
        
        stats_frame.setLayout(stats_layout)
        parent_layout.addWidget(stats_frame)
    
    def create_generation_pdf_section(self, parent_layout):
        """Créer la section de génération de rapports PDF"""
        pdf_frame = QFrame()
        pdf_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            }
        """)
        
        pdf_layout = QVBoxLayout()
        pdf_layout.setContentsMargins(20, 20, 20, 20)
        pdf_layout.setSpacing(15)
        
        # Ligne avec titre et bouton masquer
        title_button_layout = QHBoxLayout()
        
        pdf_title = QLabel("📄 Génération de Rapports PDF")
        pdf_title.setFont(QFont("Arial", 14, QFont.Bold))
        pdf_title.setStyleSheet(f"color: {COLOR_PRIMARY}; background-color: transparent; border: none;")
        title_button_layout.addWidget(pdf_title)
        
        # Bouton masquer/afficher
        self.pdf_section_visible = True
        self.toggle_pdf_btn = QPushButton("▲ Masquer")
        self.toggle_pdf_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.toggle_pdf_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_pdf_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #0056b3;
            }}
        """)
        self.toggle_pdf_btn.clicked.connect(self.toggle_pdf_section)
        title_button_layout.addStretch()
        title_button_layout.addWidget(self.toggle_pdf_btn)
        
        pdf_layout.addLayout(title_button_layout)
        
        # Container pour le contenu PDF
        self.pdf_content_container = QWidget()
        pdf_content_layout = QVBoxLayout()
        pdf_content_layout.setContentsMargins(0, 0, 0, 0)
        pdf_content_layout.setSpacing(15)
        self.pdf_content_container.setLayout(pdf_content_layout)
        
        # Description
        pdf_desc = QLabel("Générez des rapports PDF pour les journées clôturées ou par période")
        pdf_desc.setFont(QFont("Arial", 10))
        pdf_desc.setStyleSheet("color: #666; background-color: transparent; border: none;")
        pdf_content_layout.addWidget(pdf_desc)
        
        # Section 1: Rapport journalier
        jour_layout = QHBoxLayout()
        
        jour_label = QLabel("📅 Rapport Journalier:")
        jour_label.setFont(QFont("Arial", 11, QFont.Bold))
        jour_label.setStyleSheet("background-color: transparent; border: none;")
        jour_layout.addWidget(jour_label)
        
        from PyQt5.QtWidgets import QDateEdit
        from PyQt5.QtCore import QDate
        
        self.pdf_date_picker = QDateEdit()
        self.pdf_date_picker.setDate(QDate.currentDate())
        self.pdf_date_picker.setCalendarPopup(True)
        self.pdf_date_picker.setFont(QFont("Arial", 10))
        self.pdf_date_picker.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 150px;
            }
            QDateEdit:hover {
                border: 2px solid #2E86AB;
            }
        """)
        jour_layout.addWidget(self.pdf_date_picker)
        
        # Bouton générer journalier
        generate_jour_button = QPushButton("📄 Générer")
        generate_jour_button.setFont(QFont("Arial", 10, QFont.Bold))
        generate_jour_button.setCursor(Qt.PointingHandCursor)
        generate_jour_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #236B8E;
            }}
        """)
        generate_jour_button.clicked.connect(self.generer_rapport_pdf_date)
        jour_layout.addWidget(generate_jour_button)
        jour_layout.addStretch()
        pdf_content_layout.addLayout(jour_layout)
        
        # Séparateur
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setStyleSheet("background-color: #e5e7eb;")
        pdf_content_layout.addWidget(separator1)
        
        # Section 2: Rapport hebdomadaire
        semaine_layout = QHBoxLayout()
        
        semaine_label = QLabel("📊 Rapport Hebdomadaire:")
        semaine_label.setFont(QFont("Arial", 11, QFont.Bold))
        semaine_label.setStyleSheet("background-color: transparent; border: none;")
        semaine_layout.addWidget(semaine_label)
        
        semaine_info = QLabel("(Semaine en cours)")
        semaine_info.setFont(QFont("Arial", 9))
        semaine_info.setStyleSheet("color: #666; background-color: transparent; border: none;")
        semaine_layout.addWidget(semaine_info)
        
        generate_semaine_button = QPushButton("📄 Générer")
        generate_semaine_button.setFont(QFont("Arial", 10, QFont.Bold))
        generate_semaine_button.setCursor(Qt.PointingHandCursor)
        generate_semaine_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #28a745;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #218838;
            }}
        """)
        generate_semaine_button.clicked.connect(self.generer_rapport_hebdomadaire)
        semaine_layout.addWidget(generate_semaine_button)
        semaine_layout.addStretch()
        pdf_content_layout.addLayout(semaine_layout)
        
        # Séparateur
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setStyleSheet("background-color: #e5e7eb;")
        pdf_content_layout.addWidget(separator2)
        
        # Section 3: Rapport mensuel
        mois_layout = QHBoxLayout()
        
        mois_label = QLabel("📈 Rapport Mensuel:")
        mois_label.setFont(QFont("Arial", 11, QFont.Bold))
        mois_label.setStyleSheet("background-color: transparent; border: none;")
        mois_layout.addWidget(mois_label)
        
        # Sélecteur de mois
        self.pdf_mois_picker = QComboBox()
        self.pdf_mois_picker.addItems(["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                                       "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"])
        self.pdf_mois_picker.setCurrentIndex(datetime.now().month - 1)
        self.pdf_mois_picker.setFont(QFont("Arial", 10))
        self.pdf_mois_picker.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 120px;
            }
            QComboBox:hover {
                border: 2px solid #2E86AB;
            }
        """)
        mois_layout.addWidget(self.pdf_mois_picker)
        
        # Sélecteur d'année pour mois
        self.pdf_mois_annee_picker = QComboBox()
        current_year = datetime.now().year
        for year in range(current_year - 5, current_year + 1):
            self.pdf_mois_annee_picker.addItem(str(year))
        self.pdf_mois_annee_picker.setCurrentText(str(current_year))
        self.pdf_mois_annee_picker.setFont(QFont("Arial", 10))
        self.pdf_mois_annee_picker.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 80px;
            }
            QComboBox:hover {
                border: 2px solid #2E86AB;
            }
        """)
        mois_layout.addWidget(self.pdf_mois_annee_picker)
        
        generate_mois_button = QPushButton("📄 Générer")
        generate_mois_button.setFont(QFont("Arial", 10, QFont.Bold))
        generate_mois_button.setCursor(Qt.PointingHandCursor)
        generate_mois_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #ffc107;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #e0a800;
            }}
        """)
        generate_mois_button.clicked.connect(self.generer_rapport_mensuel)
        mois_layout.addWidget(generate_mois_button)
        mois_layout.addStretch()
        pdf_content_layout.addLayout(mois_layout)
        
        # Séparateur
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.HLine)
        separator3.setStyleSheet("background-color: #e5e7eb;")
        pdf_content_layout.addWidget(separator3)
        
        # Section 4: Rapport annuel
        annee_layout = QHBoxLayout()
        
        annee_label = QLabel("📊 Rapport Annuel:")
        annee_label.setFont(QFont("Arial", 11, QFont.Bold))
        annee_label.setStyleSheet("background-color: transparent; border: none;")
        annee_layout.addWidget(annee_label)
        
        # Sélecteur d'année
        self.pdf_annee_picker = QComboBox()
        for year in range(current_year - 5, current_year + 1):
            self.pdf_annee_picker.addItem(str(year))
        self.pdf_annee_picker.setCurrentText(str(current_year))
        self.pdf_annee_picker.setFont(QFont("Arial", 10))
        self.pdf_annee_picker.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 80px;
            }
            QComboBox:hover {
                border: 2px solid #2E86AB;
            }
        """)
        annee_layout.addWidget(self.pdf_annee_picker)
        
        generate_annee_button = QPushButton("📄 Générer")
        generate_annee_button.setFont(QFont("Arial", 10, QFont.Bold))
        generate_annee_button.setCursor(Qt.PointingHandCursor)
        generate_annee_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #dc3545;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #c82333;
            }}
        """)
        generate_annee_button.clicked.connect(self.generer_rapport_annuel)
        annee_layout.addWidget(generate_annee_button)
        annee_layout.addStretch()
        pdf_content_layout.addLayout(annee_layout)
        
        # Ajouter le container au layout principal
        pdf_layout.addWidget(self.pdf_content_container)
        
        pdf_frame.setLayout(pdf_layout)
        parent_layout.addWidget(pdf_frame)
    
    def toggle_pdf_section(self):
        """Basculer la visibilité de la section PDF"""
        self.pdf_section_visible = not self.pdf_section_visible
        self.pdf_content_container.setVisible(self.pdf_section_visible)
        
        if self.pdf_section_visible:
            self.toggle_pdf_btn.setText("▲ Masquer")
        else:
            self.toggle_pdf_btn.setText("▼ Afficher")
    
    def create_dashboard(self, parent_layout):
        """Ancienne méthode - redirigée vers create_rapports_tab pour compatibilité"""
        self.create_rapports_tab(parent_layout)
        # Frame pour les filtres
        filter_frame = QFrame()
        filter_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #ddd;
            }
        """)
        
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(20, 15, 20, 15)
        
        # Label
        filter_label = QLabel("Période:")
        filter_label.setFont(QFont("Arial", 11, QFont.Bold))
        filter_label.setStyleSheet("background-color: transparent; border: none;")
        filter_layout.addWidget(filter_label)
        
        # ComboBox pour le filtre
        self.period_filter = QComboBox()
        self.period_filter.addItems(["Aujourd'hui", "Cette semaine", "Ce mois", "Cette année", "Tout"])
        self.period_filter.setFont(QFont("Arial", 10))
        self.period_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 150px;
            }
            QComboBox:hover {
                border: 2px solid #2E86AB;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.period_filter.currentTextChanged.connect(self.actualiser_dashboard)
        filter_layout.addWidget(self.period_filter)
        
        filter_layout.addStretch()
        filter_frame.setLayout(filter_layout)
        parent_layout.addWidget(filter_frame)
        
        # Frame pour les statistiques du dashboard
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #ddd;
            }
        """)
        
        stats_layout = QVBoxLayout()
        stats_layout.setContentsMargins(20, 20, 20, 20)
        stats_layout.setSpacing(15)
        
        # Titre
        stats_title = QLabel("📊 Résumé de la période")
        stats_title.setFont(QFont("Arial", 14, QFont.Bold))
        stats_title.setStyleSheet(f"color: {COLOR_PRIMARY}; background-color: transparent; border: none;")
        stats_layout.addWidget(stats_title)
        
        # Stats en ligne
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(15)
        
        # Total Recettes
        recettes_card = QFrame()
        recettes_card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_SUCCESS};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        recettes_card_layout = QVBoxLayout()
        
        recettes_title = QLabel("💰 Recette(s)")
        recettes_title.setFont(QFont("Arial", 11, QFont.Bold))
        recettes_title.setStyleSheet("color: white; background-color: transparent;")
        recettes_title.setAlignment(Qt.AlignCenter)
        
        self.dashboard_recettes = QLabel("0.00 FC")
        self.dashboard_recettes.setFont(QFont("Arial", 18, QFont.Bold))
        self.dashboard_recettes.setStyleSheet("color: white; background-color: transparent;")
        self.dashboard_recettes.setAlignment(Qt.AlignCenter)
        
        recettes_card_layout.addWidget(recettes_title)
        recettes_card_layout.addWidget(self.dashboard_recettes)
        recettes_card.setLayout(recettes_card_layout)
        summary_layout.addWidget(recettes_card)
        
        # Total Dépenses
        depenses_card = QFrame()
        depenses_card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_DANGER};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        depenses_card_layout = QVBoxLayout()
        
        depenses_title = QLabel("💸 Dépenses")
        depenses_title.setFont(QFont("Arial", 11, QFont.Bold))
        depenses_title.setStyleSheet("color: white; background-color: transparent;")
        depenses_title.setAlignment(Qt.AlignCenter)
        
        self.dashboard_depenses = QLabel("0.00 FC")
        self.dashboard_depenses.setFont(QFont("Arial", 18, QFont.Bold))
        self.dashboard_depenses.setStyleSheet("color: white; background-color: transparent;")
        self.dashboard_depenses.setAlignment(Qt.AlignCenter)
        
        depenses_card_layout.addWidget(depenses_title)
        depenses_card_layout.addWidget(self.dashboard_depenses)
        depenses_card.setLayout(depenses_card_layout)
        summary_layout.addWidget(depenses_card)
        
        # Résultat
        resultat_card = QFrame()
        resultat_card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_PRIMARY};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        resultat_card_layout = QVBoxLayout()
        
        resultat_title = QLabel("📈 Solde")
        resultat_title.setFont(QFont("Arial", 11, QFont.Bold))
        resultat_title.setStyleSheet("color: white; background-color: transparent;")
        resultat_title.setAlignment(Qt.AlignCenter)
        
        self.dashboard_resultat = QLabel("0.00 FC")
        self.dashboard_resultat.setFont(QFont("Arial", 18, QFont.Bold))
        self.dashboard_resultat.setStyleSheet("color: white; background-color: transparent;")
        self.dashboard_resultat.setAlignment(Qt.AlignCenter)
        
        resultat_card_layout.addWidget(resultat_title)
        resultat_card_layout.addWidget(self.dashboard_resultat)
        resultat_card.setLayout(resultat_card_layout)
        summary_layout.addWidget(resultat_card)
        
        stats_layout.addLayout(summary_layout)
        stats_frame.setLayout(stats_layout)
        parent_layout.addWidget(stats_frame)
        
        # Table des statistiques par jour
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #ddd;
            }
        """)
        
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(20, 20, 20, 20)
        
        # Titre
        table_title = QLabel("📅 Détails par jour")
        table_title.setFont(QFont("Arial", 14, QFont.Bold))
        table_title.setStyleSheet(f"color: {COLOR_PRIMARY}; background-color: transparent; border: none;")
        table_layout.addWidget(table_title)
        
        # Table
        self.dashboard_table = QTableWidget()
        self.dashboard_table.setColumnCount(5)
        self.dashboard_table.setHorizontalHeaderLabels(["Date", "Recettes (FC)", "Dépenses (FC)", "Résultat (FC)", "Statut"])
        self.dashboard_table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #2E86AB;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        self.dashboard_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                gridline-color: #ddd;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #B3D9FF;
                color: black;
            }
        """)
        self.dashboard_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.dashboard_table.setAlternatingRowColors(True)
        self.dashboard_table.verticalHeader().setVisible(False)
        
        # Ajuster la largeur des colonnes
        header = self.dashboard_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        table_layout.addWidget(self.dashboard_table)
        table_frame.setLayout(table_layout)
        parent_layout.addWidget(table_frame)
        
    def actualiser_rapports(self):
        """Actualiser les données de l'onglet rapports"""
        # Déterminer la période
        periode = self.period_filter.currentText()
        date_debut = None
        date_fin = datetime.now().strftime("%Y-%m-%d")
        
        if periode == "Aujourd'hui":
            date_debut = datetime.now().strftime("%Y-%m-%d")
        elif periode == "Cette semaine":
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday())
            date_debut = start_of_week.strftime("%Y-%m-%d")
        elif periode == "Ce mois":
            date_debut = datetime.now().strftime("%Y-%m-01")
        elif periode == "Cette année":
            date_debut = datetime.now().strftime("%Y-01-01")
        else:  # Tout
            date_debut = None
            date_fin = None
        
        # Obtenir les statistiques détaillées
        stats = self.db.obtenir_statistiques_detaillees_par_jour(date_debut, date_fin)
        
        # Filtrer uniquement les jours clôturés
        stats_clotures = [(date, rec, dep_norm, dep_caisse, apport) 
                          for date, rec, dep_norm, dep_caisse, apport in stats 
                          if self.db.verifier_cloture(date)]
        
        # Calculer les totaux (uniquement transactions journalières normales)
        total_recettes = 0
        total_depenses_normales = 0
        total_depenses_caisse = 0
        
        for date, recettes, depenses_normales, depenses_caisse, apports in stats_clotures:
            total_recettes += recettes
            total_depenses_normales += depenses_normales
            total_depenses_caisse += depenses_caisse
        
        # Résultat calculé uniquement avec les dépenses normales (journalières)
        resultat = total_recettes - total_depenses_normales
        
        # Mettre à jour les cartes
        self.dashboard_recettes.setText(f"{total_recettes:,.0f} FC")
        self.dashboard_depenses.setText(f"{total_depenses_normales:,.0f} FC")
        #self.dashboard_depenses_caisse.setText(f"{total_depenses_caisse:,.0f} FC")
        self.dashboard_resultat.setText(f"{resultat:,.0f} FC")
        
        # Mettre à jour la table
        self.dashboard_table.setRowCount(0)
        
        for date, recettes, depenses_normales, depenses_caisse, apports in stats_clotures:
            # Résultat calculé uniquement avec les dépenses normales (journalières)
            resultat_jour = recettes - depenses_normales
            
            # Le rapport est forcément clôturé (filtré au préalable)
            est_cloture = True
            
            row_position = self.dashboard_table.rowCount()
            self.dashboard_table.insertRow(row_position)
            
            # Formater la date
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_formatted = date_obj.strftime("%d/%m/%Y")
            
            # Créer les items
            recettes_item = QTableWidgetItem(f"{recettes:,.0f}")
            # Afficher uniquement les dépenses normales (journalières)
            depenses_item = QTableWidgetItem(f"{depenses_normales:,.0f}")
            
            # Afficher le résultat seulement si clôturé
            if est_cloture:
                resultat_item = QTableWidgetItem(f"{resultat_jour:,.0f}")
                color = QColor(COLOR_SUCCESS) if resultat_jour >= 0 else QColor(COLOR_DANGER)
                resultat_item.setForeground(color)
                font = resultat_item.font()
                font.setBold(True)
                resultat_item.setFont(font)
            else:
                resultat_item = QTableWidgetItem("--")
            
            items = [
                QTableWidgetItem(date_formatted),
                recettes_item,
                depenses_item,
                resultat_item
            ]
            
            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignCenter if col != 0 else Qt.AlignLeft | Qt.AlignVCenter)
                self.dashboard_table.setItem(row_position, col, item)
    
    def on_period_filter_changed(self):
        """Gérer le changement du filtre de période"""
        # Réinitialiser le filtre de date pour éviter les conflits
        from PyQt5.QtCore import QDate
        self.date_filter.setDate(QDate.currentDate())
        self.actualiser_rapports()
    
    def on_month_filter_changed(self):
        """Gérer le changement du filtre de mois"""
        from datetime import datetime
        from calendar import monthrange
        
        # Récupérer le mois et l'année sélectionnés
        month_index = self.month_filter.currentIndex()  # 0-11
        year = int(self.year_filter.currentText())
        month = month_index + 1  # 1-12
        
        # Calculer le premier et dernier jour du mois
        first_day = datetime(year, month, 1)
        last_day_num = monthrange(year, month)[1]
        last_day = datetime(year, month, last_day_num)
        
        date_debut = first_day.strftime("%Y-%m-%d")
        date_fin = last_day.strftime("%Y-%m-%d")
        
        # Obtenir les statistiques pour ce mois
        stats = self.db.obtenir_statistiques_detaillees_par_jour(date_debut, date_fin)
        
        # Filtrer uniquement les jours clôturés
        stats_clotures = [(date, rec, dep_norm, dep_caisse, apport) 
                          for date, rec, dep_norm, dep_caisse, apport in stats 
                          if self.db.verifier_cloture(date)]
        
        # Calculer les totaux (uniquement transactions journalières normales)
        total_recettes = 0
        total_depenses_normales = 0
        total_depenses_caisse = 0
        
        for date, recettes, depenses_normales, depenses_caisse, apports in stats_clotures:
            total_recettes += recettes
            total_depenses_normales += depenses_normales
            total_depenses_caisse += depenses_caisse
        
        # Résultat calculé uniquement avec les dépenses normales (journalières)
        resultat = total_recettes - total_depenses_normales
        
        # Mettre à jour les cartes
        self.dashboard_recettes.setText(f"{total_recettes:,.0f} FC")
        self.dashboard_depenses.setText(f"{total_depenses_normales:,.0f} FC")
        self.dashboard_resultat.setText(f"{resultat:,.0f} FC")
        
        # Mettre à jour la table
        self.dashboard_table.setRowCount(0)
        
        for date, recettes, depenses_normales, depenses_caisse, apports in stats_clotures:
            # Résultat calculé uniquement avec les dépenses normales (journalières)
            resultat_jour = recettes - depenses_normales
            
            # Le rapport est forcément clôturé (filtré au préalable)
            est_cloture = True
            
            row_position = self.dashboard_table.rowCount()
            self.dashboard_table.insertRow(row_position)
            
            # Date
            date_item = QTableWidgetItem(date)
            self.dashboard_table.setItem(row_position, 0, date_item)
            
            # Recettes
            recettes_item = QTableWidgetItem(f"{recettes:,.0f} FC")
            recettes_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.dashboard_table.setItem(row_position, 1, recettes_item)
            
            # Dépenses (uniquement normales)
            depenses_item = QTableWidgetItem(f"{depenses_normales:,.0f} FC")
            depenses_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.dashboard_table.setItem(row_position, 2, depenses_item)
            
            # Résultat
            resultat_item = QTableWidgetItem(f"{resultat_jour:,.0f} FC")
            resultat_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if resultat_jour >= 0:
                resultat_item.setForeground(QColor(COLOR_SUCCESS))
            else:
                resultat_item.setForeground(QColor(COLOR_DANGER))
            self.dashboard_table.setItem(row_position, 3, resultat_item)
            
            # Statut
            statut_text = "Clôturé" if est_cloture else "Ouvert"
            statut_color = "#6c757d" if est_cloture else COLOR_PRIMARY
            statut_item = QTableWidgetItem(statut_text)
            statut_item.setForeground(QColor(statut_color))
            self.dashboard_table.setItem(row_position, 4, statut_item)
    
    def on_date_filter_changed(self):
        """Gérer le changement de la date dans le filtre"""
        # Ne rien faire automatiquement, attendre le clic sur le bouton
        pass
    
    def afficher_rapport_date(self):
        """Afficher le rapport pour la date sélectionnée"""
        # Récupérer la date sélectionnée
        date_selectionnee = self.date_filter.date().toString("yyyy-MM-dd")
        
        # Vérifier si la date est clôturée
        if not self.db.verifier_cloture(date_selectionnee):
            # Ne rien afficher si le rapport n'est pas clôturé
            self.dashboard_recettes.setText("0.00 FC")
            self.dashboard_depenses.setText("0.00 FC")
            self.dashboard_resultat.setText("0.00 FC")
            self.dashboard_table.setRowCount(0)
            return
        
        # Obtenir les statistiques pour cette date uniquement
        stats = self.db.obtenir_statistiques_detaillees_par_jour(date_selectionnee, date_selectionnee)
        
        # Calculer les totaux (uniquement transactions journalières normales)
        total_recettes = 0
        total_depenses_normales = 0
        total_depenses_caisse = 0
        
        for date, recettes, depenses_normales, depenses_caisse, apport in stats:
            total_recettes += recettes
            total_depenses_normales += depenses_normales
            total_depenses_caisse += depenses_caisse
        
        # Résultat calculé uniquement avec les dépenses normales (journalières)
        resultat = total_recettes - total_depenses_normales
        
        # Mettre à jour les cartes
        self.dashboard_recettes.setText(f"{total_recettes:,.0f} FC")
        self.dashboard_depenses.setText(f"{total_depenses_normales:,.0f} FC")
        #self.dashboard_depenses_caisse.setText(f"{total_depenses_caisse:,.0f} FC")
        self.dashboard_resultat.setText(f"{resultat:,.0f} FC")
        
        # Mettre à jour la table
        self.dashboard_table.setRowCount(0)
        
        for date, recettes, depenses_normales, depenses_caisse, apport in stats:
            # Résultat calculé uniquement avec les dépenses normales (journalières)
            resultat_jour = recettes - depenses_normales
            
            # Vérifier si le rapport est clôturé
            est_cloture = self.db.verifier_cloture(date)
            
            row_position = self.dashboard_table.rowCount()
            self.dashboard_table.insertRow(row_position)
            
            # Formater la date
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_formatted = date_obj.strftime("%d/%m/%Y")
            
            # Créer les items
            recettes_item = QTableWidgetItem(f"{recettes:,.0f}")
            # Afficher uniquement les dépenses normales (journalières)
            depenses_item = QTableWidgetItem(f"{depenses_normales:,.0f}")
            
            # Afficher le résultat seulement si clôturé
            if est_cloture:
                resultat_item = QTableWidgetItem(f"{resultat_jour:,.0f}")
                color = QColor(COLOR_SUCCESS) if resultat_jour >= 0 else QColor(COLOR_DANGER)
                resultat_item.setForeground(color)
                font = resultat_item.font()
                font.setBold(True)
                resultat_item.setFont(font)
            else:
                resultat_item = QTableWidgetItem("--")
            
            items = [
                QTableWidgetItem(date_formatted),
                recettes_item,
                depenses_item,
                resultat_item
            ]
            
            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignCenter if col != 0 else Qt.AlignLeft | Qt.AlignVCenter)
                self.dashboard_table.setItem(row_position, col, item)
        
        # Réinitialiser le filtre de période pour éviter les conflits
        self.period_filter.blockSignals(True)
        self.period_filter.setCurrentIndex(-1)  # Désélectionner
        self.period_filter.blockSignals(False)
    
    def generer_pdf_pour_date(self, date):
        """Générer un PDF pour une date spécifique"""
        try:
            # Vérifier si le rapport est clôturé
            est_cloture = self.db.verifier_cloture(date)
            
            if not est_cloture:
                QMessageBox.warning(
                    self, 
                    "Rapport non clôturé", 
                    "Le rapport doit être clôturé avant de pouvoir générer le PDF."
                )
                return
            
            # Vérifier s'il y a des transactions
            transactions = self.db.obtenir_transactions(date)
            
            if not transactions:
                QMessageBox.warning(self, "Attention", "Aucune transaction pour cette date.")
                return
            
            # Demander où sauvegarder le fichier
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_formatee = date_obj.strftime("%Y-%m-%d")
            nom_fichier_defaut = f"Rapport_Journalier_{date_formatee}.pdf"
            
            # Ouvrir le dialogue de sauvegarde
            nom_fichier, _ = QFileDialog.getSaveFileName(
                self,
                "Enregistrer le rapport PDF",
                os.path.join(os.path.expanduser("~"), "Documents", nom_fichier_defaut),
                "Fichiers PDF (*.pdf)"
            )
            
            if not nom_fichier:
                return  # L'utilisateur a annulé
            
            # Générer le PDF
            generateur = GenerateurRapportPDF(self.db)
            generateur.generer_rapport_journalier(date, nom_fichier)
            
            # Demander si l'utilisateur veut ouvrir le fichier
            reply = QMessageBox.question(
                self,
                "Succès",
                f"Le rapport PDF a été généré avec succès!\n\nFichier: {nom_fichier}\n\nVoulez-vous l'ouvrir maintenant?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                # Ouvrir le PDF avec l'application par défaut
                import subprocess
                import platform
                
                if platform.system() == 'Darwin':  # macOS
                    subprocess.call(('open', nom_fichier))
                elif platform.system() == 'Windows':  # Windows
                    os.startfile(nom_fichier)
                else:  # Linux
                    self.ouvrir_pdf(nom_fichier)
                    
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de la génération du PDF: {str(e)}")
    
    def ouvrir_pdf(self, nom_fichier):
        """Ouvrir un fichier PDF avec le lecteur approprié"""
        import subprocess
        import shutil
        
        # Liste des lecteurs PDF à essayer dans l'ordre
        lecteurs = ['evince', 'okular', 'atril', 'xreader', 'qpdfview', 'mupdf', 'firefox']
        
        # Trouver le premier lecteur disponible
        lecteur_trouve = None
        for lecteur in lecteurs:
            if shutil.which(lecteur):
                lecteur_trouve = lecteur
                break
        
        try:
            if lecteur_trouve:
                subprocess.Popen([lecteur_trouve, nom_fichier], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            else:
                # Fallback vers xdg-open si aucun lecteur spécifique n'est trouvé
                subprocess.Popen(['xdg-open', nom_fichier],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"Erreur lors de l'ouverture du PDF: {e}")
    
    def generer_rapport_pdf_date(self):
        """Générer un PDF pour la date sélectionnée dans le date picker"""
        date = self.pdf_date_picker.date().toString("yyyy-MM-dd")
        self.generer_pdf_pour_date(date)
    
    def generer_rapport_hebdomadaire(self):
        """Générer un rapport PDF pour la semaine en cours"""
        from calendar import monthrange
        
        # Calculer le début et la fin de la semaine
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        date_debut = start_of_week.strftime("%Y-%m-%d")
        date_fin = end_of_week.strftime("%Y-%m-%d")
        
        # Obtenir les statistiques pour la semaine
        stats = self.db.obtenir_statistiques_detaillees_par_jour(date_debut, date_fin)
        
        # Filtrer uniquement les jours clôturés
        stats_clotures = [(date, rec, dep_norm, dep_caisse, apport) 
                          for date, rec, dep_norm, dep_caisse, apport in stats 
                          if self.db.verifier_cloture(date)]
        
        if not stats_clotures:
            QMessageBox.warning(self, "Attention", "Aucun rapport clôturé pour cette semaine.")
            return
        
        # Générer le nom du fichier
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nom_fichier = f"Rapport_Hebdomadaire_{start_of_week.strftime('%d-%m-%Y')}_au_{end_of_week.strftime('%d-%m-%Y')}_{timestamp}.pdf"
        nom_fichier = os.path.join(os.path.expanduser("~"), "Documents", nom_fichier)
        
        try:
            from utils.pdf_generator import PDFGenerator
            pdf_gen = PDFGenerator(self.db)
            pdf_gen.generer_rapport_periode(date_debut, date_fin, nom_fichier, "Hebdomadaire")
            
            QMessageBox.information(
                self,
                "Succès",
                f"Rapport hebdomadaire généré avec succès!\n\nEmplacement: {nom_fichier}"
            )
            
            # Ouvrir le PDF
            self.ouvrir_pdf(nom_fichier)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération du PDF:\n{str(e)}")
    
    def generer_rapport_mensuel(self):
        """Générer un rapport PDF pour le mois sélectionné"""
        from calendar import monthrange
        
        # Récupérer le mois et l'année sélectionnés
        month_index = self.pdf_mois_picker.currentIndex()
        year = int(self.pdf_mois_annee_picker.currentText())
        month = month_index + 1
        
        # Calculer le premier et dernier jour du mois
        first_day = datetime(year, month, 1)
        last_day_num = monthrange(year, month)[1]
        last_day = datetime(year, month, last_day_num)
        
        date_debut = first_day.strftime("%Y-%m-%d")
        date_fin = last_day.strftime("%Y-%m-%d")
        
        # Obtenir les statistiques pour le mois
        stats = self.db.obtenir_statistiques_detaillees_par_jour(date_debut, date_fin)
        
        # Filtrer uniquement les jours clôturés
        stats_clotures = [(date, rec, dep_norm, dep_caisse, apport) 
                          for date, rec, dep_norm, dep_caisse, apport in stats 
                          if self.db.verifier_cloture(date)]
        
        if not stats_clotures:
            QMessageBox.warning(self, "Attention", "Aucun rapport clôturé pour ce mois.")
            return
        
        # Générer le nom du fichier
        mois_nom = self.pdf_mois_picker.currentText()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nom_fichier = f"Rapport_Mensuel_{mois_nom}_{year}_{timestamp}.pdf"
        nom_fichier = os.path.join(os.path.expanduser("~"), "Documents", nom_fichier)
        
        try:
            from utils.pdf_generator import PDFGenerator
            pdf_gen = PDFGenerator(self.db)
            pdf_gen.generer_rapport_mensuel(date_debut, date_fin, nom_fichier, mois_nom, year)
            
            QMessageBox.information(
                self,
                "Succès",
                f"Rapport mensuel généré avec succès!\n\nEmplacement: {nom_fichier}"
            )
            
            # Ouvrir le PDF
            self.ouvrir_pdf(nom_fichier)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération du PDF:\n{str(e)}")
    
    def generer_rapport_annuel(self):
        """Générer un rapport PDF pour l'année sélectionnée"""
        # Récupérer l'année sélectionnée
        year = int(self.pdf_annee_picker.currentText())
        
        date_debut = f"{year}-01-01"
        date_fin = f"{year}-12-31"
        
        # Obtenir les statistiques pour l'année
        stats = self.db.obtenir_statistiques_detaillees_par_jour(date_debut, date_fin)
        
        # Filtrer uniquement les jours clôturés
        stats_clotures = [(date, rec, dep_norm, dep_caisse, apport) 
                          for date, rec, dep_norm, dep_caisse, apport in stats 
                          if self.db.verifier_cloture(date)]
        
        if not stats_clotures:
            QMessageBox.warning(self, "Attention", "Aucun rapport clôturé pour cette année.")
            return
        
        # Générer le nom du fichier
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nom_fichier = f"Rapport_Annuel_{year}_{timestamp}.pdf"
        nom_fichier = os.path.join(os.path.expanduser("~"), "Documents", nom_fichier)
        
        try:
            from utils.pdf_generator import PDFGenerator
            pdf_gen = PDFGenerator(self.db)
            pdf_gen.generer_rapport_annuel(date_debut, date_fin, nom_fichier, year)
            
            QMessageBox.information(
                self,
                "Succès",
                f"Rapport annuel généré avec succès!\n\nEmplacement: {nom_fichier}"
            )
            
            # Ouvrir le PDF
            self.ouvrir_pdf(nom_fichier)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération du PDF:\n{str(e)}")
    
    def actualiser_dashboard(self):
        """Actualiser l'affichage de tous les onglets"""
        if hasattr(self, 'accueil_tab_widget'):
            self.accueil_tab_widget.actualiser()
        if hasattr(self, 'rapports_tab_widget'):
            self.rapports_tab_widget.actualiser()
        if hasattr(self, 'caisse_tab_widget'):
            self.caisse_tab_widget.actualiser()
        
        # Actualiser aussi l'en-tête de la caisse si visible
        if hasattr(self, 'caisse_header_widget') and self.caisse_header_widget.isVisible():
            self.actualiser_caisse_header()
    
    def actualiser_caisse_header(self):
        """Actualiser le montant en caisse dans l'en-tête"""
        if hasattr(self, 'caisse_header_montant'):
            caisse_info = self.db.calculer_caisse()
            self.caisse_header_montant.setText(f"{caisse_info['caisse']:,.0f} FC")
    
    # Ancienne méthode create_caisse_tab supprimée - remplacée par CaisseTab de views/caisse_tab.py
    
    def actualiser_caisse(self):
        """Actualiser les informations de la caisse"""
        # Utiliser la méthode actualiser de CaisseTab si elle existe
        if hasattr(self, 'caisse_tab_widget'):
            self.caisse_tab_widget.actualiser()
        
        # Actualiser l'en-tête de la caisse
        self.actualiser_caisse_header()
        
        # Calculer la caisse pour l'en-tête principal
        caisse_info = self.db.calculer_caisse()
        
        # Mettre à jour le montant en caisse dans l'en-tête principal
        if hasattr(self, 'rapport_montant_caisse'):
            self.rapport_montant_caisse.setText(f"{caisse_info['caisse']:,.0f} FC")
    def on_caisse_period_filter_changed(self):
        """Gérer le changement du filtre de période pour la caisse"""
        # Réinitialiser le filtre de date pour éviter les conflits
        self.caisse_date_filter.setDate(QDate.currentDate())
        self.actualiser_caisse()
    
    def afficher_caisse_date(self):
        """Afficher les transactions de caisse pour une date spécifique"""
        # Récupérer la date sélectionnée
        date_selectionnee = self.caisse_date_filter.date().toString("yyyy-MM-dd")
        
        # Calculer la caisse pour cette date spécifique
        caisse_info = self.db.calculer_caisse(date_selectionnee, date_selectionnee)
        
        self.caisse_montant.setText(f"{caisse_info['caisse']:,.0f} FC")
        self.caisse_solde_cloture.setText(f"{caisse_info['solde_cloture']:,.0f} FC")
        self.caisse_depenses_speciales.setText(f"{caisse_info['depenses_speciales']:,.0f} FC")
        self.caisse_apports.setText(f"{caisse_info['apports']:,.0f} FC")
        
        # Actualiser le tableau des dépenses spéciales pour cette date
        self.depenses_speciales_table.setRowCount(0)
        
        depenses = self.db.obtenir_depenses_speciales(date_selectionnee, date_selectionnee)
        for depense in depenses:
            id_dep, montant, description, date, created_at = depense
            
            row_position = self.depenses_speciales_table.rowCount()
            self.depenses_speciales_table.insertRow(row_position)
            
            items = [
                QTableWidgetItem(str(id_dep)),
                QTableWidgetItem(f"{montant:,.0f}"),
                QTableWidgetItem(description),
                QTableWidgetItem(date)
            ]
            
            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignCenter if col != 2 else Qt.AlignLeft | Qt.AlignVCenter)
                if col == 1:
                    item.setForeground(QColor(COLOR_DANGER))
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                self.depenses_speciales_table.setItem(row_position, col, item)
        
        # Actualiser le tableau des apports pour cette date
        self.apports_table.setRowCount(0)
        
        apports = self.db.obtenir_apports(date_selectionnee, date_selectionnee)
        for apport in apports:
            id_app, montant, description, date, created_at = apport
            
            row_position = self.apports_table.rowCount()
            self.apports_table.insertRow(row_position)
            
            items = [
                QTableWidgetItem(str(id_app)),
                QTableWidgetItem(f"{montant:,.0f}"),
                QTableWidgetItem(description),
                QTableWidgetItem(date)
            ]
            
            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignCenter if col != 2 else Qt.AlignLeft | Qt.AlignVCenter)
                if col == 1:
                    item.setForeground(QColor(COLOR_SUCCESS))
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                self.apports_table.setItem(row_position, col, item)
        
        # Réinitialiser le filtre de période pour éviter les conflits
        self.caisse_period_filter.blockSignals(True)
        self.caisse_period_filter.setCurrentIndex(0)  # Tout
        self.caisse_period_filter.blockSignals(False)
                
                
    def ajouter_depense_speciale(self):
        """Ajouter une dépense spéciale (caisse)"""
        try:
            # Vérifier d'abord si la caisse n'est pas vide
            caisse_info = self.db.calculer_caisse()
            if caisse_info['caisse'] <= 0:
                QMessageBox.warning(
                    self,
                    "Caisse vide",
                    "La caisse est vide. Impossible d'effectuer une dépense.\n\nVeuillez d'abord clôturer des rapports journaliers pour alimenter la caisse."
                )
                return
            
            montant_text = self.depense_speciale_montant.text().strip()
            
            if not montant_text:
                QMessageBox.warning(self, "Attention", "Veuillez entrer un montant")
                return
            
            montant = float(montant_text)
            description = self.depense_speciale_description.text().strip()
            
            if montant <= 0:
                QMessageBox.critical(self, "Erreur", "Le montant doit être supérieur à 0")
                return
            
            if not description:
                QMessageBox.warning(self, "Attention", "Veuillez entrer une description")
                return
            
            # Vérifier qu'il y a assez dans la caisse
            if montant > caisse_info['caisse']:
                reply = QMessageBox.question(
                    self,
                    "Attention",
                    f"Le montant ({montant:,.0f} FC) dépasse la caisse disponible ({caisse_info['caisse']:,.0f} FC).\n\nVoulez-vous continuer quand même?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return
            
            # Ajouter la dépense spéciale
            self.db.ajouter_transaction("depense", montant, description, "speciale")
            
            # Réinitialiser les champs
            self.depense_speciale_montant.clear()
            self.depense_speciale_description.clear()
            
            # Actualiser l'affichage
            self.actualiser_caisse()
            
            QMessageBox.information(self, "Succès", "Dépense spéciale ajoutée avec succès!")
            
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer un montant valide")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {str(e)}")
    
    def ajouter_apport_caisse(self):
        """Ajouter un apport manuel dans la caisse"""
        try:
            montant_text = self.apport_caisse_montant.text().strip()
            
            if not montant_text:
                QMessageBox.warning(self, "Attention", "Veuillez entrer un montant")
                return
            
            montant = float(montant_text)
            description = self.apport_caisse_description.text().strip()
            
            # La description est obligatoire pour les apports
            if not description:
                QMessageBox.warning(self, "Attention", "Veuillez entrer une description pour l'apport en capital")
                return
            
            if montant <= 0:
                QMessageBox.critical(self, "Erreur", "Le montant doit être supérieur à 0")
                return
            
            # Ajouter l'apport comme une transaction spéciale de type "apport"
            self.db.ajouter_transaction("apport", montant, description, "speciale")
            
            # Réinitialiser les champs
            self.apport_caisse_montant.clear()
            self.apport_caisse_description.clear()
            
            # Actualiser l'affichage
            self.actualiser_caisse()
            self.actualiser_rapports()
            
            QMessageBox.information(self, "Succès", f"Apport de {montant:,.0f} FC ajouté dans la caisse!")
            
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer un montant valide")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {str(e)}")
            
    def generer_rapport_pdf(self):
        """Générer un rapport PDF pour la journée"""
        try:
            date_jour = datetime.now().strftime("%Y-%m-%d")
            
            # Vérifier si le rapport est clôturé
            est_cloture = self.db.verifier_cloture(date_jour)
            
            if not est_cloture:
                QMessageBox.warning(
                    self, 
                    "Rapport non clôturé", 
                    "Le rapport doit être clôturé avant de pouvoir générer le PDF.\n\nVeuillez d'abord clôturer le rapport de la journée."
                )
                return
            
            # Vérifier s'il y a des transactions
            transactions = self.db.obtenir_transactions(date_jour)
            
            if not transactions:
                QMessageBox.warning(self, "Attention", "Aucune transaction pour aujourd'hui. Impossible de générer le rapport.")
                return
            
            # Demander où sauvegarder le fichier
            date_formatee = datetime.now().strftime("%Y-%m-%d")
            nom_fichier_defaut = f"Rapport_Journalier_{date_formatee}.pdf"
            
            # Ouvrir le dialogue de sauvegarde
            nom_fichier, _ = QFileDialog.getSaveFileName(
                self,
                "Enregistrer le rapport PDF",
                os.path.join(os.path.expanduser("~"), "Documents", nom_fichier_defaut),
                "Fichiers PDF (*.pdf)"
            )
            
            if not nom_fichier:
                return  # L'utilisateur a annulé
            
            # Générer le PDF
            generateur = GenerateurRapportPDF(self.db)
            generateur.generer_rapport_journalier(date_jour, nom_fichier)
            
            # Demander si l'utilisateur veut ouvrir le fichier
            reply = QMessageBox.question(
                self,
                "Succès",
                f"Le rapport PDF a été généré avec succès!\n\nFichier: {nom_fichier}\n\nVoulez-vous l'ouvrir maintenant?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                # Ouvrir le PDF avec l'application par défaut
                import subprocess
                import platform
                
                if platform.system() == 'Darwin':  # macOS
                    subprocess.call(('open', nom_fichier))
                elif platform.system() == 'Windows':  # Windows
                    os.startfile(nom_fichier)
                else:  # Linux
                    self.ouvrir_pdf(nom_fichier)
                    
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de la génération du PDF: {str(e)}")


class ModifierTransactionDialog(QDialog):
    """Fenêtre de dialogue pour modifier une transaction"""
    
    def __init__(self, parent, transaction):
        super().__init__(parent)
        self.transaction = transaction
        self.setup_ui()
        
    def setup_ui(self):
        """Configurer l'interface de la fenêtre"""
        self.setWindowTitle("Modifier la transaction")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titre
        title = QLabel("✏️ Modifier la transaction")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet(f"color: {COLOR_PRIMARY};")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # ID (non modifiable, juste pour info)
        id_layout = QHBoxLayout()
        id_label = QLabel("ID:")
        id_label.setFont(QFont("Arial", 11))
        id_layout.addWidget(id_label)
        
        id_value = QLabel(str(self.transaction[0]))
        id_value.setFont(QFont("Arial", 11, QFont.Bold))
        id_layout.addWidget(id_value)
        id_layout.addStretch()
        layout.addLayout(id_layout)
        
        # Type de transaction
        type_layout = QHBoxLayout()
        type_label = QLabel("Type:")
        type_label.setFont(QFont("Arial", 11))
        type_layout.addWidget(type_label)
        
        self.type_group = QButtonGroup()
        self.recette_radio = QRadioButton("Recette")
        self.depense_radio = QRadioButton("Dépense")
        self.recette_radio.setFont(QFont("Arial", 10))
        self.depense_radio.setFont(QFont("Arial", 10))
        self.recette_radio.setStyleSheet(f"color: {COLOR_SUCCESS};")
        self.depense_radio.setStyleSheet(f"color: {COLOR_DANGER};")
        
        self.type_group.addButton(self.recette_radio, 1)
        self.type_group.addButton(self.depense_radio, 2)
        
        # Définir le type actuel
        if self.transaction[1] == "recette":
            self.recette_radio.setChecked(True)
        else:
            self.depense_radio.setChecked(True)
        
        type_layout.addWidget(self.recette_radio)
        type_layout.addWidget(self.depense_radio)
        type_layout.addStretch()
        layout.addLayout(type_layout)
        
        # Type de dépense (pour les dépenses)
        self.type_depense_layout = QHBoxLayout()
        type_depense_label = QLabel("Type de dépense:")
        type_depense_label.setFont(QFont("Arial", 11))
        self.type_depense_layout.addWidget(type_depense_label)
        
        self.type_depense_group = QButtonGroup()
        self.depense_normale_radio = QRadioButton("Normale (journalière)")
        self.depense_speciale_radio = QRadioButton("Spéciale (caisse)")
        self.depense_normale_radio.setFont(QFont("Arial", 10))
        self.depense_speciale_radio.setFont(QFont("Arial", 10))
        
        self.type_depense_group.addButton(self.depense_normale_radio, 1)
        self.type_depense_group.addButton(self.depense_speciale_radio, 2)
        
        # Définir le type de dépense actuel
        type_depense = self.transaction[6] if len(self.transaction) > 6 else "normale"
        if type_depense == "speciale":
            self.depense_speciale_radio.setChecked(True)
        else:
            self.depense_normale_radio.setChecked(True)
        
        self.type_depense_layout.addWidget(self.depense_normale_radio)
        self.type_depense_layout.addWidget(self.depense_speciale_radio)
        self.type_depense_layout.addStretch()
        
        self.type_depense_widget = QWidget()
        self.type_depense_widget.setLayout(self.type_depense_layout)
        self.type_depense_widget.setVisible(self.transaction[1] == "depense")
        layout.addWidget(self.type_depense_widget)
        
        # Connecter le changement de type
        self.recette_radio.toggled.connect(self.toggle_type_depense)
        self.depense_radio.toggled.connect(self.toggle_type_depense)
        
        # Montant
        montant_layout = QHBoxLayout()
        montant_label = QLabel("Montant:")
        montant_label.setFont(QFont("Arial", 11))
        montant_label.setFixedWidth(120)
        montant_layout.addWidget(montant_label)
        
        self.montant_entry = QLineEdit()
        self.montant_entry.setFont(QFont("Arial", 11))
        self.montant_entry.setText(str(self.transaction[2]))
        self.montant_entry.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #2E86AB;
            }
        """)
        montant_layout.addWidget(self.montant_entry)
        layout.addLayout(montant_layout)
        
        # Description
        desc_layout = QHBoxLayout()
        desc_label = QLabel("Description:")
        desc_label.setFont(QFont("Arial", 11))
        desc_label.setFixedWidth(120)
        desc_layout.addWidget(desc_label)
        
        self.description_entry = QLineEdit()
        self.description_entry.setFont(QFont("Arial", 11))
        self.description_entry.setText(self.transaction[3])
        self.description_entry.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #2E86AB;
            }
        """)
        desc_layout.addWidget(self.description_entry)
        layout.addLayout(desc_layout)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_button = QPushButton("Annuler")
        cancel_button.setFont(QFont("Arial", 11))
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #999;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)
        
        save_button = QPushButton("Enregistrer")
        save_button.setFont(QFont("Arial", 11, QFont.Bold))
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #236B8E;
            }}
        """)
        save_button.clicked.connect(self.validate_and_accept)
        buttons_layout.addWidget(save_button)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        
    def toggle_type_depense(self):
        """Afficher/masquer le choix du type de dépense"""
        self.type_depense_widget.setVisible(self.depense_radio.isChecked())
        
    def validate_and_accept(self):
        """Valider les données avant d'accepter"""
        try:
            montant = float(self.montant_entry.text().strip())
            if montant <= 0:
                QMessageBox.critical(self, "Erreur", "Le montant doit être supérieur à 0")
                return
            self.accept()
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer un montant valide")
    
    def get_values(self):
        """Obtenir les valeurs modifiées"""
        type_transaction = "recette" if self.recette_radio.isChecked() else "depense"
        montant = float(self.montant_entry.text().strip())
        description = self.description_entry.text().strip()
        
        type_depense = "normale"
        if type_transaction == "depense":
            type_depense = "speciale" if self.depense_speciale_radio.isChecked() else "normale"
        
        return type_transaction, montant, description, type_depense
