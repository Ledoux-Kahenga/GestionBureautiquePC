"""
Onglet Paramètres - Configuration de l'application
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QCheckBox, QSpinBox,
                             QComboBox, QLineEdit, QFileDialog, QMessageBox,
                             QGroupBox, QFormLayout, QTimeEdit, QTableWidget,
                             QTableWidgetItem, QHeaderView, QDialog, QDialogButtonBox,
                             QProgressBar)
from PyQt5.QtCore import Qt, QTime, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from datetime import datetime
import os

from config import (FONT_FAMILY, FONT_SIZE_SM, FONT_SIZE_MD, FONT_SIZE_LG, 
                    FONT_SIZE_XL, FONT_SIZE_XXL, COLOR_PRIMARY, COLOR_SUCCESS, 
                    COLOR_DANGER, COLOR_SECONDARY)
from utils.backup import BackupManager


class BackupThread(QThread):
    """Thread pour effectuer les sauvegardes sans bloquer l'interface"""
    finished = pyqtSignal(bool, str)
    
    def __init__(self, backup_manager, description=""):
        super().__init__()
        self.backup_manager = backup_manager
        self.description = description
    
    def run(self):
        success, result = self.backup_manager.create_backup(self.description)
        self.finished.emit(success, result)


class ExportThread(QThread):
    """Thread pour l'export des données"""
    finished = pyqtSignal(bool, str)
    
    def __init__(self, backup_manager, export_path, format_type):
        super().__init__()
        self.backup_manager = backup_manager
        self.export_path = export_path
        self.format_type = format_type
    
    def run(self):
        success, result = self.backup_manager.export_data(self.export_path, self.format_type)
        self.finished.emit(success, result)


