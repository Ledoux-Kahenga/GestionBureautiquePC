"""
Router pour la gestion de la caisse
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from datetime import datetime, timedelta

from api.schemas import (
    CaisseResponse, CompositionCaisseResponse, 
    HistoriqueCaisseResponse, HistoriqueCaisseItem
)
from api.routers.auth import get_current_user
from models.transaction_model import TransactionModel

router = APIRouter()


def get_db():
    """Obtenir une instance de la base de données"""
    return TransactionModel()


@router.get("/montant", response_model=CaisseResponse)
async def get_montant_caisse(
    current_user: dict = Depends(get_current_user),
    db: TransactionModel = Depends(get_db)
):
    """
    Obtenir le montant total en caisse
    
    Calcul: Soldes clôturés + Apports - Dépenses spéciales
    """
    try:
        caisse_data = db.calculer_caisse()
        
        return {
            "montant": caisse_data['caisse'],
            "devise": "FC",
            "derniere_mise_a_jour": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/composition", response_model=CompositionCaisseResponse)
async def get_composition_caisse(
    periode: str = Query("ce_mois", regex="^(aujourd_hui|cette_semaine|ce_mois|toutes)$"),
    mois: Optional[int] = Query(None, ge=1, le=12),
    current_user: dict = Depends(get_current_user),
    db: TransactionModel = Depends(get_db)
):
    """
    Obtenir la composition de la caisse
    
    Filtres:
    - periode: aujourd_hui, cette_semaine, ce_mois, toutes
    - mois: 1-12 (pour période mois_specifique)
    
    Retourne:
    - Soldes clôturés
    - Apports
    - Dépenses spéciales
    - Total
    """
    try:
        today = datetime.now().date()
        date_debut = None
        date_fin = None
        
        # Définir les dates selon la période
        if periode == "aujourd_hui":
            date_debut = today
            date_fin = today
        elif periode == "cette_semaine":
            date_debut = today - timedelta(days=today.weekday())
            date_fin = today
        elif periode == "ce_mois":
            date_debut = today.replace(day=1)
            date_fin = today
        elif mois:
            # Mois spécifique
            year = today.year
            date_debut = datetime(year, mois, 1).date()
            if mois == 12:
                date_fin = datetime(year, 12, 31).date()
            else:
                date_fin = (datetime(year, mois + 1, 1) - timedelta(days=1)).date()
        
        # Calculer la composition
        if date_debut and date_fin:
            date_debut_str = date_debut.strftime("%Y-%m-%d")
            date_fin_str = date_fin.strftime("%Y-%m-%d")
            caisse_data = db.calculer_caisse(date_debut_str, date_fin_str)
        else:
            caisse_data = db.calculer_caisse()
        
        return {
            "periode": periode,
            "solde_cloture": caisse_data['solde_cloture'],
            "apports": caisse_data['apports'],
            "depenses_speciales": caisse_data['depenses_speciales'],
            "total": caisse_data['caisse']
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/historique", response_model=HistoriqueCaisseResponse)
async def get_historique_caisse(
    type: Optional[str] = Query(None, regex="^(apport|depense)$"),
    date_debut: Optional[str] = Query(None, pattern=r'^\d{4}-\d{2}-\d{2}$'),
    date_fin: Optional[str] = Query(None, pattern=r'^\d{4}-\d{2}-\d{2}$'),
    limit: int = Query(50, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: TransactionModel = Depends(get_db)
):
    """
    Obtenir l'historique des mouvements de caisse
    
    Filtres:
    - type: apport ou depense
    - date_debut, date_fin: Période (format YYYY-MM-DD)
    - limit: Nombre max de résultats
    """
    try:
        # Obtenir les apports et dépenses spéciales
        apports = db.obtenir_apports()
        depenses = db.obtenir_depenses_speciales()
        
        # Combiner et marquer le type
        mouvements = []
        
        if not type or type == "apport":
            for app in apports:
                id_app, montant, description, date, created_at = app
                mouvements.append({
                    "id": id_app,
                    "type": "apport",
                    "montant": montant,
                    "description": description,
                    "date": date,
                    "created_at": created_at
                })
        
        if not type or type == "depense":
            for dep in depenses:
                id_dep, montant, description, date, created_at = dep
                mouvements.append({
                    "id": id_dep,
                    "type": "depense",
                    "montant": montant,
                    "description": description,
                    "date": date,
                    "created_at": created_at
                })
        
        # Filtrer par période si spécifié
        if date_debut and date_fin:
            mouvements = [
                m for m in mouvements 
                if date_debut <= m['date'] <= date_fin
            ]
        
        # Trier par date décroissante
        mouvements.sort(key=lambda x: (x['date'], x['created_at']), reverse=True)
        
        total = len(mouvements)
        mouvements = mouvements[:limit]
        
        # Formater les résultats
        data = []
        for m in mouvements:
            heure = m['created_at'].split()[1][:5] if len(m['created_at'].split()) > 1 else "00:00"
            data.append({
                "id": m['id'],
                "type": m['type'],
                "montant": m['montant'],
                "description": m['description'],
                "date": m['date'],
                "heure": heure
            })
        
        return {
            "total": total,
            "data": data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
