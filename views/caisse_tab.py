"""
Onglet Caisse - Gestion de la caisse
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
                             QFrame, QMessageBox, QHeaderView, QDialog, QDialogButtonBox,
                             QComboBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor
from datetime import datetime, timedelta
from config import (FONT_FAMILY, FONT_SIZE_SM, FONT_SIZE_MD, FONT_SIZE_LG, 
                    FONT_SIZE_XL, FONT_SIZE_XXL)

class CaisseTab(QWidget):
    """Onglet pour gérer la caisse (dépenses spéciales et apports)"""
    
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        """Initialiser l'interface"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 18, 0, 0)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)
        
        # # Titre avec marge
        # title_container = QVBoxLayout()
        # title_container.setContentsMargins(0, 0, 0, 0)
        
        # from config import COLOR_PRIMARY
        # details_title = QLabel("📋 Composition de la Caisse")
        # details_title.setFont(QFont("Arial", 14, QFont.Bold))
        # details_title.setStyleSheet(f"color: {COLOR_PRIMARY}; background-color: transparent; border: none;")
        # title_container.addWidget(details_title)
        
        # main_layout.addLayout(title_container)
        # 
        # Composition de la caisse (sans marges)
        self.create_caisse_details(main_layout)
        
        # Filtres avec marge
        filters_container = QVBoxLayout()
        filters_container.setContentsMargins(0, 0, 0, 0)
        self.create_filters(filters_container)
        main_layout.addLayout(filters_container)
        
        # Tableau (sans marges)
        self.create_table(main_layout)
    
    def create_caisse_details(self, parent_layout):
        """Créer l'affichage de la composition de la caisse"""
        from config import COLOR_PRIMARY
        
        # Section indicateurs avec marge
        indicators_container = QVBoxLayout()
        indicators_container.setContentsMargins(0, 0, 0, 0)
        
        # Titre et filtre de période pour les indicateurs
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        
        
        header_layout.addStretch()
        
        # Filtre de période pour les indicateurs
        period_label = QLabel("Période :")
        period_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD, QFont.Bold))
        header_layout.addWidget(period_label)
        
        self.indicators_period_filter = QComboBox()
        self.indicators_period_filter.addItems(["Ce mois", "Aujourd'hui", "Cette semaine", "Mois spécifique", "Toutes"])
        self.indicators_period_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 150px;
            }
            QComboBox:focus {
                border: 2px solid #2E86AB;
            }
        """)
        self.indicators_period_filter.currentTextChanged.connect(self.on_indicators_period_changed)
        header_layout.addWidget(self.indicators_period_filter)
        
        # Sélecteur de mois
        self.indicators_month_label = QLabel("Mois :")
        self.indicators_month_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD, QFont.Bold))
        self.indicators_month_label.hide()
        header_layout.addWidget(self.indicators_month_label)
        
        self.indicators_month_combo = QComboBox()
        mois_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                   "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        current_year = datetime.now().year
        for i, mois in enumerate(mois_fr):
            self.indicators_month_combo.addItem(mois, (current_year, i + 1))
        # Sélectionner le mois courant
        self.indicators_month_combo.setCurrentIndex(datetime.now().month - 1)
        self.indicators_month_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 150px;
            }
            QComboBox:focus {
                border: 2px solid #2E86AB;
            }
        """)
        self.indicators_month_combo.currentIndexChanged.connect(self.actualiser_indicateurs)
        self.indicators_month_combo.hide()
        header_layout.addWidget(self.indicators_month_combo)
        
        indicators_container.addLayout(header_layout)
        
        # Cartes horizontales (3 cartes)
        cards_layout = QHBoxLayout()
        cards_layout.setContentsMargins(0, 10, 0, 0)
        cards_layout.setSpacing(15)
        
        # Soldes clôturés / Recettes
        from config import COLOR_SUCCESS, COLOR_DANGER
        solde_card = self.create_info_card("✅ Soldes Clôturés", "0.00 FC", COLOR_SUCCESS)
        self.caisse_solde_cloture = solde_card[1]
        self.caisse_solde_card_title = solde_card[2]  # Stocker le label du titre
        cards_layout.addWidget(solde_card[0])
        
        # Apports
        apports_card = self.create_info_card("💰 Apports", "0.00 FC", COLOR_SUCCESS)
        self.caisse_apports = apports_card[1]
        cards_layout.addWidget(apports_card[0])
        
        # Dépenses spéciales
        depenses_card = self.create_info_card("💸 Dépenses", "0.00 FC", COLOR_DANGER)
        self.caisse_depenses_speciales = depenses_card[1]
        cards_layout.addWidget(depenses_card[0])
        
        indicators_container.addLayout(cards_layout)
        parent_layout.addLayout(indicators_container)
    
    def create_info_card(self, title, value, color):
        """Créer une carte d'information"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD, QFont.Bold))
        title_label.setStyleSheet("color: white; background-color: transparent;")
        title_label.setAlignment(Qt.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_XXL, QFont.Bold))
        value_label.setStyleSheet("color: white; background-color: transparent;")
        value_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.setLayout(layout)
        
        return (card, value_label, title_label)
    
    def create_filters(self, parent_layout):
        """Créer les filtres"""
        # Section filtres
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(15)
        
        # Filtre par type
        type_label = QLabel("Type :")
        type_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD, QFont.Bold))
        filters_layout.addWidget(type_label)
        
        self.type_filter = QComboBox()
        self.type_filter.addItems(["Tous", "Apports", "Dépenses"])
        self.type_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 150px;
            }
            QComboBox:focus {
                border: 2px solid #2E86AB;
            }
        """)
        self.type_filter.currentTextChanged.connect(self.appliquer_filtres)
        filters_layout.addWidget(self.type_filter)
        
        # Filtre par période
        period_label = QLabel("Période :")
        period_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD, QFont.Bold))
        filters_layout.addWidget(period_label)
        
        self.period_filter = QComboBox()
        self.period_filter.addItems(["Toutes", "Aujourd'hui", "Cette semaine", "Ce mois", "Personnalisé"])
        self.period_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 150px;
            }
            QComboBox:focus {
                border: 2px solid #2E86AB;
            }
        """)
        self.period_filter.currentTextChanged.connect(self.on_period_changed)
        filters_layout.addWidget(self.period_filter)
        
        # Dates personnalisées
        date_debut_label = QLabel("Du :")
        date_debut_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD, QFont.Bold))
        self.date_debut_label = date_debut_label
        filters_layout.addWidget(date_debut_label)
        
        self.date_debut = QDateEdit()
        self.date_debut.setCalendarPopup(True)
        self.date_debut.setDate(QDate.currentDate().addDays(-30))
        self.date_debut.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 120px;
            }
            QDateEdit:focus {
                border: 2px solid #2E86AB;
            }
        """)
        self.date_debut.dateChanged.connect(self.appliquer_filtres)
        filters_layout.addWidget(self.date_debut)
        
        date_fin_label = QLabel("Au :")
        date_fin_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.date_fin_label = date_fin_label
        filters_layout.addWidget(date_fin_label)
        
        self.date_fin = QDateEdit()
        self.date_fin.setCalendarPopup(True)
        self.date_fin.setDate(QDate.currentDate())
        self.date_fin.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                min-width: 120px;
            }
            QDateEdit:focus {
                border: 2px solid #2E86AB;
            }
        """)
        self.date_fin.dateChanged.connect(self.appliquer_filtres)
        filters_layout.addWidget(self.date_fin)
        
        # Cacher les dates par défaut
        self.date_debut_label.hide()
        self.date_debut.hide()
        self.date_fin_label.hide()
        self.date_fin.hide()
        
        filters_layout.addStretch()
        parent_layout.addLayout(filters_layout)
    
    def create_table(self, parent_layout):
        """Créer le tableau unifié"""
        # Titre et boutons avec marge
        title_container = QHBoxLayout()
        title_container.setContentsMargins(20, 0, 20, 0)
        
        table_label = QLabel("📋 Historique des Mouvements de Caisse")
        table_label.setFont(QFont("Arial", 13, QFont.Bold))
        title_container.addWidget(table_label)
        
        title_container.addStretch()
        
        # Bouton Dépense
        from config import COLOR_DANGER, COLOR_SUCCESS
        depense_btn = QPushButton("💸 Dépense")
        depense_btn.setFont(QFont("Arial", 10, QFont.Bold))
        depense_btn.setCursor(Qt.PointingHandCursor)
        depense_btn.setFixedSize(120, 35)
        depense_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_DANGER};
                color: white;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #B01835;
            }}
        """)
        depense_btn.clicked.connect(self.ouvrir_dialog_depense)
        title_container.addWidget(depense_btn)
        
        # Bouton Apport
        apport_btn = QPushButton("💰 Apport")
        apport_btn.setFont(QFont("Arial", 10, QFont.Bold))
        apport_btn.setCursor(Qt.PointingHandCursor)
        apport_btn.setFixedSize(120, 35)
        apport_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_SUCCESS};
                color: white;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #058A65;
            }}
        """)
        apport_btn.clicked.connect(self.ouvrir_dialog_apport)
        title_container.addWidget(apport_btn)
        
        parent_layout.addLayout(title_container)
        
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(5)
        self.transactions_table.setHorizontalHeaderLabels(["Date", "Heure", "Type", "Description", "Montant (FC)"])
        self.configure_table(self.transactions_table)
        parent_layout.addWidget(self.transactions_table)
    
    def on_period_changed(self):
        """Gérer le changement de période"""
        period = self.period_filter.currentText()
        
        if period == "Personnalisé":
            self.date_debut_label.show()
            self.date_debut.show()
            self.date_fin_label.show()
            self.date_fin.show()
        else:
            self.date_debut_label.hide()
            self.date_debut.hide()
            self.date_fin_label.hide()
            self.date_fin.hide()
        
        self.appliquer_filtres()
    
    def appliquer_filtres(self):
        """Appliquer les filtres au tableau"""
        # Obtenir toutes les transactions (apports et dépenses)
        depenses = self.controller.obtenir_depenses_speciales()
        apports = self.controller.obtenir_apports()
        
        # Combiner et marquer le type
        transactions = []
        for dep in depenses:
            id_dep, montant, description, date, created_at = dep
            transactions.append(("depense", montant, description, date, created_at))
        
        for app in apports:
            id_app, montant, description, date, created_at = app
            transactions.append(("apport", montant, description, date, created_at))
        
        # Filtrer par type
        type_filter = self.type_filter.currentText()
        if type_filter == "Apports":
            transactions = [t for t in transactions if t[0] == "apport"]
        elif type_filter == "Dépenses":
            transactions = [t for t in transactions if t[0] == "depense"]
        
        # Filtrer par période
        period = self.period_filter.currentText()
        today = datetime.now().date()
        
        if period == "Aujourd'hui":
            date_debut = today
            date_fin = today
            transactions = [t for t in transactions if datetime.strptime(t[3], "%Y-%m-%d").date() == today]
        elif period == "Cette semaine":
            # Lundi de cette semaine
            date_debut = today - timedelta(days=today.weekday())
            date_fin = today
            transactions = [t for t in transactions if date_debut <= datetime.strptime(t[3], "%Y-%m-%d").date() <= date_fin]
        elif period == "Ce mois":
            date_debut = today.replace(day=1)
            date_fin = today
            transactions = [t for t in transactions if date_debut <= datetime.strptime(t[3], "%Y-%m-%d").date() <= date_fin]
        elif period == "Personnalisé":
            date_debut = self.date_debut.date().toPyDate()
            date_fin = self.date_fin.date().toPyDate()
            transactions = [t for t in transactions if date_debut <= datetime.strptime(t[3], "%Y-%m-%d").date() <= date_fin]
        
        # Trier par date décroissante
        transactions.sort(key=lambda x: (x[3], x[4]), reverse=True)
        
        # Afficher dans le tableau
        self.transactions_table.setRowCount(len(transactions))
        
        from config import COLOR_SUCCESS, COLOR_DANGER
        
        for row, transaction in enumerate(transactions):
            type_trans, montant, description, date, created_at = transaction
            
            # Alterner les couleurs de fond
            row_color = QColor("#F8F9FA") if row % 2 == 0 else QColor("#FFFFFF")
            
            # Date
            date_item = QTableWidgetItem(datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y"))
            date_item.setTextAlignment(Qt.AlignCenter)
            date_item.setBackground(row_color)
            self.transactions_table.setItem(row, 0, date_item)
            
            # Heure
            heure = created_at.split()[1][:5] if len(created_at.split()) > 1 else ""
            heure_item = QTableWidgetItem(heure)
            heure_item.setTextAlignment(Qt.AlignCenter)
            heure_item.setBackground(row_color)
            self.transactions_table.setItem(row, 1, heure_item)
            
            # Type
            type_label = "💰 Apport" if type_trans == "apport" else "💸 Dépense"
            type_item = QTableWidgetItem(type_label)
            type_item.setTextAlignment(Qt.AlignCenter)
            type_item.setBackground(row_color)
            if type_trans == "apport":
                type_item.setForeground(QColor(COLOR_SUCCESS))
            else:
                type_item.setForeground(QColor(COLOR_DANGER))
            self.transactions_table.setItem(row, 2, type_item)
            
            # Description
            desc_item = QTableWidgetItem(description or "-")
            desc_item.setBackground(row_color)
            self.transactions_table.setItem(row, 3, desc_item)
            
            # Montant
            signe = "+" if type_trans == "apport" else "-"
            montant_item = QTableWidgetItem(f"{signe}{montant:,.0f}")
            montant_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            montant_item.setBackground(row_color)
            if type_trans == "apport":
                montant_item.setForeground(QColor(COLOR_SUCCESS))
            else:
                montant_item.setForeground(QColor(COLOR_DANGER))
            self.transactions_table.setItem(row, 4, montant_item)
    
    def configure_table(self, table):
        """Configurer le style d'un tableau"""
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                border-radius: 0px;
                gridline-color: #E0E0E0;
            }
            QHeaderView::section {
                background-color: #2E86AB;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #E0E0E0;
            }
        """)
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QTableWidget.SelectRows)
    
    def get_input_style(self):
        """Style pour les champs de saisie"""
        return """
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #2E86AB;
            }
        """
    
    def on_indicators_period_changed(self):
        """Gérer le changement de période pour les indicateurs"""
        period = self.indicators_period_filter.currentText()
        
        if period == "Mois spécifique":
            self.indicators_month_label.show()
            self.indicators_month_combo.show()
        else:
            self.indicators_month_label.hide()
            self.indicators_month_combo.hide()
        
        self.actualiser_indicateurs()
    
    def actualiser_indicateurs(self):
        """Actualiser les indicateurs selon la période sélectionnée"""
        period = self.indicators_period_filter.currentText()
        today = datetime.now().date()
        
        # Mettre à jour le titre de la carte selon la période
        if period == "Ce mois":
            self.caisse_solde_card_title.setText("💵 Recettes Mensuelles")
        elif period == "Cette semaine":
            self.caisse_solde_card_title.setText("💵 Recettes Hebdo")
        elif period == "Aujourd'hui":
            self.caisse_solde_card_title.setText("💵 Recettes du Jour")
        elif period == "Mois spécifique":
            year, month = self.indicators_month_combo.currentData()
            mois_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                       "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
            self.caisse_solde_card_title.setText(f"💵 Recettes {mois_fr[month-1]}")
        else:  # Toutes
            self.caisse_solde_card_title.setText("💵 Recettes Totales")
        
        # Définir les dates selon la période
        if period == "Aujourd'hui":
            date_debut = today
            date_fin = today
        elif period == "Cette semaine":
            date_debut = today - timedelta(days=today.weekday())
            date_fin = today
        elif period == "Ce mois":
            date_debut = today.replace(day=1)
            date_fin = today
        elif period == "Mois spécifique":
            year, month = self.indicators_month_combo.currentData()
            date_debut = datetime(year, month, 1).date()
            # Dernier jour du mois
            if month == 12:
                date_fin = datetime(year, 12, 31).date()
            else:
                date_fin = (datetime(year, month + 1, 1) - timedelta(days=1)).date()
        else:  # Toutes
            date_debut = None
            date_fin = None
        
        # Calculer la caisse avec filtre de période
        if date_debut and date_fin:
            date_debut_str = date_debut.strftime("%Y-%m-%d")
            date_fin_str = date_fin.strftime("%Y-%m-%d")
            caisse_data = self.controller.calculer_caisse(date_debut_str, date_fin_str)
        else:
            caisse_data = self.controller.calculer_caisse()
        
        self.caisse_solde_cloture.setText(f"{caisse_data['solde_cloture']:,.0f} FC")
        self.caisse_depenses_speciales.setText(f"{caisse_data['depenses_speciales']:,.0f} FC")
        self.caisse_apports.setText(f"{caisse_data['apports']:,.0f} FC")
    
    def actualiser(self):
        """Actualiser l'affichage de la caisse"""
        # Actualiser les indicateurs
        self.actualiser_indicateurs()
        
        # Actualiser le tableau avec filtres
        self.appliquer_filtres()
    
    def ouvrir_dialog_depense(self):
        """Ouvrir le dialog pour ajouter une dépense spéciale"""
        dialog = DepenseDialog(self.controller, self)
        if dialog.exec_() == QDialog.Accepted:
            self.actualiser()
            if self.parent_window:
                self.parent_window.actualiser_dashboard()
    
    def ouvrir_dialog_apport(self):
        """Ouvrir le dialog pour ajouter un apport"""
        dialog = ApportDialog(self.controller, self)
        if dialog.exec_() == QDialog.Accepted:
            self.actualiser()
            if self.parent_window:
                self.parent_window.actualiser_dashboard()


