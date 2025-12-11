"""
Router pour les statistiques et dashboard
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta

from api.schemas import DashboardResponse, StatsPeriodesResponse
from api.routers.auth import get_current_user
from models.transaction_model import TransactionModel

router = APIRouter()


def get_db():
    """Obtenir une instance de la base de données"""
    return TransactionModel()


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard_stats(
    current_user: dict = Depends(get_current_user),
    db: TransactionModel = Depends(get_db)
):
    """
    Obtenir les statistiques du dashboard
    
    Retourne:
    - État de la caisse avec variation 24h
    - Rapport du jour
    - Dernières transactions
    """
    try:
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        # Calcul caisse actuelle
        caisse_data = db.calculer_caisse()
        caisse_actuelle = caisse_data['caisse']
        
        # Calcul caisse hier
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        caisse_hier_data = db.calculer_caisse(None, yesterday_str)
        caisse_hier = caisse_hier_data['caisse']
        
        # Variation
        variation_24h = caisse_actuelle - caisse_hier
        pourcentage_variation = (variation_24h / caisse_hier * 100) if caisse_hier != 0 else 0
        
        # Rapport du jour
        today_str = today.strftime("%Y-%m-%d")
        rapport = db.obtenir_rapport_journalier(today_str)
        
        if rapport:
            date_r, recettes, depenses, est_cloture = rapport
            solde = recettes - depenses
        else:
            recettes = 0
            depenses = 0
            solde = 0
            est_cloture = False
        
        # Dernières transactions
        transactions = db.obtenir_transactions_recentes(10)
        
        transactions_data = []
        for t in transactions:
            id_t, type_t, montant, description, date_t, type_depense, created_at = t
            heure = created_at.split()[1][:5] if len(created_at.split()) > 1 else "00:00"
            transactions_data.append({
                "id": id_t,
                "type": type_t,
                "montant": montant,
                "description": description,
                "date": date_t,
                "heure": heure,
                "type_depense": type_depense,
                "created_at": created_at
            })
        
        return {
            "caisse": {
                "montant": caisse_actuelle,
                "variation_24h": variation_24h,
                "pourcentage_variation": round(pourcentage_variation, 2)
            },
            "rapport_jour": {
                "date": today_str,
                "recettes": recettes,
                "depenses": depenses,
                "solde": solde,
                "cloture": bool(est_cloture)
            },
            "derniere_transactions": transactions_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/periode", response_model=StatsPeriodesResponse)
async def get_stats_periode(
    date_debut: str = Query(..., pattern=r'^\d{4}-\d{2}-\d{2}$'),
    date_fin: str = Query(..., pattern=r'^\d{4}-\d{2}-\d{2}$'),
    current_user: dict = Depends(get_current_user),
    db: TransactionModel = Depends(get_db)
):
    """
    Obtenir les statistiques sur une période
    
    Paramètres:
    - date_debut: Format YYYY-MM-DD
    - date_fin: Format YYYY-MM-DD
    
    Retourne:
    - Total recettes
    - Total dépenses
    - Solde net
    - Nombre de transactions
    - Moyenne quotidienne
    """
    try:
        # Valider les dates
        try:
            debut = datetime.strptime(date_debut, "%Y-%m-%d").date()
            fin = datetime.strptime(date_fin, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Format de date invalide")
        
        if debut > fin:
            raise HTTPException(
                status_code=400,
                detail="La date de début doit être antérieure à la date de fin"
            )
        
        # Obtenir toutes les transactions de la période
        total_recettes = 0
        total_depenses = 0
        nombre_transactions = 0
        
        current = debut
        while current <= fin:
            current_str = current.strftime("%Y-%m-%d")
            rapport = db.obtenir_rapport_journalier(current_str)
            
            if rapport:
                date_r, recettes, depenses, est_cloture = rapport
                total_recettes += recettes
                total_depenses += depenses
                
                # Compter les transactions
                transactions = db.obtenir_transactions_par_date(current_str)
                nombre_transactions += len(transactions)
            
            current += timedelta(days=1)
        
        # Calculer les statistiques
        solde_net = total_recettes - total_depenses
        nombre_jours = (fin - debut).days + 1
        moyenne_quotidienne = solde_net / nombre_jours if nombre_jours > 0 else 0
        
        return {
            "periode": {
                "debut": date_debut,
                "fin": date_fin
            },
            "total_recettes": total_recettes,
            "total_depenses": total_depenses,
            "solde_net": solde_net,
            "nombre_transactions": nombre_transactions,
            "moyenne_quotidienne": round(moyenne_quotidienne, 2)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
