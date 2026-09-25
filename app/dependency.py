import csv
import os
import uuid

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from sqlalchemy.orm import Session
from decimal import Decimal

from .database import SessionLocal
from .models import BusinessActivityModel, CassaPrevidenzialeModel,  RiduzioniModel
from .schemas.business_schemas import Regime
from .schemas.user_tax_profile import TargetRiduzione

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal() 
    
    try:
        seed_riduzioni_table(db, csv_filename="riduzioni_attuali.csv")
        seed_ateco_table(db, csv_filename="codici_ateco_2025.csv")
        seed_casse_table(db, csv_filename="casse_previdenziali.csv")
    finally:
        db.close()

        print("Database connection closed.")
    yield
import re


def seed_ateco_table(db: Session, csv_filename: str = "codici_ateco_2025.csv"):
    has_data = db.query(BusinessActivityModel).with_entities(BusinessActivityModel.code).first() is not None

    if has_data:
        print(f"\n{bcolors.OKCYAN}ATECO codes table already populated. {bcolors.HEADER}Skip seeding.{bcolors.ENDC}")
        return

    print(f"\n{bcolors.OKBLUE}ATECO codes table is empty. {bcolors.HEADER}Starting seeding...{bcolors.ENDC}")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "data", csv_filename)

    if not os.path.exists(csv_path):
        print(f"{bcolors.FAIL}Error: The file {csv_path} does not exist. Unable to populate the table.{bcolors.ENDC}")
        return

    records_to_insert = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        next(f) 
        
        reader = csv.DictReader(
            f,
            delimiter=";", 
            fieldnames=["Codice", "Titolo", "Classificazione"]
        )
        
        for row in reader:
            code_raw = row.get("Codice")
            desc_raw = row.get("Titolo")
            level_raw = row.get("Classificazione")
            
            if not code_raw or not desc_raw:
                continue
                
            records_to_insert.append({
                "code": code_raw.strip(),
                "description": desc_raw.strip(),
                "level": level_raw.strip() if level_raw else "Sottocategoria"
            })

    if records_to_insert:
        try:
            db.bulk_insert_mappings(BusinessActivityModel, records_to_insert)
            db.commit()
            print(f"{bcolors.OKGREEN}Success! Inserted {len(records_to_insert)} records in the ATECO table.{bcolors.ENDC}")
        except Exception as e:
            db.rollback()
            print(f"{bcolors.FAIL}Error during the seeding of the ATECO codes: {e}{bcolors.ENDC}")

def seed_casse_table(db: Session, csv_filename: str = "casse_previdenziali.csv"):
    has_data = db.query(CassaPrevidenzialeModel).with_entities(CassaPrevidenzialeModel.id).first() is not None

    if has_data:
        print(f"\n{bcolors.OKCYAN}Casse Previdenziali table already populated. {bcolors.HEADER}Skip seeding.{bcolors.ENDC}")
        return

    print(f"\n{bcolors.OKBLUE}Casse Previdenziali table is empty. {bcolors.HEADER}Starting seeding...{bcolors.ENDC}")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "data", csv_filename)

    if not os.path.exists(csv_path):
        print(f"{bcolors.FAIL}Error: The file {csv_path} does not exist. Unable to populate the table.{bcolors.ENDC}")
        return

    records_to_insert = []
    
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")
        
        for row in reader:
            id_raw = row.get("id")
            nome_raw = row.get("nome")
            
            if not id_raw or not nome_raw:
                continue
                
            records_to_insert.append({
                "id": id_raw.strip(),
                "nome": nome_raw.strip(),
                "descrizione": row.get("descrizione", "").strip(),
                "aliquota_fattura_percentuale": Decimal(row.get("aliquota_fattura_percentuale", "0.00")),
                "aliquota_reddito_percentuale": Decimal(row.get("aliquota_reddito_percentuale", "0.00")),
                "tipo_minimale": row.get("tipo_minimale", "").strip(),
                "minimale_reddito": Decimal(row.get("minimale_soggettivo_base", "0.00")),
                "note_agevolazioni": row.get("note_agevolazioni", "").strip()
            })

    if records_to_insert:
        try:
            db.bulk_insert_mappings(CassaPrevidenzialeModel, records_to_insert)
            db.commit()
            print(f"{bcolors.OKGREEN}Success! Inserted {len(records_to_insert)} records in the Casse Previdenziali table.{bcolors.ENDC}")
        except Exception as e:
            db.rollback()
            print(f"{bcolors.FAIL}Error during the seeding of the Casse Previdenziali: {e}{bcolors.ENDC}")


