"""
Modèles Pydantic pour la validation des données
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime, date


# Modèles de base
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


class UserLogin(BaseModel):
    username: str
    password: str


# Modèles Transaction
class TransactionBase(BaseModel):
    type: Literal["recette", "depense", "apport"]
    montant: float = Field(gt=0, description="Montant doit être positif")
    description: str = Field(min_length=3, description="Description obligatoire")
    date: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$', description="Format: YYYY-MM-DD")
    type_depense: Literal["normale", "speciale"] = "normale"
    
    @validator('date')
    def validate_date_not_future(cls, v):
        """Vérifier que la date n'est pas dans le futur"""
        date_obj = datetime.strptime(v, "%Y-%m-%d").date()
        if date_obj > datetime.now().date():
            raise ValueError("La date ne peut pas être dans le futur")
        return v


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    montant: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, min_length=3)


class TransactionResponse(TransactionBase):
    id: int
    heure: str
    created_at: str
    
    class Config:
        from_attributes = True


# Modèles Caisse
class CaisseResponse(BaseModel):
    montant: float
    devise: str = "FC"
    derniere_mise_a_jour: str


class CompositionCaisseResponse(BaseModel):
    periode: str
    solde_cloture: float
    apports: float
    depenses_speciales: float
    total: float


class HistoriqueCaisseItem(BaseModel):
    id: int
    type: str
    montant: float
    description: str
    date: str
    heure: str


class HistoriqueCaisseResponse(BaseModel):
    total: int
    data: list[HistoriqueCaisseItem]


# Modèles Rapport
class RapportSummary(BaseModel):
    date: str
    recettes: float
    depenses: float
    solde: Optional[float]
    cloture: bool
    nombre_transactions: int


class RapportDetail(BaseModel):
    date: str
    recettes: float
    depenses: float
    solde: Optional[float]
    cloture: bool
    transactions: list[TransactionResponse]


class RapportsListResponse(BaseModel):
    total: int
    data: list[RapportSummary]


class ClotureRequest(BaseModel):
    date: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$')


class ClotureResponse(BaseModel):
    date: str
    cloture: bool
    heure_cloture: str
    message: str


# Modèles Statistiques
class CaisseStats(BaseModel):
    montant: float
    variation_24h: float
    pourcentage_variation: float


class RapportJourStats(BaseModel):
    date: str
    recettes: float
    depenses: float
    solde: float
    cloture: bool


class DashboardResponse(BaseModel):
    caisse: CaisseStats
    rapport_jour: RapportJourStats
    derniere_transactions: list[TransactionResponse]


class PeriodeStats(BaseModel):
    debut: str
    fin: str


class StatsPeriodesResponse(BaseModel):
    periode: PeriodeStats
    total_recettes: float
    total_depenses: float
    solde_net: float
    nombre_transactions: int
    moyenne_quotidienne: float


# Modèles de réponse génériques
class SuccessResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str


class PaginatedResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: list
