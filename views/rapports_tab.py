"""
Onglet Rapports - Vue des rapports journaliers
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QFrame, QMessageBox, QHeaderView, QComboBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta


class RapportsTab(QWidget):
    """Onglet pour visualiser et filtrer les rapports"""
    
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        """Initialiser l'interface"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 20, 0, 0)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)
        
        # Container avec marges pour les filtres
        filters_container = QVBoxLayout()
        filters_container.setContentsMargins(20, 0, 20, 0)
        filters_container.setSpacing(20)
        
        # Filtres en haut
        self.create_filters(filters_container)
        
        main_layout.addLayout(filters_container)
        
        # Titre "Résumé de la période" et indicateurs (sans marges)
        self.create_summary_section(main_layout)
        
        # Tableau des rapports (sans marges)
        self.create_reports_table(main_layout)
    
    def create_filters(self, parent_layout):
        """Créer les filtres de période"""
        filters_frame = QFrame()
        filters_frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
                padding: 0px;
            }
        """)
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(15)
        filters_frame.setLayout(filters_layout)

        filters_layout.addStretch()
        
        # Période: Aujourd'hui
        period_label = QLabel("Période:")
        period_label.setFont(QFont("Arial", 11, QFont.Bold))
        filters_layout.addWidget(period_label)
        
        self.period_filter = QComboBox()
        self.period_filter.addItems(["Aujourd'hui", "Cette semaine", "Ce mois", "Cette année", "Personnalisé"])
        self.period_filter.setFont(QFont("Arial", 10))
        self.period_filter.setFixedWidth(150)
        self.period_filter.currentTextChanged.connect(self.on_period_filter_changed)
        self.period_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """)
        filters_layout.addWidget(self.period_filter)
        
        # Mois:
        self.month_label = QLabel("Mois:")
        self.month_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.month_label.setVisible(False)  # Masqué par défaut
        filters_layout.addWidget(self.month_label)
        
        self.month_filter = QComboBox()
        mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        self.month_filter.addItems(mois)
        self.month_filter.setCurrentIndex(datetime.now().month - 1)
        self.month_filter.setFont(QFont("Arial", 10))
        self.month_filter.setFixedWidth(120)
        self.month_filter.currentTextChanged.connect(self.appliquer_filtre)
        self.month_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """)
        self.month_filter.setVisible(False)  # Masqué par défaut
        filters_layout.addWidget(self.month_filter)
        
        # Année
        self.year_label = QLabel("Année:")
        self.year_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.year_label.setVisible(False)  # Masqué par défaut
        filters_layout.addWidget(self.year_label)
        
        self.year_filter = QComboBox()
        current_year = datetime.now().year
        for year in range(current_year - 5, current_year + 2):
            self.year_filter.addItem(str(year))
        self.year_filter.setCurrentText(str(current_year))
        self.year_filter.setFont(QFont("Arial", 10))
        self.year_filter.setFixedWidth(80)
        self.year_filter.currentTextChanged.connect(self.appliquer_filtre)
        self.year_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """)
        self.year_filter.setVisible(False)  # Masqué par défaut
        filters_layout.addWidget(self.year_filter)
        
        # Date spécifique
        self.date_label = QLabel("Date spécifique:")
        self.date_label.setFont(QFont("Arial", 11, QFont.Bold))
        filters_layout.addWidget(self.date_label)
        
        self.date_picker = QDateEdit()
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setFont(QFont("Arial", 10))
        self.date_picker.setFixedWidth(120)
        self.date_picker.setDisplayFormat("dd/MM/yyyy")
        self.date_picker.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """)
        filters_layout.addWidget(self.date_picker)
        
        # Bouton Afficher
        from config import COLOR_PRIMARY
        self.filter_button = QPushButton("📊 Afficher")
        self.filter_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.filter_button.setFixedSize(120, 38)
        self.filter_button.setCursor(Qt.PointingHandCursor)
        self.filter_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                border-radius: 5px;
                border: none;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: #236B8E;
            }}
        """)
        self.filter_button.clicked.connect(lambda: self.afficher_rapport_date(self.date_picker.date().toString("yyyy-MM-dd")))
        filters_layout.addWidget(self.filter_button)
        
        filters_layout.addStretch()
        parent_layout.addWidget(filters_frame)
    
    def create_summary_section(self, parent_layout):
        """Créer la section résumé avec les cartes"""
        # Container pour le titre avec marge
        title_container = QVBoxLayout()
        title_container.setContentsMargins(20, 0, 20, 0)
        
        # Titre
        # title_label = QLabel("Résumé de la période")
        # title_label.setFont(QFont("Arial", 14, QFont.Bold))
        # from config import COLOR_PRIMARY
        # title_label.setStyleSheet(f"color: {COLOR_PRIMARY}; margin-top: 10px; margin-bottom: 10px;")
        # title_container.addWidget(title_label)
        
        parent_layout.addLayout(title_container)
        
        # Frame pour les cartes (sans marges)
        cards_layout = QHBoxLayout()
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(10)
        
        # Carte Recette
        from config import COLOR_SUCCESS, COLOR_DANGER, COLOR_PRIMARY as COLOR_BLUE
        
        recette_card = QFrame()
        recette_card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_SUCCESS};
                border-radius: 8px;
                padding: 20px;
              
            }}
        """)
        recette_layout = QVBoxLayout()
        recette_layout.setSpacing(10)
        
        recette_title = QLabel("💰 Recette")
        recette_title.setFont(QFont("Arial", 12, QFont.Bold))
        recette_title.setStyleSheet("color: rgba(255, 255, 255, 0.9); background-color: transparent; border-radius: 5px; padding: 8px;")
        recette_title.setAlignment(Qt.AlignCenter)
        
        self.recette_value = QLabel("40,000 FC")
        self.recette_value.setFont(QFont("Arial", 24, QFont.Bold))
        self.recette_value.setStyleSheet("color: white; background-color: transparent; border-radius: 5px; padding: 12px;")
        self.recette_value.setAlignment(Qt.AlignCenter)
        
        recette_layout.addWidget(recette_title)
        recette_layout.addWidget(self.recette_value)
        recette_card.setLayout(recette_layout)
        cards_layout.addWidget(recette_card)
        
        # Carte Solde
        solde_card = QFrame()
        solde_card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BLUE};
                border-radius: 8px;
                padding: 20px;
                border-left: 1px solid rgba(255, 255, 255, 0.3);
                border-right: 1px solid rgba(255, 255, 255, 0.3);
            }}
        """)
        solde_layout = QVBoxLayout()
        solde_layout.setSpacing(10)
        
        solde_title = QLabel("💵 Solde")
        solde_title.setFont(QFont("Arial", 12, QFont.Bold))
        solde_title.setStyleSheet("color: rgba(255, 255, 255, 0.9); background-color: transparent; border-radius: 5px; padding: 8px;")
        solde_title.setAlignment(Qt.AlignCenter)
        
        self.solde_value = QLabel("31,000 FC")
        self.solde_value.setFont(QFont("Arial", 36, QFont.Bold))
        self.solde_value.setStyleSheet("color: white; background-color: transparent; border-radius: 5px; padding: 12px;")
        self.solde_value.setAlignment(Qt.AlignCenter)
        
        solde_layout.addWidget(solde_title)
        solde_layout.addWidget(self.solde_value)
        solde_card.setLayout(solde_layout)
        cards_layout.addWidget(solde_card)
        
        # Carte Dépenses
        depense_card = QFrame()
        depense_card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_DANGER};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        depense_layout = QVBoxLayout()
        depense_layout.setSpacing(10)
        
        depense_title = QLabel("📉 Dépenses")
        depense_title.setFont(QFont("Arial", 12, QFont.Bold))
        depense_title.setStyleSheet("color: rgba(255, 255, 255, 0.9); background-color: transparent; border-radius: 5px; padding: 8px;")
        depense_title.setAlignment(Qt.AlignCenter)
        
        self.depense_value = QLabel("9,000 FC")
        self.depense_value.setFont(QFont("Arial", 24, QFont.Bold))
        self.depense_value.setStyleSheet("color: white; background-color: transparent; border-radius: 5px; padding: 12px;")
        self.depense_value.setAlignment(Qt.AlignCenter)
        
        depense_layout.addWidget(depense_title)
        depense_layout.addWidget(self.depense_value)
        depense_card.setLayout(depense_layout)
        cards_layout.addWidget(depense_card)
        
        parent_layout.addLayout(cards_layout)
    
    def create_reports_table(self, parent_layout):
        """Créer le tableau des rapports"""
        self.reports_table = QTableWidget()
        self.reports_table.setColumnCount(5)
        self.reports_table.setHorizontalHeaderLabels(["Date", "Recettes (FC)", "Dépenses (FC)", "Solde (FC)", "Statut"])
        
        # Style du tableau
        self.reports_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                border-radius: 8px;
                gridline-color: #E0E0E0;
            }
            QHeaderView::section {
                background-color: #2E86AB;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #E0E0E0;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: black;
            }
        """)
        
        header = self.reports_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        
        self.reports_table.verticalHeader().setVisible(False)
        self.reports_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.reports_table.setAlternatingRowColors(True)
        
        parent_layout.addWidget(self.reports_table)
    
    def on_period_filter_changed(self, period):
        """Gérer le changement de filtre de période"""
        if period == "Personnalisé":
            self.month_label.setVisible(True)
            self.month_filter.setVisible(True)
            self.year_label.setVisible(True)
            self.year_filter.setVisible(True)
            self.appliquer_filtre()
        else:
            self.month_label.setVisible(False)
            self.month_filter.setVisible(False)
            self.year_label.setVisible(False)
            self.year_filter.setVisible(False)
            self.appliquer_filtre()
    
    def appliquer_filtre(self):
        """Appliquer le filtre sélectionné"""
        period = self.period_filter.currentText()
        
        if period == "Personnalisé":
            # Utiliser le mois et l'année sélectionnés
            mois_index = self.month_filter.currentIndex() + 1  # Janvier = 1
            annee = int(self.year_filter.currentText())
            
            # Premier jour du mois
            from calendar import monthrange
            date_debut = f"{annee}-{mois_index:02d}-01"
            
            # Dernier jour du mois
            dernier_jour = monthrange(annee, mois_index)[1]
            date_fin = f"{annee}-{mois_index:02d}-{dernier_jour:02d}"
            
            # Appeler actualiser_rapports_periode avec les dates
            self.actualiser_rapports_periode(date_debut, date_fin)
        else:
            self.actualiser_rapports()
    
    def actualiser_rapports_periode(self, date_debut, date_fin):
        """Actualiser avec une période personnalisée"""
        # Obtenir les statistiques
        stats = self.controller.obtenir_statistiques_par_jour(date_debut, date_fin)
        
        # Calculer les totaux pour les cartes (uniquement rapports clôturés)
        total_recettes = 0
        total_depenses = 0
        total_solde = 0
        for stat in stats:
            date, recettes, depenses = stat
            est_cloture = self.controller.verifier_cloture(date)
            total_recettes += recettes
            total_depenses += depenses
            # Inclure le solde seulement si clôturé
            if est_cloture:
                total_solde += (recettes - depenses)
        
        # Mettre à jour les cartes de résumé
        self.recette_value.setText(f"{total_recettes:,.0f} FC")
        self.depense_value.setText(f"{total_depenses:,.0f} FC")
        self.solde_value.setText(f"{total_solde:,.0f} FC")
        
        # Remplir le tableau
        self.reports_table.setRowCount(len(stats))
        
        for row, stat in enumerate(stats):
            date, recettes, depenses = stat
            solde = recettes - depenses
            
            # Vérifier si clôturé
            est_cloture = self.controller.verifier_cloture(date)
            statut = "✓ Clôturé" if est_cloture else "En cours"
            
            # Date
            date_item = QTableWidgetItem(datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y"))
            date_item.setTextAlignment(Qt.AlignCenter)
            self.reports_table.setItem(row, 0, date_item)
            
            # Recettes
            recettes_item = QTableWidgetItem(f"{recettes:,.0f}")
            recettes_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.reports_table.setItem(row, 1, recettes_item)
            
            # Dépenses
            depenses_item = QTableWidgetItem(f"{depenses:,.0f}")
            depenses_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.reports_table.setItem(row, 2, depenses_item)
            
            # Solde (seulement si clôturé)
            from config import COLOR_SUCCESS, COLOR_DANGER
            from PyQt5.QtGui import QColor
            if est_cloture:
                solde_item = QTableWidgetItem(f"{solde:,.0f}")
                solde_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                if solde >= 0:
                    solde_item.setForeground(QColor(COLOR_SUCCESS))
                else:
                    solde_item.setForeground(QColor(COLOR_DANGER))
            else:
                solde_item = QTableWidgetItem("--")
                solde_item.setTextAlignment(Qt.AlignCenter)
            self.reports_table.setItem(row, 3, solde_item)
            
            # Statut
            statut_item = QTableWidgetItem(statut)
            statut_item.setTextAlignment(Qt.AlignCenter)
            if est_cloture:
                statut_item.setForeground(QColor(COLOR_SUCCESS))
            self.reports_table.setItem(row, 4, statut_item)
    
    def actualiser_rapports(self):
        """Actualiser la liste des rapports selon le filtre"""
        period = self.period_filter.currentText()
        
        date_debut = None
        date_fin = None
        
        if period == "Aujourd'hui":
            date_debut = date_fin = datetime.now().strftime("%Y-%m-%d")
        elif period == "Cette semaine":
            today = datetime.now()
            start_week = today - timedelta(days=today.weekday())
            date_debut = start_week.strftime("%Y-%m-%d")
            date_fin = datetime.now().strftime("%Y-%m-%d")
        elif period == "Ce mois":
            today = datetime.now()
            date_debut = today.replace(day=1).strftime("%Y-%m-%d")
            date_fin = today.strftime("%Y-%m-%d")
        elif period == "Cette année":
            today = datetime.now()
            date_debut = today.replace(month=1, day=1).strftime("%Y-%m-%d")
            date_fin = today.strftime("%Y-%m-%d")
        
        # Obtenir les statistiques
        stats = self.controller.obtenir_statistiques_par_jour(date_debut, date_fin)
        
        # Calculer les totaux pour les cartes
        total_recettes = 0
        total_depenses = 0
        total_solde = 0
        for stat in stats:
            date, recettes, depenses = stat
            total_recettes += recettes
            total_depenses += depenses
            # Solde seulement pour rapports clôturés
            est_cloture = self.controller.verifier_cloture(date)
            if est_cloture:
                total_solde += (recettes - depenses)
        
        # Mettre à jour les cartes de résumé
        self.recette_value.setText(f"{total_recettes:,.0f} FC")
        self.depense_value.setText(f"{total_depenses:,.0f} FC")
        self.solde_value.setText(f"{total_solde:,.0f} FC")
        
        # Remplir le tableau
        self.reports_table.setRowCount(len(stats))
        
        for row, stat in enumerate(stats):
            date, recettes, depenses = stat
            solde = recettes - depenses
            
            # Vérifier si clôturé
            est_cloture = self.controller.verifier_cloture(date)
            statut = "✓ Clôturé" if est_cloture else "En cours"
            
            # Date
            date_item = QTableWidgetItem(datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y"))
            date_item.setTextAlignment(Qt.AlignCenter)
            self.reports_table.setItem(row, 0, date_item)
            
            # Recettes
            recettes_item = QTableWidgetItem(f"{recettes:,.0f}")
            recettes_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.reports_table.setItem(row, 1, recettes_item)
            
            # Dépenses
            depenses_item = QTableWidgetItem(f"{depenses:,.0f}")
            depenses_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.reports_table.setItem(row, 2, depenses_item)
            
            # Solde (seulement si clôturé)
            from config import COLOR_SUCCESS, COLOR_DANGER
            from PyQt5.QtGui import QColor
            if est_cloture:
                solde_item = QTableWidgetItem(f"{solde:,.0f}")
                solde_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                if solde >= 0:
                    solde_item.setForeground(QColor(COLOR_SUCCESS))
                else:
                    solde_item.setForeground(QColor(COLOR_DANGER))
            else:
                solde_item = QTableWidgetItem("--")
                solde_item.setTextAlignment(Qt.AlignCenter)
            self.reports_table.setItem(row, 3, solde_item)
            
            # Statut
            statut_item = QTableWidgetItem(statut)
            statut_item.setTextAlignment(Qt.AlignCenter)
            if est_cloture:
                statut_item.setForeground(QColor(COLOR_SUCCESS))
            self.reports_table.setItem(row, 4, statut_item)
    
    def actualiser(self):
        """Méthode générique d'actualisation"""
        self.actualiser_rapports()
    
    def afficher_rapport_date(self, date):
        """Afficher le rapport pour une date spécifique"""
        stats = self.controller.calculer_solde(date)
        
        # Mettre à jour les cartes de résumé
        self.recette_value.setText(f"{stats['recettes']:,.0f} FC")
        self.depense_value.setText(f"{stats['depenses']:,.0f} FC")
        self.solde_value.setText(f"{stats['solde']:,.0f} FC")
        
        self.reports_table.setRowCount(1)
        
        # Date
        date_item = QTableWidgetItem(datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y"))
        date_item.setTextAlignment(Qt.AlignCenter)
        self.reports_table.setItem(0, 0, date_item)
        
        # Recettes
        recettes_item = QTableWidgetItem(f"{stats['recettes']:,.0f}")
        recettes_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.reports_table.setItem(0, 1, recettes_item)
        
        # Dépenses
        depenses_item = QTableWidgetItem(f"{stats['depenses']:,.0f}")
        depenses_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.reports_table.setItem(0, 2, depenses_item)
        
        # Solde
        solde_item = QTableWidgetItem(f"{stats['solde']:,.0f}")
        solde_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.reports_table.setItem(0, 3, solde_item)
        
        # Statut
        est_cloture = self.controller.verifier_cloture(date)
        statut = "✓ Clôturé" if est_cloture else "En cours"
        statut_item = QTableWidgetItem(statut)
        statut_item.setTextAlignment(Qt.AlignCenter)
        self.reports_table.setItem(0, 4, statut_item)
