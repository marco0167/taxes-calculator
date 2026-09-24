import csv
import os

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import BusinessActivity

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
        seed_ateco_table(db, csv_filename="codici_ateco_2025.csv")
    finally:
        db.close()

        print("Database connection closed.")
    yield
import re


def seed_ateco_table(db: Session, csv_filename: str = "ateco_data.csv"):
    has_data = db.query(BusinessActivity).with_entities(BusinessActivity.code).first() is not None

    if has_data:
        print("ATECO codes table already populated. Skip seeding.")
        return

    print("ATECO codes table is empty. Starting seeding...")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "data", csv_filename)

    if not os.path.exists(csv_path):
        print(f"Error: The file {csv_path} does not exist. Unable to populate the table.")
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
            db.bulk_insert_mappings(BusinessActivity, records_to_insert)
            db.commit()
            print(f"Success! Inserted {len(records_to_insert)} records in the ATECO table.")
        except Exception as e:
            db.rollback()
            print(f"Error during the seeding of the ATECO codes: {e}")


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

