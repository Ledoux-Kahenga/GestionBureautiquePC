"""
Gestion de la base de données SQLite
"""
import sqlite3
from datetime import datetime
from config import DATABASE_PATH


class Database:
    """Classe pour gérer les opérations de base de données"""
    
    def __init__(self):
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Établir la connexion à la base de données"""
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()
        
    def disconnect(self):
        """Fermer la connexion à la base de données"""
        if self.conn:
            self.conn.close()
            
    def create_tables(self):
        """Créer les tables nécessaires"""
        self.connect()
        
        # Table des transactions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                montant REAL NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                created_at TEXT NOT NULL,
                type_depense TEXT DEFAULT 'normale'
            )
        ''')
        
        # Vérifier si la colonne type_depense existe, sinon l'ajouter
        self.cursor.execute("PRAGMA table_info(transactions)")
        columns = [column[1] for column in self.cursor.fetchall()]
        
        if 'type_depense' not in columns:
            self.cursor.execute('''
                ALTER TABLE transactions ADD COLUMN type_depense TEXT DEFAULT 'normale'
            ''')
        
        # Table des rapports journaliers
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rapports_journaliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL UNIQUE,
                cloture INTEGER DEFAULT 0,
                cloture_at TEXT
            )
        ''')
        
        self.conn.commit()
        self.disconnect()
        
    def ajouter_transaction(self, type_transaction, montant, description="", type_depense="normale"):
        """Ajouter une nouvelle transaction"""
        self.connect()
        date_actuelle = datetime.now().strftime("%Y-%m-%d")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.cursor.execute('''
            INSERT INTO transactions (type, montant, description, date, created_at, type_depense)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (type_transaction, montant, description, date_actuelle, created_at, type_depense))
        
        self.conn.commit()
        transaction_id = self.cursor.lastrowid
        self.disconnect()
        return transaction_id
        
    def obtenir_transactions(self, date=None):
        """Obtenir les transactions (toutes ou pour une date spécifique) - uniquement les transactions normales (journalières)"""
        self.connect()
        
        if date:
            self.cursor.execute('''
                SELECT id, type, montant, description, date, created_at
                FROM transactions
                WHERE date = ? AND type_depense = 'normale'
                ORDER BY created_at DESC
            ''', (date,))
        else:
            self.cursor.execute('''
                SELECT id, type, montant, description, date, created_at
                FROM transactions
                WHERE type_depense = 'normale'
                ORDER BY created_at DESC
            ''')
        
        transactions = self.cursor.fetchall()
        self.disconnect()
        return transactions
        
    def calculer_solde(self, date=None):
        """Calculer le solde disponible - uniquement les transactions journalières normales"""
        self.connect()
        
        if date:
            # Solde pour une date spécifique
            self.cursor.execute('''
                SELECT 
                    SUM(CASE WHEN type = 'recette' AND type_depense = 'normale' THEN montant ELSE 0 END) as total_recettes,
                    SUM(CASE WHEN type = 'depense' AND type_depense = 'normale' THEN montant ELSE 0 END) as total_depenses
                FROM transactions
                WHERE date = ?
            ''', (date,))
        else:
            # Solde global
            self.cursor.execute('''
                SELECT 
                    SUM(CASE WHEN type = 'recette' AND type_depense = 'normale' THEN montant ELSE 0 END) as total_recettes,
                    SUM(CASE WHEN type = 'depense' AND type_depense = 'normale' THEN montant ELSE 0 END) as total_depenses
                FROM transactions
            ''')
        
        result = self.cursor.fetchone()
        self.disconnect()
        
        recettes = result[0] if result[0] else 0
        depenses = result[1] if result[1] else 0
        solde = recettes - depenses
        
        return {
            'recettes': recettes,
            'depenses': depenses,
            'solde': solde
        }
        
    def supprimer_transaction(self, transaction_id):
        """Supprimer une transaction"""
        self.connect()
        self.cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        self.conn.commit()
        self.disconnect()
        
    def obtenir_transaction(self, transaction_id):
        """Obtenir une transaction spécifique par ID"""
        self.connect()
        
        self.cursor.execute('''
            SELECT id, type, montant, description, date, created_at, type_depense
            FROM transactions
            WHERE id = ?
        ''', (transaction_id,))
        
        transaction = self.cursor.fetchone()
        self.disconnect()
        return transaction
        
    def modifier_transaction(self, transaction_id, type_transaction, montant, description, type_depense="normale"):
        """Modifier une transaction existante"""
        self.connect()
        
        self.cursor.execute('''
            UPDATE transactions
            SET type = ?, montant = ?, description = ?, type_depense = ?
            WHERE id = ?
        ''', (type_transaction, montant, description, type_depense, transaction_id))
        
        self.conn.commit()
        self.disconnect()
        
    def obtenir_statistiques_par_jour(self, date_debut=None, date_fin=None):
        """Obtenir les statistiques groupées par jour - uniquement transactions journalières normales"""
        self.connect()
        
        if date_debut and date_fin:
            self.cursor.execute('''
                SELECT 
                    date,
                    SUM(CASE WHEN type = 'recette' AND type_depense = 'normale' THEN montant ELSE 0 END) as recettes,
                    SUM(CASE WHEN type = 'depense' AND type_depense = 'normale' THEN montant ELSE 0 END) as depenses
                FROM transactions
                WHERE date BETWEEN ? AND ?
                GROUP BY date
                ORDER BY date DESC
            ''', (date_debut, date_fin))
        else:
            self.cursor.execute('''
                SELECT 
                    date,
                    SUM(CASE WHEN type = 'recette' AND type_depense = 'normale' THEN montant ELSE 0 END) as recettes,
                    SUM(CASE WHEN type = 'depense' AND type_depense = 'normale' THEN montant ELSE 0 END) as depenses
                FROM transactions
                GROUP BY date
                ORDER BY date DESC
            ''')
        
        results = self.cursor.fetchall()
        self.disconnect()
        return results
    
    def obtenir_statistiques_detaillees_par_jour(self, date_debut=None, date_fin=None):
        """Obtenir les statistiques détaillées avec séparation des dépenses normales et spéciales"""
        self.connect()
        
        if date_debut and date_fin:
            self.cursor.execute('''
                SELECT 
                    date,
                    SUM(CASE WHEN type = 'recette' THEN montant ELSE 0 END) as recettes,
                    SUM(CASE WHEN type = 'depense' AND type_depense = 'normale' THEN montant ELSE 0 END) as depenses_normales,
                    SUM(CASE WHEN type = 'depense' AND type_depense = 'speciale' THEN montant ELSE 0 END) as depenses_speciales
                FROM transactions
                WHERE date BETWEEN ? AND ?
                GROUP BY date
                ORDER BY date DESC
            ''', (date_debut, date_fin))
        else:
            self.cursor.execute('''
                SELECT 
                    date,
                    SUM(CASE WHEN type = 'recette' THEN montant ELSE 0 END) as recettes,
                    SUM(CASE WHEN type = 'depense' AND type_depense = 'normale' THEN montant ELSE 0 END) as depenses_normales,
                    SUM(CASE WHEN type = 'depense' AND type_depense = 'speciale' THEN montant ELSE 0 END) as depenses_speciales
                FROM transactions
                GROUP BY date
                ORDER BY date DESC
            ''')
        
        results = self.cursor.fetchall()
        self.disconnect()
        return results
        
    def calculer_caisse(self, date_debut=None, date_fin=None):
        """Calculer le montant en caisse (soldes journaliers clôturés + apports - dépenses spéciales)
        Si date_debut et date_fin sont fournis, calcule pour cette période uniquement"""
        self.connect()
        
        # Obtenir la somme des soldes des rapports clôturés
        if date_debut and date_fin:
            self.cursor.execute('''
                SELECT 
                    SUM(CASE WHEN t.type = 'recette' THEN t.montant ELSE -t.montant END) as solde_cloture
                FROM transactions t
                INNER JOIN rapports_journaliers r ON t.date = r.date
                WHERE r.cloture = 1 AND t.type_depense = 'normale'
                  AND t.date BETWEEN ? AND ?
            ''', (date_debut, date_fin))
        else:
            self.cursor.execute('''
                SELECT 
                    SUM(CASE WHEN t.type = 'recette' THEN t.montant ELSE -t.montant END) as solde_cloture
                FROM transactions t
                INNER JOIN rapports_journaliers r ON t.date = r.date
                WHERE r.cloture = 1 AND t.type_depense = 'normale'
            ''')
        
        result_cloture = self.cursor.fetchone()
        solde_cloture = result_cloture[0] if result_cloture[0] else 0
        
        # Obtenir la somme des dépenses spéciales (qui sortent de la caisse)
        if date_debut and date_fin:
            self.cursor.execute('''
                SELECT SUM(montant) as depenses_speciales
                FROM transactions
                WHERE type = 'depense' AND type_depense = 'speciale'
                  AND date BETWEEN ? AND ?
            ''', (date_debut, date_fin))
        else:
            self.cursor.execute('''
                SELECT SUM(montant) as depenses_speciales
                FROM transactions
                WHERE type = 'depense' AND type_depense = 'speciale'
            ''')
        
        result_speciales = self.cursor.fetchone()
        depenses_speciales = result_speciales[0] if result_speciales[0] else 0
        
        # Obtenir la somme des apports en caisse
        if date_debut and date_fin:
            self.cursor.execute('''
                SELECT SUM(montant) as apports
                FROM transactions
                WHERE type = 'apport' AND type_depense = 'speciale'
                  AND date BETWEEN ? AND ?
            ''', (date_debut, date_fin))
        else:
            self.cursor.execute('''
                SELECT SUM(montant) as apports
                FROM transactions
                WHERE type = 'apport' AND type_depense = 'speciale'
            ''')
        
        result_apports = self.cursor.fetchone()
        apports = result_apports[0] if result_apports[0] else 0
        
        self.disconnect()
        
        return {
            'solde_cloture': solde_cloture,
            'depenses_speciales': depenses_speciales,
            'apports': apports,
            'caisse': solde_cloture + apports - depenses_speciales
        }
        
    def obtenir_depenses_speciales(self, date_debut=None, date_fin=None):
        """Obtenir toutes les dépenses spéciales avec filtre optionnel par date"""
        self.connect()
        
        if date_debut and date_fin:
            self.cursor.execute('''
                SELECT id, montant, description, date, created_at
                FROM transactions
                WHERE type = 'depense' AND type_depense = 'speciale'
                  AND date BETWEEN ? AND ?
                ORDER BY created_at DESC
            ''', (date_debut, date_fin))
        else:
            self.cursor.execute('''
                SELECT id, montant, description, date, created_at
                FROM transactions
                WHERE type = 'depense' AND type_depense = 'speciale'
                ORDER BY created_at DESC
            ''')
        
        results = self.cursor.fetchall()
        self.disconnect()
        return results
    
    def obtenir_apports(self, date_debut=None, date_fin=None):
        """Obtenir tous les apports en capital avec filtre optionnel par date"""
        self.connect()
        
        if date_debut and date_fin:
            self.cursor.execute('''
                SELECT id, montant, description, date, created_at
                FROM transactions
                WHERE type = 'apport' AND type_depense = 'speciale'
                  AND date BETWEEN ? AND ?
                ORDER BY created_at DESC
            ''', (date_debut, date_fin))
        else:
            self.cursor.execute('''
                SELECT id, montant, description, date, created_at
                FROM transactions
                WHERE type = 'apport' AND type_depense = 'speciale'
                ORDER BY created_at DESC
            ''')
        
        results = self.cursor.fetchall()
        self.disconnect()
        return results
        
    def cloturer_rapport(self, date):
        """Clôturer le rapport d'une date donnée"""
        self.connect()
        cloture_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.cursor.execute('''
            INSERT OR REPLACE INTO rapports_journaliers (date, cloture, cloture_at)
            VALUES (?, 1, ?)
        ''', (date, cloture_at))
        
        self.conn.commit()
        self.disconnect()
        
    def rouvrir_rapport(self, date):
        """Rouvrir un rapport clôturé"""
        self.connect()
        
        self.cursor.execute('''
            UPDATE rapports_journaliers
            SET cloture = 0, cloture_at = NULL
            WHERE date = ?
        ''', (date,))
        
        self.conn.commit()
        self.disconnect()
        
    def verifier_cloture(self, date):
        """Vérifier si un rapport est clôturé"""
        self.connect()
        
        self.cursor.execute('''
            SELECT cloture FROM rapports_journaliers WHERE date = ?
        ''', (date,))
        
        result = self.cursor.fetchone()
        self.disconnect()
        
        return result[0] == 1 if result else False
        
    def obtenir_rapports_clotures(self):
        """Obtenir tous les rapports clôturés"""
        self.connect()
        
        self.cursor.execute('''
            SELECT date, cloture_at FROM rapports_journaliers WHERE cloture = 1
            ORDER BY date DESC
        ''')
        
        results = self.cursor.fetchall()
        self.disconnect()
        return results
    
    def obtenir_rapports_non_clotures(self):
        """Obtenir tous les rapports non clôturés"""
        self.connect()
        
        self.cursor.execute('''
            SELECT DISTINCT t.date
            FROM transactions t
            LEFT JOIN rapports_journaliers r ON t.date = r.date
            WHERE r.cloture IS NULL OR r.cloture = 0
            ORDER BY t.date DESC
        ''')
        
        results = self.cursor.fetchall()
        self.disconnect()
        return results