class DepenseDialog(QDialog):
    """Dialog pour ajouter une dépense spéciale"""
    
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent_tab = parent
        self.init_ui()
    
    def init_ui(self):
        """Initialiser l'interface du dialog"""
        from config import COLOR_DANGER
        
        self.setWindowTitle("Ajouter une Dépense Spéciale")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Titre
        title = QLabel("💸 Nouvelle Dépense Spéciale")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet(f"color: {COLOR_DANGER};")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Formulaire
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Montant
        montant_label = QLabel("Montant (FC):")
        montant_label.setFont(QFont("Arial", 11, QFont.Bold))
        form_layout.addWidget(montant_label)
        
        self.montant_input = QLineEdit()
        self.montant_input.setPlaceholderText("Entrez le montant")
        self.montant_input.setFont(QFont("Arial", 12))
        self.montant_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 12pt;
            }
            QLineEdit:focus {
                border: 2px solid #DC3545;
            }
        """)
        form_layout.addWidget(self.montant_input)
        
        # Description
        desc_label = QLabel("Description:")
        desc_label.setFont(QFont("Arial", 11, QFont.Bold))
        form_layout.addWidget(desc_label)
        
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Entrez la description")
        self.description_input.setFont(QFont("Arial", 12))
        self.description_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 12pt;
            }
            QLineEdit:focus {
                border: 2px solid #DC3545;
            }
        """)
        form_layout.addWidget(self.description_input)
        
        layout.addLayout(form_layout)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setFont(QFont("Arial", 11))
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 10px 30px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        buttons_layout.addStretch()
        
        add_btn = QPushButton("Ajouter")
        add_btn.setFont(QFont("Arial", 11, QFont.Bold))
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_DANGER};
                color: white;
                padding: 10px 30px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #B01835;
            }}
        """)
        add_btn.clicked.connect(self.ajouter_depense)
        buttons_layout.addWidget(add_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def ajouter_depense(self):
        """Ajouter la dépense avec analyse"""
        montant = self.montant_input.text().strip()
        description = self.description_input.text().strip()
        
        if not montant or not description:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
            return
        
        try:
            montant_float = float(montant)
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Le montant doit être un nombre valide")
            return
        
        # Analyser l'impact sur la caisse
        caisse_data = self.controller.calculer_caisse()
        caisse_actuelle = caisse_data['caisse']
        nouvelle_caisse = caisse_actuelle - montant_float
        
        # Construire le message d'analyse
        message_analyse = f"<b>Analyse de l'impact sur la caisse :</b><br><br>"
        message_analyse += f"• Montant en caisse actuel : <b>{caisse_actuelle:,.0f} FC</b><br>"
        message_analyse += f"• Dépense à effectuer : <b>{montant_float:,.0f} FC</b><br>"
        message_analyse += f"• Nouvelle caisse : <b>{nouvelle_caisse:,.0f} FC</b><br><br>"
        
        # Avertissements selon le niveau de risque
        warnings = []
        niveau_risque = "normal"
        
        if nouvelle_caisse < 0:
            warnings.append("⛔ <b>ALERTE CRITIQUE :</b> La caisse sera négative !")
            warnings.append("   → Vous dépensez plus que ce qui est disponible")
            niveau_risque = "critique"
        elif nouvelle_caisse < caisse_actuelle * 0.2:
            warnings.append("⚠️ <b>ATTENTION :</b> Il restera moins de 20% de la caisse")
            warnings.append("   → Envisagez un apport en capital si nécessaire")
            niveau_risque = "eleve"
        elif nouvelle_caisse < caisse_actuelle * 0.5:
            warnings.append("ℹ️ <b>INFO :</b> Il restera moins de 50% de la caisse")
            warnings.append("   → Surveillez vos dépenses")
            niveau_risque = "moyen"
        else:
            warnings.append("✅ <b>SANTÉ BONNE :</b> La caisse reste saine")
            warnings.append("   → Dépense raisonnable")
        
        # Pourcentage de la dépense par rapport à la caisse
        if caisse_actuelle > 0:
            pourcentage = (montant_float / caisse_actuelle) * 100
            warnings.append(f"   → Dépense = {pourcentage:.1f}% de la caisse")
        
        message_analyse += "<br>".join(warnings)
        message_analyse += "<br><br><b>Voulez-vous confirmer cette dépense ?</b>"
        
        # Créer une boîte de dialogue de confirmation
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirmation de Dépense")
        msg_box.setText(message_analyse)
        
        # Icône selon le niveau de risque
        if niveau_risque == "critique":
            msg_box.setIcon(QMessageBox.Critical)
        elif niveau_risque == "eleve":
            msg_box.setIcon(QMessageBox.Warning)
        else:
            msg_box.setIcon(QMessageBox.Information)
        
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No if niveau_risque == "critique" else QMessageBox.Yes)
        
        # Afficher et attendre la réponse
        reponse = msg_box.exec_()
        
        if reponse != QMessageBox.Yes:
            return
        
        # Procéder à l'ajout
        try:
            transaction_id = self.controller.ajouter_transaction(
                "depense", montant_float, description, "speciale"
            )
            
            if transaction_id:
                QMessageBox.information(self, "Succès", "Dépense spéciale ajoutée avec succès")
                self.accept()
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors de l'ajout de la dépense")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur: {str(e)}")


class ApportDialog(QDialog):
    """Dialog pour ajouter un apport en capital"""
    
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent_tab = parent
        self.init_ui()
    
    def init_ui(self):
        """Initialiser l'interface du dialog"""
        from config import COLOR_SUCCESS
        
        self.setWindowTitle("Ajouter un Apport en Capital")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Titre
        title = QLabel("💰 Nouvel Apport en Capital")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet(f"color: {COLOR_SUCCESS};")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Formulaire
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Montant
        montant_label = QLabel("Montant (FC):")
        montant_label.setFont(QFont("Arial", 11, QFont.Bold))
        form_layout.addWidget(montant_label)
        
        self.montant_input = QLineEdit()
        self.montant_input.setPlaceholderText("Entrez le montant")
        self.montant_input.setFont(QFont("Arial", 12))
        self.montant_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 12pt;
            }
            QLineEdit:focus {
                border: 2px solid #07B584;
            }
        """)
        form_layout.addWidget(self.montant_input)
        
        # Description
        desc_label = QLabel("Description:")
        desc_label.setFont(QFont("Arial", 11, QFont.Bold))
        form_layout.addWidget(desc_label)
        
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Entrez la description")
        self.description_input.setFont(QFont("Arial", 12))
        self.description_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 12pt;
            }
            QLineEdit:focus {
                border: 2px solid #07B584;
            }
        """)
        form_layout.addWidget(self.description_input)
        
        layout.addLayout(form_layout)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setFont(QFont("Arial", 11))
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 10px 30px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        buttons_layout.addStretch()
        
        add_btn = QPushButton("Ajouter")
        add_btn.setFont(QFont("Arial", 11, QFont.Bold))
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_SUCCESS};
                color: white;
                padding: 10px 30px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #058A65;
            }}
        """)
        add_btn.clicked.connect(self.ajouter_apport)
        buttons_layout.addWidget(add_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def ajouter_apport(self):
        """Ajouter l'apport"""
        montant = self.montant_input.text().strip()
        description = self.description_input.text().strip()
        
        if not montant or not description:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
            return
        
        try:
            montant_float = float(montant)
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Le montant doit être un nombre valide")
            return
        
        # Procéder à l'ajout
        try:
            transaction_id = self.controller.ajouter_transaction(
                "apport", montant_float, description, "speciale"
            )
            
            if transaction_id:
                QMessageBox.information(self, "Succès", "Apport en capital ajouté avec succès")
                self.accept()
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors de l'ajout de l'apport")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur: {str(e)}")
