"""
Onglet Accueil - Tableau de bord et transactions
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QRadioButton, QTableWidget, 
                             QTableWidgetItem, QFrame, QButtonGroup, QMessageBox, 
                             QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPixmap
from datetime import datetime
import os


class AccueilTab(QWidget):
    """Onglet principal avec dashboard et transactions"""
    
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent_window = parent
        self.date_courante = datetime.now().strftime("%Y-%m-%d")  # Stocker la date affichée
        self.init_ui()
    
    def init_ui(self):
        """Initialiser l'interface"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 20, 0, 0)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)
        
        # Label de la date
        from config import COLOR_PRIMARY
        self.date_label = QLabel()
        self.date_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.date_label.setStyleSheet(f"color: {COLOR_PRIMARY}; background-color: transparent;")
        self.date_label.setAlignment(Qt.AlignCenter)
        self.mettre_a_jour_date_label()
        main_layout.addWidget(self.date_label)
        
        # Frame pour les statistiques
        self.create_stats_frame(main_layout)
        
        # Frame pour l'ajout de transactions
        self.create_transaction_frame(main_layout)
        
        # Frame pour l'historique
        self.create_history_frame(main_layout)
    
    def create_stats_frame(self, parent_layout):
        """Créer le cadre des statistiques (dashboard cards)"""
        from config import COLOR_SUCCESS, COLOR_DANGER, COLOR_PRIMARY
        
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)
        
        # Recettes du jour
        recettes_frame = QFrame()
        recettes_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_SUCCESS};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        recettes_layout = QVBoxLayout()
        
        recettes_title = QLabel("📈 Recettes")
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
        
        # Solde disponible
        self.solde_frame = QFrame()
        self.solde_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_PRIMARY};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        solde_layout = QVBoxLayout()
        
        solde_title = QLabel("💰 Solde")
        solde_title.setFont(QFont("Arial", 12, QFont.Bold))
        solde_title.setStyleSheet("color: white; background-color: transparent;")
        solde_title.setAlignment(Qt.AlignCenter)
        
        self.solde_label = QLabel("0.00 FC")
        self.solde_label.setFont(QFont("Arial", 36, QFont.Bold))
        self.solde_label.setStyleSheet("color: white; background-color: transparent;")
        self.solde_label.setAlignment(Qt.AlignCenter)
        
        solde_layout.addWidget(solde_title)
        solde_layout.addWidget(self.solde_label)
        self.solde_frame.setLayout(solde_layout)
        stats_layout.addWidget(self.solde_frame)
        
        # Dépenses du jour
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
        from config import COLOR_SECONDARY
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
        
        # Bouton Envoyer (visible uniquement si rapport clôturé)
        self.envoyer_button = QPushButton("📤 Envoyer")
        self.envoyer_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.envoyer_button.setCursor(Qt.PointingHandCursor)
        self.envoyer_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                padding: 12px 30px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #1E6A8F;
            }}
        """)
        self.envoyer_button.clicked.connect(self.envoyer_rapport)
        self.envoyer_button.hide()  # Caché par défaut
        cloture_layout.addWidget(self.envoyer_button)
        
        cloture_layout.addStretch()
        parent_layout.addLayout(cloture_layout)
    
    def create_transaction_frame(self, parent_layout):
        """Créer le formulaire d'ajout de transaction"""
        # Le formulaire sera affiché dans un dialogue
        pass
    
    def toggle_transaction_form(self):
        """Afficher le dialogue de transaction"""
        from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QButtonGroup, QRadioButton, QLineEdit
        from config import COLOR_PRIMARY, COLOR_SUCCESS, COLOR_DANGER
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Nouvelle Transaction")
        dialog.setModal(True)
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Type de transaction
        type_layout = QHBoxLayout()
        type_label = QLabel("Type:")
        type_label.setFont(QFont("Arial", 11))
        type_layout.addWidget(type_label)
        
        type_group = QButtonGroup()
        self.recette_radio = QRadioButton("Recette")
        self.depense_radio = QRadioButton("Dépense")
        self.recette_radio.setChecked(True)
        self.recette_radio.setFont(QFont("Arial", 10))
        self.depense_radio.setFont(QFont("Arial", 10))
        self.recette_radio.setStyleSheet(f"color: {COLOR_SUCCESS};")
        self.depense_radio.setStyleSheet(f"color: {COLOR_DANGER};")
        
        type_group.addButton(self.recette_radio, 1)
        type_group.addButton(self.depense_radio, 2)
        
        type_layout.addWidget(self.recette_radio)
        type_layout.addWidget(self.depense_radio)
        type_layout.addStretch()
        layout.addLayout(type_layout)
        
        # Montant
        montant_layout = QHBoxLayout()
        montant_label = QLabel("Montant:")
        montant_label.setFont(QFont("Arial", 11))
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
        desc_label.setFixedWidth(100)
        desc_layout.addWidget(desc_label)
        
        self.description_entry = QLineEdit()
        self.description_entry.setFont(QFont("Arial", 11))
        self.description_entry.setPlaceholderText("Description")
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
        
        # Boutons du dialogue
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.button(QDialogButtonBox.Ok).setText("Ajouter")
        button_box.button(QDialogButtonBox.Cancel).setText("Annuler")
        button_box.accepted.connect(lambda: self.valider_transaction(dialog))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def valider_transaction(self, dialog):
        """Valider et ajouter la transaction"""
        if self.parent_window:
            # Appeler la méthode du parent pour ajouter la transaction
            if self.parent_window.ajouter_transaction():
                dialog.accept()
    
    def ajouter_transaction(self):
        """Méthode appelée par le dialogue pour ajouter une transaction"""
        if self.parent_window:
            return self.parent_window.ajouter_transaction()
    
    def create_history_frame(self, parent_layout):
        """Créer le tableau d'historique des transactions"""
        from PyQt5.QtWidgets import QTableWidget, QHeaderView
        from config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_DANGER
        
        # Conteneur pour le tableau avec titre et boutons
        history_container = QFrame()
        history_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 0px;
            }
        """)
        history_layout = QVBoxLayout()
        history_layout.setSpacing(15)
        history_container.setLayout(history_layout)
        
        # En-tête avec titre et boutons
        header_layout = QHBoxLayout()
        
        # Titre
        title_label = QLabel("Historique des opérations")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet(f"color: {COLOR_PRIMARY}; background-color: transparent;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Bouton Rapports
        btn_rapports = QPushButton("📋 Rapports")
        btn_rapports.setFixedSize(120, 35)
        btn_rapports.setCursor(Qt.PointingHandCursor)
        btn_rapports.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                border-radius: 5px;
                border: none;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
        """)
        btn_rapports.clicked.connect(self.afficher_liste_rapports)
        header_layout.addWidget(btn_rapports)
        
        # Bouton Actualiser
        btn_actualiser = QPushButton("🔄 Actualiser")
        btn_actualiser.setFixedSize(120, 35)
        btn_actualiser.setCursor(Qt.PointingHandCursor)
        btn_actualiser.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_SECONDARY};
                color: white;
                border-radius: 5px;
                border: none;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
        """)
        btn_actualiser.clicked.connect(self.actualiser_affichage)
        header_layout.addWidget(btn_actualiser)
        
        # Bouton Modifier
        btn_modifier = QPushButton("✏️ Modifier")
        btn_modifier.setFixedSize(120, 35)
        btn_modifier.setCursor(Qt.PointingHandCursor)
        btn_modifier.setStyleSheet(f"""
            QPushButton {{
                background-color: #FF9800;
                color: white;
                border-radius: 5px;
                border: none;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #F57C00;
            }}
        """)
        btn_modifier.clicked.connect(self.modifier_transaction)
        header_layout.addWidget(btn_modifier)
        
        # Bouton Supprimer
        btn_supprimer = QPushButton("🗑️ Supprimer")
        btn_supprimer.setFixedSize(120, 35)
        btn_supprimer.setCursor(Qt.PointingHandCursor)
        btn_supprimer.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_DANGER};
                color: white;
                border-radius: 5px;
                border: none;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #C0392B;
            }}
        """)
        btn_supprimer.clicked.connect(self.supprimer_transaction)
        header_layout.addWidget(btn_supprimer)
        
        history_layout.addLayout(header_layout)
        
        # Créer le tableau
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["N°", "Type", "Montant (FC)", "Description", "Date", "Heure"])
        
        # Configuration de base
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setShowGrid(True)
        self.table.setAlternatingRowColors(True)
        
        # Configuration de l'en-tête
        header = self.table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setStretchLastSection(False)
        header.setMinimumHeight(45)
        header.setMaximumHeight(45)

        header_font = QFont("Arial", 12, QFont.Bold)
        header.setFont(header_font)

        # Largeurs des colonnes
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.resizeSection(0, 60)

        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.resizeSection(1, 100)

        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.resizeSection(2, 130)

        header.setSectionResizeMode(3, QHeaderView.Stretch)

        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.resizeSection(4, 110)

        header.setSectionResizeMode(5, QHeaderView.Fixed)
        header.resizeSection(5, 80)

        # Style du tableau
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                gridline-color: #E0E0E0;
                alternate-background-color: #F9F9F9;
            }
            QTableWidget::item {
                padding: 10px 8px;
                color: #333;
                border: none;
                border-bottom: 1px solid #E8E8E8;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #000;
            }
            QHeaderView::section {
                background-color: #2E86AB;
                color: #FFFFFF;
                padding: 14px 8px;
                border: none;
                border-right: 1px solid rgba(255, 255, 255, 0.1);
                font-weight: bold;
                font-size: 11px;
                text-transform: uppercase;
            }
            QHeaderView::section:last {
                border-right: none;
            }
        """)        
        history_layout.addWidget(self.table, 1)  # Le 1 indique que le tableau doit s'étirer
        parent_layout.addWidget(history_container, 1)  # Le conteneur aussi doit s'étirer
    
    def toggle_cloture_rapport(self):
        """Clôturer ou réouvrir le rapport du jour"""
        if self.parent_window:
            self.parent_window.toggle_cloture_rapport()
    
    def actualiser_affichage(self):
        """Actualiser l'affichage avec gestion de la clôture"""
        from config import COLOR_SUCCESS, COLOR_DANGER, COLOR_SECONDARY
        
        # Utiliser la date courante au lieu de la date du jour
        est_cloture = self.controller.verifier_cloture(self.date_courante)
        
        # Adapter le texte du bouton selon la date
        est_aujourdhui = self.date_courante == datetime.now().strftime("%Y-%m-%d")
        
        if est_cloture:
            texte_bouton = "🔓 Rouvrir le rapport" if not est_aujourdhui else "🔓 Rouvrir le rapport du jour"
            self.cloture_button.setText(texte_bouton)
            self.cloture_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLOR_SUCCESS};
                    color: white;
                    padding: 12px;
                    border-radius: 5px;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: #058965;
                }}
            """)
            self.cloture_status.setText("✅ Rapport clôturé")
            self.cloture_status.setStyleSheet(f"color: {COLOR_SUCCESS}; background-color: transparent;")
            self.envoyer_button.show()  # Afficher le bouton Envoyer
        else:
            texte_bouton = "🔒 Clôturer le rapport" if not est_aujourdhui else "🔒 Clôturer le rapport du jour"
            self.cloture_button.setText(texte_bouton)
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
            """)
            self.cloture_status.setText("⚠️ Rapport non clôturé")
            self.cloture_status.setStyleSheet(f"color: {COLOR_DANGER}; background-color: transparent;")
            self.envoyer_button.hide()  # Cacher le bouton Envoyer
        
        # Actualiser les statistiques pour la date courante
        stats = self.controller.calculer_solde(self.date_courante)
        
        # Masquer le solde si le rapport n'est pas clôturé
        if not est_cloture:
            self.solde_label.setText("-- FC")
            self.solde_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: #999999;
                    border-radius: 10px;
                    padding: 10px;
                }}
            """)
        else:
            self.solde_label.setText(f"{stats['solde']:,.0f} FC")
            # Changer la couleur du solde selon le montant
            if stats['solde'] < 0:
                self.solde_frame.setStyleSheet(f"""
                    QFrame {{
                        background-color: {COLOR_DANGER};
                        border-radius: 10px;
                        padding: 10px;
                    }}
                """)
            else:
                from config import COLOR_PRIMARY
                self.solde_frame.setStyleSheet(f"""
                    QFrame {{
                        background-color: {COLOR_PRIMARY};
                        border-radius: 10px;
                        padding: 10px;
                    }}
                """)
        
        self.recettes_label.setText(f"{stats['recettes']:,.0f} FC")
        self.depenses_label.setText(f"{stats['depenses']:,.0f} FC")
        
        # Actualiser l'historique - afficher les transactions de la date courante
        self.table.setRowCount(0)
        
        transactions = self.controller.obtenir_transactions(self.date_courante)
        for index, transaction in enumerate(transactions, start=1):
            id_trans, type_trans, montant, description, date, created_at = transaction
            
            # Extraire l'heure de created_at
            heure = created_at.split()[1] if len(created_at.split()) > 1 else ""
            
            # Formater le montant
            montant_formatted = f"{montant:,.0f}"
            
            # Ajouter une ligne dans le tableau
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            # Créer les items
            items = [
                QTableWidgetItem(str(index)),  # Numéro séquentiel 1, 2, 3...
                QTableWidgetItem(type_trans.capitalize()),
                QTableWidgetItem(montant_formatted),
                QTableWidgetItem(description),
                QTableWidgetItem(date),
                QTableWidgetItem(heure)
            ]
            
            # Stocker l'ID réel dans les données de la première colonne pour modification/suppression
            items[0].setData(Qt.UserRole, id_trans)
            
            # Définir la couleur selon le type
            from PyQt5.QtGui import QBrush
            if type_trans == "recette":
                color = QColor("#06A77D")  # Vert
            else:
                color = QColor("#D62246")  # Rouge
            
            for col, item in enumerate(items):
                # Centrer toutes les colonnes (horizontalement et verticalement)
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                    
                if col == 1:  # Colorer la colonne Type en vert ou rouge
                    item.setForeground(QBrush(color))
                if col == 2:  # Colorer la colonne Montant en vert ou rouge
                    item.setForeground(QBrush(color))
                self.table.setItem(row_position, col, item)
    
    def actualiser(self):
        """Actualiser l'affichage des données"""
        # Mettre à jour les statistiques pour la date courante
        stats = self.controller.calculer_solde(self.date_courante)
        self.solde_label.setText(f"{stats['solde']:,.0f} FC")
        self.recettes_label.setText(f"{stats['recettes']:,.0f} FC")
        self.depenses_label.setText(f"{stats['depenses']:,.0f} FC")
        
        # Changer la couleur du solde selon positif/négatif
        from config import COLOR_PRIMARY, COLOR_DANGER
        if stats['solde'] >= 0:
            self.solde_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLOR_PRIMARY};
                    border-radius: 10px;
                    padding: 10px;
                }}
            """)
        else:
            self.solde_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLOR_DANGER};
                    border-radius: 10px;
                    padding: 10px;
                }}
            """)
    
    def afficher_liste_rapports(self):
        """Afficher la liste de tous les rapports pour sélection"""
        from PyQt5.QtWidgets import QDialog, QListWidget, QListWidgetItem, QDialogButtonBox
        from datetime import datetime
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Sélectionner un rapport")
        dialog.setModal(True)
        dialog.setMinimumSize(400, 500)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Titre
        from config import COLOR_PRIMARY
        title = QLabel("📋 Liste des rapports journaliers")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet(f"color: {COLOR_PRIMARY};")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Liste des rapports
        liste = QListWidget()
        liste.setFont(QFont("Arial", 11))
        liste.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #E3F2FD;
                color: black;
            }
            QListWidget::item:hover {
                background-color: #F5F5F5;
            }
        """)
        
        # Obtenir tous les rapports
        rapports = self.controller.obtenir_tous_rapports()
        
        if not rapports:
            item = QListWidgetItem("Aucun rapport disponible")
            item.setFlags(Qt.NoItemFlags)
            liste.addItem(item)
        else:
            for date_rapport, recettes, depenses, est_cloture in rapports:
                solde = recettes - depenses
                statut = "🔒 Clôturé" if est_cloture else "🔓 Ouvert"
                date_format = datetime.strptime(date_rapport, "%Y-%m-%d").strftime("%d/%m/%Y")
                
                texte = f"{date_format}  |  {statut}  |  Recettes: {recettes:,.0f} FC  |  Dépenses: {depenses:,.0f} FC  |  Solde: {solde:,.0f} FC"
                
                item = QListWidgetItem(texte)
                item.setData(Qt.UserRole, date_rapport)
                liste.addItem(item)
        
        liste.itemDoubleClicked.connect(lambda item: self.charger_rapport(item.data(Qt.UserRole), dialog))
        layout.addWidget(liste)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        # Bouton pour retourner au rapport du jour
        retour_btn = QPushButton("🏠 Retour au rapport du jour")
        retour_btn.setFont(QFont("Arial", 10, QFont.Bold))
        retour_btn.setCursor(Qt.PointingHandCursor)
        retour_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #2573A7;
            }}
        """)
        retour_btn.clicked.connect(lambda: self.charger_rapport(datetime.now().strftime("%Y-%m-%d"), dialog))
        buttons_layout.addWidget(retour_btn)
        
        buttons_layout.addStretch()
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.charger_rapport(liste.currentItem().data(Qt.UserRole) if liste.currentItem() else None, dialog))
        buttons.rejected.connect(dialog.reject)
        buttons_layout.addWidget(buttons)
        
        layout.addLayout(buttons_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def mettre_a_jour_date_label(self):
        """Mettre à jour le label de la date affichée"""
        date_obj = datetime.strptime(self.date_courante, "%Y-%m-%d")
        date_format = date_obj.strftime("%d/%m/%Y")
        
        # Vérifier si c'est aujourd'hui
        est_aujourdhui = self.date_courante == datetime.now().strftime("%Y-%m-%d")
        
        if est_aujourdhui:
            self.date_label.setText(f"📅 Rapport du jour - {date_format}")
        else:
            self.date_label.setText(f"📅 Rapport du {date_format}")
    
    def charger_rapport(self, date_rapport, dialog):
        """Charger un rapport spécifique dans l'interface"""
        if not date_rapport:
            return
        
        # Mettre à jour la date courante
        self.date_courante = date_rapport
        self.mettre_a_jour_date_label()
        
        # Obtenir les statistiques du rapport
        stats = self.controller.calculer_solde(date_rapport)
        
        # Mettre à jour les indicateurs
        self.recettes_label.setText(f"{stats['recettes']:,.0f} FC")
        self.depenses_label.setText(f"{stats['depenses']:,.0f} FC")
        
        # Vérifier si clôturé
        est_cloture = self.controller.verifier_cloture(date_rapport)
        
        if not est_cloture:
            self.solde_label.setText("-- FC")
            self.solde_frame.setStyleSheet("""
                QFrame {
                    background-color: #999999;
                    border-radius: 10px;
                    padding: 10px;
                }
            """)
        else:
            self.solde_label.setText(f"{stats['solde']:,.0f} FC")
            from config import COLOR_PRIMARY, COLOR_DANGER
            if stats['solde'] < 0:
                self.solde_frame.setStyleSheet(f"""
                    QFrame {{
                        background-color: {COLOR_DANGER};
                        border-radius: 10px;
                        padding: 10px;
                    }}
                """)
            else:
                self.solde_frame.setStyleSheet(f"""
                    QFrame {{
                        background-color: {COLOR_PRIMARY};
                        border-radius: 10px;
                        padding: 10px;
                    }}
                """)
        
        # Mettre à jour le statut de clôture
        self.actualiser_affichage()
        
        # Charger les transactions du rapport
        transactions = self.controller.obtenir_transactions_par_date(date_rapport)
        self.table.setRowCount(len(transactions))
        
        for row, transaction in enumerate(transactions):
            id_transaction, type_trans, montant, description, date, cloture = transaction
            
            # N°
            num_item = QTableWidgetItem(str(row + 1))
            num_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, num_item)
            
            # Type
            type_item = QTableWidgetItem(type_trans.capitalize())
            type_item.setTextAlignment(Qt.AlignCenter)
            from config import COLOR_SUCCESS, COLOR_DANGER
            if type_trans == "recette":
                type_item.setForeground(QColor(COLOR_SUCCESS))
            else:
                type_item.setForeground(QColor(COLOR_DANGER))
            self.table.setItem(row, 1, type_item)
            
            # Montant
            montant_item = QTableWidgetItem(f"{montant:,.0f}")
            montant_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if type_trans == "recette":
                montant_item.setForeground(QColor(COLOR_SUCCESS))
            else:
                montant_item.setForeground(QColor(COLOR_DANGER))
            self.table.setItem(row, 2, montant_item)
            
            # Description
            desc_item = QTableWidgetItem(description)
            desc_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 3, desc_item)
            
            # Date et Heure
            dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            date_item = QTableWidgetItem(dt.strftime("%d/%m/%Y"))
            date_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, date_item)
            
            heure_item = QTableWidgetItem(dt.strftime("%H:%M"))
            heure_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 5, heure_item)
        
        dialog.accept()
    
    def modifier_transaction(self):
        """Modifier la transaction sélectionnée"""
        if self.parent_window:
            self.parent_window.modifier_transaction()
    
    def supprimer_transaction(self):
        """Supprimer la transaction sélectionnée"""
        if self.parent_window:
            self.parent_window.supprimer_transaction()
    
    def envoyer_rapport(self):
        """Envoyer le rapport clôturé via l'API"""
        from PyQt5.QtWidgets import QMessageBox
        
        # Vérifier que le rapport est bien clôturé
        if not self.controller.verifier_cloture(self.date_courante):
            QMessageBox.warning(
                self,
                "Erreur",
                "Le rapport doit être clôturé avant d'être envoyé."
            )
            return
        
        # Message de confirmation
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirmer l'envoi")
        msg.setText(f"Voulez-vous envoyer le rapport du {datetime.strptime(self.date_courante, '%Y-%m-%d').strftime('%d/%m/%Y')} ?")
        msg.setInformativeText("Le rapport sera envoyé au serveur via l'API.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        
        if msg.exec_() == QMessageBox.Yes:
            try:
                # Ici, vous pouvez ajouter le code pour envoyer via l'API
                # Pour l'instant, on affiche juste un message de succès
                QMessageBox.information(
                    self,
                    "Succès",
                    f"Le rapport du {datetime.strptime(self.date_courante, '%Y-%m-%d').strftime('%d/%m/%Y')} a été envoyé avec succès !"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Erreur",
                    f"Erreur lors de l'envoi du rapport : {str(e)}"
                )
