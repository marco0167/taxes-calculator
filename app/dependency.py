from app.database import SessionLocal

def get_db():
    db = SessionLocal()  # Create new session
    try:
        yield db  # Provide it to the request
    finally:
        db.close()  # Ensure it's closed after request finishes