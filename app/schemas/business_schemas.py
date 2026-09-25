from pydantic import BaseModel
from enum import Enum

class Regime(Enum):
    FORFETTARIO = "forfettario"
    
class Level(Enum):
    section = "Sezione"
    division = "Divisione"
    group = "Gruppo"
    class_ = "Classe"
    category = "Categoria"
    subcategory = "Sottocategoria"
    all = "Tutti"

class BusinessActivity(BaseModel):
    code: str
    description: str
    level: Level

    class Config:
        orm_mode = True

class UserTaxProfile(BaseModel):
    id: int
    user_id: int
    regime_fiscale: Regime
    coefficiente_redditivita: float
    aliquota_imposta: float
    tipo_inps: str
    aliquota_inps: float
    contibuto_fisso_inps: float
    anno_inizio_attivita: int

    class Config:
        orm_mode = True