def seed_riduzioni_table(db: Session, csv_filename: str = "riduzioni_attuali.csv"):
    has_data = db.query(RiduzioniModel).with_entities(RiduzioniModel.id).first() is not None

    if has_data:
        print(f"\n{bcolors.OKCYAN}Riduzioni table already populated. {bcolors.HEADER}Skip seeding.{bcolors.ENDC}")
        return

    print(f"\n{bcolors.OKBLUE}Riduzioni table is empty. {bcolors.HEADER}Starting seeding...{bcolors.ENDC}")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "data", csv_filename)

    if not os.path.exists(csv_path):
        print(f"{bcolors.FAIL}Error: The file {csv_path} does not exist. Unable to populate the table.{bcolors.ENDC}")
        return

    records_to_insert = []
    
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        
        for row in reader:
            descrizione_raw = row.get("descrizione")
            if not descrizione_raw:
                continue

            regimi_raw = row.get("regimi_fiscali_applicabili", "").strip()
            regimi_enum_list = []
            if regimi_raw:
                clean_regimi = regimi_raw.replace("{", "").replace("}", "").strip()
                if clean_regimi:
                    for x in clean_regimi.split(","):
                        if x.strip():
                            try:
                                val_int = int(x.strip())
                                regimi_enum_list.append(Regime(val_int))
                            except (ValueError, KeyError):
                                print(f"{bcolors.WARNING}Warning: {x} non è un ID valido per l'Enum Regime. Salto.{bcolors.ENDC}")


            target_raw = row.get("target_applicazione", "CONTRIBUTI_FISSI").strip().upper()
            try:
                target_enum = TargetRiduzione[target_raw]
            except KeyError:
                target_enum = TargetRiduzione.CONTRIBUTI_FISSI
                print(f"{bcolors.WARNING}Warning: Target {target_raw} non trovato. Impostato di default.{bcolors.ENDC}")

            records_to_insert.append({
                "id": uuid.uuid4(),
                "descrizione": descrizione_raw.strip(),
                "percentuale_riduzione": Decimal(row.get("percentuale_riduzione", "0.00")),
                "target_applicazione": target_enum,
                "regimi_fiscali_applicabili": regimi_enum_list
            })

    if records_to_insert:
        try:
            db.bulk_insert_mappings(RiduzioniModel, records_to_insert)
            db.commit()
            print(f"{bcolors.OKGREEN}Success! Inserted {len(records_to_insert)} records in the Riduzioni table.{bcolors.ENDC}")
        except Exception as e:
            db.rollback()
            print(f"{bcolors.FAIL}Error during the seeding of the Riduzioni: {e}{bcolors.ENDC}")

def get_coefficiente_redditivita(codice_ateco: str) -> int:
    pulito = re.sub(r'[\s.]', '', str(codice_ateco))
    
    if re.match(r'^(10|11|55|56|4781|45|46[2-9]|47[1-7]|479)', pulito):
        return 40
        
    if re.match(r'^(4782|4789)', pulito):
        return 54
        
    if re.match(r'^461', pulito):
        return 62
        
    if re.match(r'^(4[1-3]|68)', pulito):
        return 86
        
    if re.match(r'^(6[4-6]|69|7[0-5]|85|8[6-8])', pulito):
        return 78
        
    return 67

