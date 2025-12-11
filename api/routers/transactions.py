"""
Router pour les transactions
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from datetime import datetime

from api.schemas import (
    TransactionCreate, TransactionUpdate, TransactionResponse,
    SuccessResponse
)
from api.routers.auth import get_current_user
from models.transaction_model import TransactionModel

router = APIRouter()


def get_db():
    """Obtenir une instance de la base de données"""
    return TransactionModel()


@router.get("/", response_model=dict)
async def get_transactions(
    date: Optional[str] = Query(None, pattern=r'^\d{4}-\d{2}-\d{2}$'),
    type: Optional[str] = Query(None, regex="^(recette|depense|apport)$"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: dict = Depends(get_current_user),
    db: TransactionModel = Depends(get_db)
):
    """
    Obtenir la liste des transactions
    
    Filtres disponibles:
    - date: Format YYYY-MM-DD
    - type: recette, depense, apport
    - limit: Nombre max de résultats (1-100)
    - offset: Pagination
    """
    try:
        if date:
            transactions = db.obtenir_transactions_par_date(date)
        else:
            # Obtenir toutes les transactions récentes
            transactions = db.obtenir_transactions_recentes(limit)
        
        # Filtrer par type si spécifié
        if type:
            transactions = [t for t in transactions if t[1] == type]
        
        # Pagination
        total = len(transactions)
        transactions = transactions[offset:offset + limit]
        
        # Formater les résultats
        data = []
        for t in transactions:
            id_t, type_t, montant, description, date_t, type_depense, created_at = t
            heure = created_at.split()[1][:5] if len(created_at.split()) > 1 else "00:00"
            data.append({
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
            "total": total,
            "limit": limit,
            "offset": offset,
            "data": data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    current_user: dict = Depends(get_current_user),
    db: TransactionModel = Depends(get_db)
):
    """Obtenir une transaction par son ID"""
    try:
        transaction = db.obtenir_transaction_par_id(transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction non trouvée")
        
        id_t, type_t, montant, description, date_t, type_depense, created_at = transaction
        heure = created_at.split()[1][:5] if len(created_at.split()) > 1 else "00:00"
        
        return {
            "id": id_t,
            "type": type_t,
            "montant": montant,
            "description": description,
            "date": date_t,
            "heure": heure,
            "type_depense": type_depense,
            "created_at": created_at
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=201)
async def create_transaction(
    transaction: TransactionCreate,
    current_user: dict = Depends(get_current_user),
    db: TransactionModel = Depends(get_db)
):
    """
    Créer une nouvelle transaction
    
    Types possibles:
    - recette: Revenus
    - depense: Dépenses (normale ou spéciale)
    - apport: Apport en capital
    """
    try:
        success, result = db.ajouter_transaction(
            transaction.type,
            transaction.montant,
            transaction.description,
            transaction.type_depense,
            transaction.date
        )
        
        if not success:
            raise HTTPException(status_code=400, detail=result)
        
        # Retourner la transaction créée avec son ID
        return {
            "id": result,
            "type": transaction.type,
            "montant": transaction.montant,
            "description": transaction.description,
            "date": transaction.date,
            "heure": datetime.now().strftime("%H:%M"),
            "type_depense": transaction.type_depense,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": "Transaction ajoutée avec succès"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{transaction_id}")
async def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    current_user: dict = Depends(get_current_user),
    db: TransactionModel = Depends(get_db)
):
    """
    Modifier une transaction
    
    Note: Impossible de modifier une transaction d'un rapport clôturé
    """
    try:
        # Vérifier que la transaction existe
        existing = db.obtenir_transaction_par_id(transaction_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Transaction non trouvée")
        
        # Vérifier que le rapport n'est pas clôturé
        date_transaction = existing[4]
        rapport = db.obtenir_rapport_journalier(date_transaction)
        if rapport and rapport[3]:  # Si clôturé
            raise HTTPException(
                status_code=403,
                detail="Impossible de modifier une transaction d'un rapport clôturé"
            )
        
        # Mettre à jour uniquement les champs fournis
        update_data = {}
        if transaction.montant is not None:
            update_data['montant'] = transaction.montant
        if transaction.description is not None:
            update_data['description'] = transaction.description
        
        if not update_data:
            raise HTTPException(status_code=400, detail="Aucune donnée à modifier")
        
        success = db.modifier_transaction(transaction_id, **update_data)
        
        if not success:
            raise HTTPException(status_code=500, detail="Erreur lors de la modification")
        
        return {
            "id": transaction_id,
            "message": "Transaction modifiée avec succès"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    current_user: dict = Depends(get_current_user),
    db: TransactionModel = Depends(get_db)
):
    """
    Supprimer une transaction
    
    Note: Impossible de supprimer une transaction d'un rapport clôturé
    """
    try:
        # Vérifier que la transaction existe
        existing = db.obtenir_transaction_par_id(transaction_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Transaction non trouvée")
        
        # Vérifier que le rapport n'est pas clôturé
        date_transaction = existing[4]
        rapport = db.obtenir_rapport_journalier(date_transaction)
        if rapport and rapport[3]:  # Si clôturé
            raise HTTPException(
                status_code=403,
                detail="Impossible de supprimer une transaction d'un rapport clôturé"
            )
        
        success = db.supprimer_transaction(transaction_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="Erreur lors de la suppression")
        
        return {"message": "Transaction supprimée avec succès"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
