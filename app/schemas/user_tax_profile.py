from pydantic import BaseModel
from enum import Enum

class AliquotaImpostaSostitutiva(Enum):
    FORFETTARIO_5 = 0.05
    FORFETTARIO_15 = 0.15

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
        
    