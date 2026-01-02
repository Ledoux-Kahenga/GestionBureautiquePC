"""
Dialogue de modification de transaction
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QRadioButton, QButtonGroup,
                             QMessageBox, QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config import (FONT_FAMILY, FONT_SIZE_SM, FONT_SIZE_MD, FONT_SIZE_XXL)

class ModifierTransactionDialog(QDialog):
    """Fenêtre de dialogue pour modifier une transaction"""
    
    def __init__(self, transaction, parent=None):
        super().__init__(parent)
        self.transaction = transaction
        self.setup_ui()
        
    def setup_ui(self):
        """Configurer l'interface de la fenêtre"""
        from config import COLOR_PRIMARY, COLOR_SUCCESS, COLOR_DANGER
        
        self.setWindowTitle("Modifier la transaction")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titre
        title = QLabel("✏️ Modifier la transaction")
        title.setFont(QFont(FONT_FAMILY, FONT_SIZE_XXL, QFont.Bold))
        title.setStyleSheet(f"color: {COLOR_PRIMARY};")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # ID (non modifiable, juste pour info)
        id_layout = QHBoxLayout()
        id_label = QLabel("ID:")
        id_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD))
        id_layout.addWidget(id_label)
        
        id_value = QLabel(str(self.transaction[0]))
        id_value.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD, QFont.Bold))
        id_layout.addWidget(id_value)
        id_layout.addStretch()
        layout.addLayout(id_layout)
        
        # Type de transaction
        type_layout = QHBoxLayout()
        type_label = QLabel("Type:")
        type_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD))
        type_layout.addWidget(type_label)
        
        self.type_group = QButtonGroup()
        self.recette_radio = QRadioButton("Recette")
        self.depense_radio = QRadioButton("Dépense")
        self.recette_radio.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        self.depense_radio.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
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
        type_depense_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD))
        self.type_depense_layout.addWidget(type_depense_label)
        
        self.type_depense_group = QButtonGroup()
        self.depense_normale_radio = QRadioButton("Normale (journalière)")
        self.depense_speciale_radio = QRadioButton("Spéciale (caisse)")
        self.depense_normale_radio.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        self.depense_speciale_radio.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        
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
        montant_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD))
        montant_label.setFixedWidth(120)
        montant_layout.addWidget(montant_label)
        
        self.montant_entry = QLineEdit()
        self.montant_entry.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD))
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
        desc_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD))
        desc_label.setFixedWidth(120)
        desc_layout.addWidget(desc_label)
        
        self.description_entry = QLineEdit()
        self.description_entry.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD))
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
        cancel_button.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD))
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
        save_button.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD, QFont.Bold))
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
