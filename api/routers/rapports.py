"""
Router pour les rapports journaliers
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from typing import Optional
from datetime import datetime

from api.schemas import (
    RapportsListResponse, RapportDetail, RapportSummary,
    ClotureRequest, ClotureResponse
)
from api.routers.auth import get_current_user
from models.transaction_model import TransactionModel

router = APIRouter()


def get_db():
    """Obtenir une instance de la base de données"""
    return TransactionModel()


@router.get("/", response_model=RapportsListResponse)
async def get_rapports(
    mois: Optional[int] = Query(None, ge=1, le=12),
    annee: Optional[int] = Query(None),
    limit: int = Query(30, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: TransactionModel = Depends(get_db)
):
    """
    Obtenir la liste des rapports journaliers
    
    Filtres:
    - mois: 1-12
    - annee: Année
    - limit: Nombre max de résultats
    """
    try:
        rapports = db.obtenir_tous_rapports()
        
        # Filtrer par mois/année si spécifié
        if mois or annee:
            filtered = []
            for r in rapports:
                date_obj = datetime.strptime(r[0], "%Y-%m-%d")
                if mois and date_obj.month != mois:
                    continue
                if annee and date_obj.year != annee:
                    continue
                filtered.append(r)
            rapports = filtered
        
        # Limiter les résultats
        total = len(rapports)
        rapports = rapports[:limit]
        
        # Formater les résultats
        data = []
        for r in rapports:
            date, recettes, depenses, est_cloture = r
            
            # Calculer le nombre de transactions
            transactions = db.obtenir_transactions_par_date(date)
            nombre_transactions = len(transactions)
            
            # Solde uniquement si clôturé
            solde = recettes - depenses if est_cloture else None
            
            data.append({
                "date": date,
                "recettes": recettes,
                "depenses": depenses,
                "solde": solde,
                "cloture": bool(est_cloture),
                "nombre_transactions": nombre_transactions
            })
        
        return {
            "total": total,
            "data": data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{date}", response_model=RapportDetail)
async def get_rapport_by_date(
    date: str,
    current_user: dict = Depends(get_current_user),
    db: TransactionModel = Depends(get_db)
):
    """
    Obtenir le détail d'un rapport journalier
    
    Inclut toutes les transactions du jour
    """
    try:
        # Valider le format de date
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Format de date invalide (YYYY-MM-DD)")
        
        rapport = db.obtenir_rapport_journalier(date)
        
        if not rapport:
            raise HTTPException(status_code=404, detail=f"Aucun rapport trouvé pour le {date}")
        
        date_r, recettes, depenses, est_cloture = rapport
        
        # Obtenir les transactions
        transactions = db.obtenir_transactions_par_date(date)
        
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
        
        # Solde uniquement si clôturé
        solde = recettes - depenses if est_cloture else None
        
        return {
            "date": date_r,
            "recettes": recettes,
            "depenses": depenses,
            "solde": solde,
            "cloture": bool(est_cloture),
            "transactions": transactions_data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cloturer", response_model=ClotureResponse)
async def cloturer_rapport(
    request: ClotureRequest,
    current_user: dict = Depends(get_current_user),
    db: TransactionModel = Depends(get_db)
):
    """
    Clôturer un rapport journalier
    
    Note: Cette action est irréversible
    """
    try:
        # Vérifier que le rapport existe
        rapport = db.obtenir_rapport_journalier(request.date)
        
        if not rapport:
            raise HTTPException(
                status_code=404,
                detail=f"Aucun rapport trouvé pour le {request.date}"
            )
        
        # Vérifier qu'il n'est pas déjà clôturé
        if rapport[3]:  # est_cloture
            raise HTTPException(
                status_code=400,
                detail=f"Le rapport du {request.date} est déjà clôturé"
            )
        
        # Clôturer
        success = db.cloturer_rapport(request.date)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Erreur lors de la clôture du rapport"
            )
        
        return {
            "date": request.date,
            "cloture": True,
            "heure_cloture": "23:59:00",
            "message": "Rapport clôturé avec succès"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pdf/{date}")
async def get_rapport_pdf(
    date: str,
    current_user: dict = Depends(get_current_user),
    db: TransactionModel = Depends(get_db)
):
    """
    Générer et télécharger le PDF d'un rapport journalier
    
    Note: Cette fonctionnalité nécessite le module rapport_pdf.py
    """
    try:
        # Vérifier que le rapport existe
        rapport = db.obtenir_rapport_journalier(date)
        
        if not rapport:
            raise HTTPException(
                status_code=404,
                detail=f"Aucun rapport trouvé pour le {date}"
            )
        
        # Générer le PDF
        try:
            from rapport_pdf import generer_rapport_pdf
            pdf_path = generer_rapport_pdf(date, db)
            
            # Lire le PDF
            with open(pdf_path, "rb") as f:
                pdf_content = f.read()
            
            # Retourner le PDF
            return Response(
                content=pdf_content,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename=rapport_{date}.pdf"
                }
            )
        
        except ImportError:
            raise HTTPException(
                status_code=501,
                detail="Génération PDF non disponible"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
