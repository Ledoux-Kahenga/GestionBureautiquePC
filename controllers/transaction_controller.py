"""
Contrôleur pour gérer la logique métier des transactions
"""
from datetime import datetime, timedelta
from models.transaction_model import TransactionModel


class TransactionController:
    """Contrôleur pour gérer les opérations sur les transactions"""
    
    def __init__(self):
        self.model = TransactionModel()
        self.jour_courant = datetime.now().strftime("%Y-%m-%d")
    
    def ajouter_transaction(self, type_transaction, montant, description="", type_depense="normale"):
        """Ajouter une nouvelle transaction"""
        try:
            montant_float = float(montant)
            if montant_float <= 0:
                return False, "Le montant doit être supérieur à 0"
            
            transaction_id = self.model.ajouter_transaction(
                type_transaction, montant_float, description, type_depense
            )
            return True, transaction_id
        except ValueError:
            return False, "Montant invalide"
        except Exception as e:
            return False, str(e)
    
    def modifier_transaction(self, transaction_id, type_transaction, montant, description, type_depense="normale"):
        """Modifier une transaction existante"""
        try:
            montant_float = float(montant)
            if montant_float <= 0:
                return False, "Le montant doit être supérieur à 0"
            
            self.model.modifier_transaction(
                transaction_id, type_transaction, montant_float, description, type_depense
            )
            return True, "Transaction modifiée avec succès"
        except ValueError:
            return False, "Montant invalide"
        except Exception as e:
            return False, str(e)
    
    def supprimer_transaction(self, transaction_id):
        """Supprimer une transaction"""
        try:
            self.model.supprimer_transaction(transaction_id)
            return True, "Transaction supprimée avec succès"
        except Exception as e:
            return False, str(e)
    
    def obtenir_transactions(self, date=None):
        """Obtenir les transactions"""
        return self.model.obtenir_transactions(date)
    
    def obtenir_transaction(self, transaction_id):
        """Obtenir une transaction spécifique"""
        return self.model.obtenir_transaction(transaction_id)
    
    def calculer_solde(self, date=None):
        """Calculer le solde"""
        return self.model.calculer_solde(date)
    
    def obtenir_statistiques_par_jour(self, date_debut=None, date_fin=None):
        """Obtenir les statistiques par jour"""
        return self.model.obtenir_statistiques_par_jour(date_debut, date_fin)
    
    def obtenir_statistiques_detaillees_par_jour(self, date_debut=None, date_fin=None):
        """Obtenir les statistiques détaillées par jour"""
        return self.model.obtenir_statistiques_detaillees_par_jour(date_debut, date_fin)
    
    def calculer_caisse(self, date_debut=None, date_fin=None):
        """Calculer le montant en caisse"""
        return self.model.calculer_caisse(date_debut, date_fin)
    
    def obtenir_depenses_speciales(self, date_debut=None, date_fin=None):
        """Obtenir les dépenses spéciales"""
        return self.model.obtenir_depenses_speciales(date_debut, date_fin)
    
    def obtenir_apports(self, date_debut=None, date_fin=None):
        """Obtenir les apports en capital"""
        return self.model.obtenir_apports(date_debut, date_fin)
    
    def cloturer_rapport(self, date):
        """Clôturer un rapport journalier"""
        try:
            # Vérifier s'il y a des recettes
            stats = self.model.calculer_solde(date)
            if stats['recettes'] <= 0:
                return False, "Impossible de clôturer : aucune recette pour cette date"
            
            # Vérifier si déjà clôturé
            if self.model.verifier_cloture(date):
                return False, "Ce rapport est déjà clôturé"
            
            self.model.cloturer_rapport(date)
            return True, "Rapport clôturé avec succès"
        except Exception as e:
            return False, str(e)
    
    def rouvrir_rapport(self, date):
        """Rouvrir un rapport clôturé"""
        try:
            if not self.model.verifier_cloture(date):
                return False, "Ce rapport n'est pas clôturé"
            
            self.model.rouvrir_rapport(date)
            return True, "Rapport rouvert avec succès"
        except Exception as e:
            return False, str(e)
    
    def verifier_cloture(self, date):
        """Vérifier si un rapport est clôturé"""
        return self.model.verifier_cloture(date)
    
    def obtenir_rapports_clotures(self):
        """Obtenir tous les rapports clôturés"""
        return self.model.obtenir_rapports_clotures()
    
    def obtenir_rapports_non_clotures(self):
        """Obtenir tous les rapports non clôturés"""
        return self.model.obtenir_rapports_non_clotures()
    
    def verifier_nouveau_jour(self):
        """Vérifier si c'est un nouveau jour et effectuer les actions nécessaires"""
        date_actuelle = datetime.now().strftime("%Y-%m-%d")
        
        if date_actuelle != self.jour_courant:
            # Clôturer automatiquement la journée précédente si nécessaire
            date_hier = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            
            if not self.model.verifier_cloture(date_hier):
                stats = self.model.calculer_solde(date_hier)
                
                if stats['recettes'] > 0:
                    self.model.cloturer_rapport(date_hier)
                    self.jour_courant = date_actuelle
                    return True, f"Rapport du {date_hier} clôturé automatiquement"
            
            self.jour_courant = date_actuelle
            return True, "Nouveau jour détecté"
        
        return False, "Même jour"
    
    def verifier_heure_cloture_auto(self):
        """Vérifier si c'est l'heure de clôturer automatiquement"""
        from PyQt5.QtCore import QTime
        
        heure_actuelle = QTime.currentTime()
        date_actuelle = datetime.now().strftime("%Y-%m-%d")
        
        # Clôture automatique à 23h53
        if heure_actuelle.hour() == 23 and heure_actuelle.minute() == 53:
            if not self.model.verifier_cloture(date_actuelle):
                stats = self.model.calculer_solde(date_actuelle)
                
                if stats['recettes'] > 0:
                    self.model.cloturer_rapport(date_actuelle)
                    return True, f"Rapport du {date_actuelle} clôturé automatiquement"
        
        return False, "Pas l'heure de clôture"
    
    def obtenir_tous_rapports(self):
        """Obtenir la liste de tous les rapports journaliers"""
        return self.model.obtenir_tous_rapports()
    
    def obtenir_transactions_par_date(self, date):
        """Obtenir toutes les transactions d'une date spécifique"""
        return self.model.obtenir_transactions_par_date(date)
