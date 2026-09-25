from fastapi import FastAPI, Depends, HTTPException
from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from .database import engine, Base
from .dependency import get_db, lifespan

from .models import BusinessActivityModel, CassaPrevidenzialeModel, RiduzioniModel, UserModel, UserTaxProfileModel, InvoiceModel, ExpencesModel, TaxDeadlineModel

from .schemas import business_schemas, user_schemas, user_tax_profile
from .services.general_calculator import calculate
from .services.net_calculator import calculate_annual_net, calculate_net_quote, calculate_net_quote_with_estimated

INPS_FISSO = 4521
AGEVOLAZIONE_CONTRIBUTIVA = 0.50
COEFFICIENTE = 0.67
QUOTA_PERCENTUALE_INPS = 0.24
MINIMALE_REDDITO = 18808
ALIQUOTA_IMPOSTA_SOSTITUTIVA = 0.15

REDDITO_STIMATO = 30000
GESTIONE_SEPARATA = 0.2607

# reddito_stimato = Decimal(30000)
# coefficente = Decimal(0.67)

# inps_pagata = Decimal(0)
# acconto_inps_anno_precedente = Decimal(0)

# imposta_sostitutiva = Decimal(0.15) # 5% o 15%

# gestione_separata = Decimal(0.2607)

# acconto_tasse_anno_precedente = Decimal(0)


Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

@app.post("/users/", response_model=user_schemas.User)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = "hashed_" + user.password
    del user.password  # Remove the plain password attribute
    print(user)

    db_user = UserModel(**user.model_dump(), hashed_password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.get("/users/", response_model=List[user_schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    return db.query(UserModel).offset(skip).limit(limit).all()

@app.get("/users/{user_id}", response_model=user_schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/ateco-codes/", response_model=List[business_schemas.BusinessActivity])
def read_ateco_codes(
    skip: int = 0, 
    limit: int = 0, 
    level: Optional[business_schemas.Level] = None, 
    db: Session = Depends(get_db)
):
    if limit == 0:
        limit = None
        
    query = db.query(BusinessActivityModel)
    
    if level :
        query = query.filter(BusinessActivityModel.level == level.value).offset(skip).limit(limit)
    
    db_ateco = query.offset(skip).limit(limit).all()
    
    return db_ateco

@app.get("/casse-previdenziali/", response_model=List[user_tax_profile.CassaPrevidenziale])
def read_cassa_previdenziale(
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    query = db.query(CassaPrevidenzialeModel)
    
    if search and search.strip():
        search_term = f"%{search.lower()}%"
        query = query.filter(
            or_(
                CassaPrevidenzialeModel.id.ilike(search_term),
                CassaPrevidenzialeModel.nome.ilike(search_term),
                CassaPrevidenzialeModel.descrizione.ilike(search_term)
            )
        )
    
    db_cassa = query.offset(skip).limit(limit).all()
    
    if not db_cassa:
        raise HTTPException(status_code=404, detail="Cassa Previdenziale not found")
    
    return db_cassa

# @app.post("/user-tax-profile/", response_model=user_tax_profile.UserTaxProfile)
# def create_user_tax_profile(profile: user_tax_profile.UserTaxProfileCreate, db: Session = Depends(get_db)):

@app.get("/")
def root():
    return {"message": "Home page of the API. Use /docs to see the documentation."}

@app.post("/calculate-annual-net")
def calculate_annual_net_endpoint(
    reddito_annuo: float, 
    contributi_fissi: float,
    agevolazione_contributiva: float,
    coefficiente: float,
    quota_percentuale_inps: float,
    minimale_reddito: float,
    imposta_sostitutiva: float
):
    return {"netto_annuale": calculate_annual_net(
        reddito_annuo, 
        contributi_fissi,
        agevolazione_contributiva,
        coefficiente,
        quota_percentuale_inps,
        minimale_reddito,
        imposta_sostitutiva
    )}
    
@app.post("/calculate-net-quote")
def calculate_net_quote_endpoint(
    lordo_preventivo: float, 
    agevolazione_contributiva: float,
    coefficiente: float,
    quota_percentuale_inps: float,
    imposta_sostitutiva: float
):
    return {"netto_preventivo": calculate_net_quote(
        lordo_preventivo, 
        agevolazione_contributiva,
        coefficiente,
        quota_percentuale_inps,
        imposta_sostitutiva
    )}
    
@app.post("/calculate-net-quote-with-estimated")
def calculate_net_quote_with_estimated_endpoint(
    reddito_annuo_stimato: float,
    lordo_preventivo: float,
    contributi_fissi: float,
    agevolazione_contributiva: float,
    coefficiente: float,
    quota_percentuale_inps: float,
    minimale_reddito: float,
    imposta_sostitutiva: float
):
    return {"netto_stimato": calculate_net_quote_with_estimated(
        reddito_annuo_stimato,
        lordo_preventivo,
        contributi_fissi,
        agevolazione_contributiva,
        coefficiente,
        quota_percentuale_inps,
        minimale_reddito,
        imposta_sostitutiva
    )}


# def main():
#     # print(f"Netto annuale: {calculate_annual_net(30000, INPS_FISSO, AGEVOLAZIONE_CONTRIBUTIVA, COEFFICIENTE, QUOTA_PERCENTUALE_INPS, MINIMALE_REDDITO, ALIQUOTA_IMPOSTA_SOSTITUTIVA)}€")
#     # print(f"Netto preventivo: {calculate_net_quote(1000, AGEVOLAZIONE_CONTRIBUTIVA, COEFFICIENTE, QUOTA_PERCENTUALE_INPS, ALIQUOTA_IMPOSTA_SOSTITUTIVA)}€")
#     # print(f"Netto stimato: {calculate_net_quote_with_estimated(30000, 1000, INPS_FISSO, AGEVOLAZIONE_CONTRIBUTIVA, COEFFICIENTE, QUOTA_PERCENTUALE_INPS, MINIMALE_REDDITO, ALIQUOTA_IMPOSTA_SOSTITUTIVA)}€")

#     value = calculate(
#         REDDITO_STIMATO,
#         COEFFICIENTE,
#         0,
#         0,
#         ALIQUOTA_IMPOSTA_SOSTITUTIVA,
#         GESTIONE_SEPARATA,
#         0
#     )
#     print(value)
#     print(f"Da pagare a Giugno: {value['june_payment']['total']}, \nDa pagare a Novembre: {value['november_payment']['total']}")

# if __name__ == "__main__": 
#     main()