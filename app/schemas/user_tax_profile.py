from pydantic import BaseModel
from enum import StrEnum, Enum

class AliquotaImpostaSostitutiva(float, Enum):
    FORFETTARIO_5 = 0.05
    FORFETTARIO_15 = 0.15
    
class TargetRiduzione(StrEnum):
    CONTRIBUTI_FISSI = "contributi_fissi"
    CONTRIBUTI_ECCEDENTI = "contributi_eccedenti"
    IMPOSTA_SOSTITUTIVA = "imposta_sostitutiva"
    TOTALE_CONTRIBUTI = "totale_contributi"

class CassaPrevidenziale(BaseModel):
    id: str
    nome: str
    descrizione: str
    aliquota_fattura_percentuale: float
    aliquota_reddito_percentuale: float
    note_agevolazioni: str
    tipo_minimale: str

    class Config:
        from_attributes = True
        
class UserTaxProfileCreate(BaseModel):
    user_id: str
    regime_fiscale: int
    codice_ateco: str
    coefficiente_redditivita: float
    cassa_previdenziale: str
    aliquota_imposta: float
    aliquota_inps_personale: float
    riduzioni_applicabili: list[str]
    anno_inizio_attivita: int

    class Config:
        from_attributes = True