class SettingsTab(QWidget):
    """Onglet pour gérer les paramètres de l'application"""
    
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent_window = parent
        self.backup_manager = BackupManager()
        self.settings = self.backup_manager.load_settings()
        self.init_ui()
        self.load_current_settings()
    
    def init_ui(self):
        """Initialiser l'interface"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)
        
        # Titre
        title = QLabel("⚙️ Paramètres de l'application")
        title.setFont(QFont(FONT_FAMILY, FONT_SIZE_XXL, QFont.Bold))
        title.setStyleSheet(f"color: {COLOR_PRIMARY};")
        main_layout.addWidget(title)
        
        # Conteneur scrollable
        from PyQt5.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        content.setLayout(content_layout)
        
        # Section Sauvegarde
        self.create_backup_section(content_layout)
        
        # Section Export/Import
        self.create_export_import_section(content_layout)
        
        # Section Apparence
        self.create_appearance_section(content_layout)
        
        # Section Clôture automatique
        self.create_cloture_section(content_layout)
        
        # Section Sauvegardes existantes
        self.create_backups_list_section(content_layout)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        
        # Bouton Enregistrer
        save_layout = QHBoxLayout()
        save_layout.addStretch()
        
        self.save_button = QPushButton("💾 Enregistrer les paramètres")
        self.save_button.setFont(QFont(FONT_FAMILY, FONT_SIZE_MD, QFont.Bold))
        self.save_button.setFixedSize(250, 45)
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                border-radius: 8px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #1E6A8F;
            }}
        """)
        self.save_button.clicked.connect(self.save_settings)
        save_layout.addWidget(self.save_button)
        
        main_layout.addLayout(save_layout)
    
    def create_section_frame(self, title, icon=""):
        """Créer un cadre de section"""
        group = QGroupBox(f"{icon} {title}")
        group.setFont(QFont(FONT_FAMILY, FONT_SIZE_LG, QFont.Bold))
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
                color: {COLOR_PRIMARY};
            }}
        """)
        return group
    
    def create_backup_section(self, parent_layout):
        """Section de sauvegarde"""
        group = self.create_section_frame("Sauvegarde", "💾")
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(15, 20, 15, 15)
        
        # Options de sauvegarde
        options_layout = QFormLayout()
        options_layout.setSpacing(10)
        
        # Sauvegarde automatique
        self.auto_backup_check = QCheckBox("Activer la sauvegarde automatique")
        self.auto_backup_check.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        options_layout.addRow(self.auto_backup_check)
        
        # Sauvegarde à la fermeture
        self.backup_on_close_check = QCheckBox("Sauvegarder à la fermeture de l'application")
        self.backup_on_close_check.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        options_layout.addRow(self.backup_on_close_check)
        
        # Nombre max de sauvegardes
        max_backup_layout = QHBoxLayout()
        max_backup_label = QLabel("Nombre maximum de sauvegardes:")
        max_backup_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        self.max_backups_spin = QSpinBox()
        self.max_backups_spin.setRange(1, 50)
        self.max_backups_spin.setValue(10)
        self.max_backups_spin.setFixedWidth(80)
        max_backup_layout.addWidget(max_backup_label)
        max_backup_layout.addWidget(self.max_backups_spin)
        max_backup_layout.addStretch()
        options_layout.addRow(max_backup_layout)
        
        # Dossier de sauvegarde
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Dossier de sauvegarde:")
        folder_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        self.backup_path_edit = QLineEdit()
        self.backup_path_edit.setReadOnly(True)
        self.backup_path_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f5f5f5;
            }
        """)
        browse_btn = QPushButton("📁 Parcourir")
        browse_btn.setCursor(Qt.PointingHandCursor)
        browse_btn.clicked.connect(self.browse_backup_folder)
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.backup_path_edit, 1)
        folder_layout.addWidget(browse_btn)
        options_layout.addRow(folder_layout)
        
        layout.addLayout(options_layout)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        backup_now_btn = QPushButton("💾 Sauvegarder maintenant")
        backup_now_btn.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM, QFont.Bold))
        backup_now_btn.setFixedHeight(40)
        backup_now_btn.setCursor(Qt.PointingHandCursor)
        backup_now_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_SUCCESS};
                color: white;
                border-radius: 5px;
                border: none;
                padding: 0 20px;
            }}
            QPushButton:hover {{
                background-color: #058A65;
            }}
        """)
        backup_now_btn.clicked.connect(self.backup_now)
        buttons_layout.addWidget(backup_now_btn)
        
        open_folder_btn = QPushButton("📂 Ouvrir le dossier")
        open_folder_btn.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        open_folder_btn.setFixedHeight(40)
        open_folder_btn.setCursor(Qt.PointingHandCursor)
        open_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border-radius: 5px;
                border: none;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        open_folder_btn.clicked.connect(self.open_backup_folder)
        buttons_layout.addWidget(open_folder_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def create_export_import_section(self, parent_layout):
        """Section Export/Import"""
        group = self.create_section_frame("Export / Import des données", "📤")
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(15, 20, 15, 15)
        
        # Description
        desc = QLabel("Exportez vos données pour les transférer ou les archiver. "
                      "Importez des données depuis un fichier JSON.")
        desc.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666;")
        layout.addWidget(desc)
        
        # Format d'export
        format_layout = QHBoxLayout()
        format_label = QLabel("Format d'export:")
        format_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        self.export_format_combo = QComboBox()
        self.export_format_combo.addItems(["JSON", "CSV", "Excel (.xlsx)"])
        self.export_format_combo.setFixedWidth(150)
        self.export_format_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
        """)
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.export_format_combo)
        format_layout.addStretch()
        layout.addLayout(format_layout)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        export_btn = QPushButton("📤 Exporter les données")
        export_btn.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM, QFont.Bold))
        export_btn.setFixedHeight(40)
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                border-radius: 5px;
                border: none;
                padding: 0 20px;
            }}
            QPushButton:hover {{
                background-color: #1E6A8F;
            }}
        """)
        export_btn.clicked.connect(self.export_data)
        buttons_layout.addWidget(export_btn)
        
        import_btn = QPushButton("📥 Importer des données")
        import_btn.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM, QFont.Bold))
        import_btn.setFixedHeight(40)
        import_btn.setCursor(Qt.PointingHandCursor)
        import_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_SECONDARY};
                color: white;
                border-radius: 5px;
                border: none;
                padding: 0 20px;
            }}
            QPushButton:hover {{
                background-color: #8B2F5E;
            }}
        """)
        import_btn.clicked.connect(self.import_data)
        buttons_layout.addWidget(import_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def create_appearance_section(self, parent_layout):
        """Section Apparence"""
        group = self.create_section_frame("Apparence", "🎨")
        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(15, 20, 15, 15)
        
        # Thème (désactivé pour l'instant)
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Thème:")
        theme_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Clair", "Sombre (bientôt disponible)"])
        self.theme_combo.setFixedWidth(200)
        self.theme_combo.setEnabled(False)  # Désactivé pour l'instant
        self.theme_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f5f5f5;
            }
        """)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        layout.addRow(theme_layout)
        
        # Taille de police
        font_layout = QHBoxLayout()
        font_label = QLabel("Taille des polices:")
        font_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        self.font_scale_combo = QComboBox()
        self.font_scale_combo.addItems(["Petite (-2)", "Normale (0)", "Grande (+2)", "Très grande (+4)"])
        self.font_scale_combo.setCurrentIndex(1)
        self.font_scale_combo.setFixedWidth(200)
        self.font_scale_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
        """)
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_scale_combo)
        font_layout.addStretch()
        layout.addRow(font_layout)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def create_cloture_section(self, parent_layout):
        """Section Clôture automatique"""
        group = self.create_section_frame("Clôture automatique", "⏰")
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(15, 20, 15, 15)
        
        # Heure de clôture
        time_layout = QHBoxLayout()
        time_label = QLabel("Heure de clôture automatique:")
        time_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        self.cloture_time_edit = QTimeEdit()
        self.cloture_time_edit.setTime(QTime(23, 59))
        self.cloture_time_edit.setDisplayFormat("HH:mm")
        self.cloture_time_edit.setFixedWidth(100)
        self.cloture_time_edit.setStyleSheet("""
            QTimeEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
        """)
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.cloture_time_edit)
        time_layout.addStretch()
        layout.addLayout(time_layout)
        
        # Notification avant clôture
        self.notify_cloture_check = QCheckBox("Notifier avant la clôture automatique")
        self.notify_cloture_check.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        layout.addWidget(self.notify_cloture_check)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def create_backups_list_section(self, parent_layout):
        """Section liste des sauvegardes"""
        group = self.create_section_frame("Sauvegardes disponibles", "📋")
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(15, 20, 15, 15)
        
        # Tableau des sauvegardes
        self.backups_table = QTableWidget()
        self.backups_table.setColumnCount(4)
        self.backups_table.setHorizontalHeaderLabels(["Date", "Taille", "Description", "Actions"])
        self.backups_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 5px;
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
            }
        """)
        
        header = self.backups_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.resizeSection(3, 180)
        self.backups_table.verticalHeader().setVisible(False)
        self.backups_table.setMaximumHeight(250)
        
        layout.addWidget(self.backups_table)
        
        # Bouton actualiser
        refresh_btn = QPushButton("🔄 Actualiser la liste")
        refresh_btn.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        refresh_btn.setFixedHeight(35)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border-radius: 5px;
                border: none;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        refresh_btn.clicked.connect(self.load_backups_list)
        layout.addWidget(refresh_btn, 0, Qt.AlignLeft)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
        
        # Charger la liste
        self.load_backups_list()
    
    def load_current_settings(self):
        """Charger les paramètres actuels dans l'interface"""
        self.auto_backup_check.setChecked(self.settings.get('auto_backup', True))
        self.backup_on_close_check.setChecked(self.settings.get('backup_on_close', True))
        self.max_backups_spin.setValue(self.settings.get('max_backups', 10))
        self.backup_path_edit.setText(self.settings.get('backup_path', self.backup_manager.backup_dir))
        self.notify_cloture_check.setChecked(self.settings.get('notify_before_cloture', True))
        
        # Heure de clôture
        cloture_time = self.settings.get('cloture_auto_time', '23:59')
        hour, minute = map(int, cloture_time.split(':'))
        self.cloture_time_edit.setTime(QTime(hour, minute))
        
        # Échelle de police
        font_scale = self.settings.get('font_scale', 0)
        scale_index = {-2: 0, 0: 1, 2: 2, 4: 3}.get(font_scale, 1)
        self.font_scale_combo.setCurrentIndex(scale_index)
    
    def save_settings(self):
        """Sauvegarder les paramètres"""
        # Récupérer l'échelle de police
        font_scale_map = {0: -2, 1: 0, 2: 2, 3: 4}
        font_scale = font_scale_map.get(self.font_scale_combo.currentIndex(), 0)
        
        settings = {
            'auto_backup': self.auto_backup_check.isChecked(),
            'backup_on_close': self.backup_on_close_check.isChecked(),
            'max_backups': self.max_backups_spin.value(),
            'backup_path': self.backup_path_edit.text(),
            'theme': 'light',
            'font_scale': font_scale,
            'cloture_auto_time': self.cloture_time_edit.time().toString("HH:mm"),
            'notify_before_cloture': self.notify_cloture_check.isChecked()
        }
        
        self.backup_manager.save_settings(settings)
        self.settings = settings
        
        QMessageBox.information(
            self,
            "Paramètres enregistrés",
            "Les paramètres ont été enregistrés avec succès.\n"
            "Certaines modifications nécessitent un redémarrage."
        )
    
    def browse_backup_folder(self):
        """Parcourir pour choisir le dossier de sauvegarde"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Choisir le dossier de sauvegarde",
            self.backup_path_edit.text()
        )
        if folder:
            self.backup_path_edit.setText(folder)
    
    def open_backup_folder(self):
        """Ouvrir le dossier de sauvegarde dans l'explorateur"""
        import subprocess
        import sys
        
        path = self.backup_path_edit.text()
        if os.path.exists(path):
            if sys.platform == 'win32':
                os.startfile(path)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', path])
            else:
                subprocess.Popen(['xdg-open', path])
    
    def backup_now(self):
        """Effectuer une sauvegarde immédiate"""
        # Demander une description
        dialog = QDialog(self)
        dialog.setWindowTitle("Description de la sauvegarde")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        label = QLabel("Description (optionnelle):")
        label.setFont(QFont(FONT_FAMILY, FONT_SIZE_SM))
        layout.addWidget(label)
        
        desc_edit = QLineEdit()
        desc_edit.setPlaceholderText("Ex: Sauvegarde avant mise à jour...")
        desc_edit.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        layout.addWidget(desc_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            description = desc_edit.text()
            
            # Créer la sauvegarde
            success, result = self.backup_manager.create_backup(description)
            
            if success:
                QMessageBox.information(
                    self,
                    "Sauvegarde réussie",
                    f"La sauvegarde a été créée avec succès:\n{result}"
                )
                self.load_backups_list()
            else:
                QMessageBox.warning(
                    self,
                    "Erreur",
                    f"Erreur lors de la sauvegarde:\n{result}"
                )
    
    def load_backups_list(self):
        """Charger la liste des sauvegardes"""
        backups = self.backup_manager.list_backups()
        self.backups_table.setRowCount(len(backups))
        
        for row, backup in enumerate(backups):
            # Date
            date_str = backup['timestamp'].strftime("%d/%m/%Y %H:%M")
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignCenter)
            self.backups_table.setItem(row, 0, date_item)
            
            # Taille
            size_mb = backup['size'] / (1024 * 1024)
            size_str = f"{size_mb:.2f} Mo"
            size_item = QTableWidgetItem(size_str)
            size_item.setTextAlignment(Qt.AlignCenter)
            self.backups_table.setItem(row, 1, size_item)
            
            # Description
            desc_item = QTableWidgetItem(backup['description'] or "-")
            self.backups_table.setItem(row, 2, desc_item)
            
            # Boutons d'action
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_layout.setSpacing(5)
            
            restore_btn = QPushButton("♻️")
            restore_btn.setToolTip("Restaurer")
            restore_btn.setFixedSize(35, 30)
            restore_btn.setCursor(Qt.PointingHandCursor)
            restore_btn.setStyleSheet(f"""
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
            restore_btn.clicked.connect(lambda checked, p=backup['path']: self.restore_backup(p))
            actions_layout.addWidget(restore_btn)
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setToolTip("Supprimer")
            delete_btn.setFixedSize(35, 30)
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.setStyleSheet(f"""
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
            delete_btn.clicked.connect(lambda checked, p=backup['path']: self.delete_backup(p))
            actions_layout.addWidget(delete_btn)
            
            actions_layout.addStretch()
            actions_widget.setLayout(actions_layout)
            self.backups_table.setCellWidget(row, 3, actions_widget)
    
    def restore_backup(self, backup_path):
        """Restaurer une sauvegarde"""
        reply = QMessageBox.warning(
            self,
            "Confirmer la restauration",
            "Êtes-vous sûr de vouloir restaurer cette sauvegarde?\n\n"
            "Les données actuelles seront remplacées.\n"
            "Une sauvegarde de sécurité sera créée avant la restauration.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.backup_manager.restore_backup(backup_path)
            
            if success:
                QMessageBox.information(
                    self,
                    "Restauration réussie",
                    "La base de données a été restaurée avec succès.\n"
                    "L'application va se fermer. Veuillez la relancer."
                )
                # Fermer l'application
                if self.parent_window:
                    self.parent_window.close()
            else:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de la restauration:\n{message}")
    
    def delete_backup(self, backup_path):
        """Supprimer une sauvegarde"""
        reply = QMessageBox.question(
            self,
            "Confirmer la suppression",
            "Êtes-vous sûr de vouloir supprimer cette sauvegarde?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.backup_manager.delete_backup(backup_path):
                self.load_backups_list()
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors de la suppression.")
    
    def export_data(self):
        """Exporter les données"""
        format_text = self.export_format_combo.currentText()
        
        # Déterminer l'extension
        if "JSON" in format_text:
            ext = "json"
            filter_str = "JSON Files (*.json)"
        elif "CSV" in format_text:
            ext = "csv"
            filter_str = "CSV Files (*.csv)"
        else:
            ext = "xlsx"
            filter_str = "Excel Files (*.xlsx)"
        
        # Nom par défaut
        default_name = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter les données",
            default_name,
            filter_str
        )
        
        if filepath:
            success, result = self.backup_manager.export_data(filepath, ext)
            
            if success:
                QMessageBox.information(
                    self,
                    "Export réussi",
                    f"Les données ont été exportées avec succès:\n{result}"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Erreur d'export",
                    f"Erreur lors de l'export:\n{result}"
                )
    
    def import_data(self):
        """Importer des données"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Importer des données",
            "",
            "JSON Files (*.json)"
        )
        
        if filepath:
            # Demander le mode d'import
            reply = QMessageBox.question(
                self,
                "Mode d'import",
                "Comment voulez-vous importer les données?\n\n"
                "• Oui = Fusionner (ajouter aux données existantes)\n"
                "• Non = Remplacer (supprimer les données existantes)",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Cancel:
                return
            
            merge = (reply == QMessageBox.Yes)
            
            success, result = self.backup_manager.import_data(filepath, merge)
            
            if success:
                QMessageBox.information(
                    self,
                    "Import réussi",
                    result
                )
                # Actualiser l'affichage
                if self.parent_window:
                    self.parent_window.actualiser_affichage()
                    self.parent_window.actualiser_dashboard()
                    self.parent_window.actualiser_caisse()
            else:
                QMessageBox.warning(
                    self,
                    "Erreur d'import",
                    f"Erreur lors de l'import:\n{result}"
                )
