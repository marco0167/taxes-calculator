from pydantic import BaseModel
from enum import IntEnum, StrEnum

class Regime(IntEnum):
    FORFETTARIO_5 = 1
    FORFETTARIO_15 = 2
    ORDINARIO = 3
    SEMPLIFICATO = 4
    
class Level(StrEnum):
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