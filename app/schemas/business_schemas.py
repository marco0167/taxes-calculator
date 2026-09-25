from pydantic import BaseModel
from enum import Enum

class Regime(Enum):
    FORFETTARIO = 1
    ORDINARIO = 2
    
class Level(Enum):
    SEZIONE = "Sezione"
    DIVISIONE = "Divisione"
    GRUPPO = "Gruppo"
    CLASSE = "Classe"
    CATEGORIA = "Categoria"
    SOTTOMARCA = "Sottocategoria"

class BusinessActivity(BaseModel):
    code: str
    description: str
    level: Level

    class Config:
        from_attributes = True

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
        from_attributes = True