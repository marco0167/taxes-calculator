from sqlalchemy import UUID, Boolean, Column, Date, Enum, Float, Index, Integer, String, Text
from app.database import Base
from app.schemas.business_schemas import Regime
    
class BusinessActivity(Base):
    __tablename__ = 'business_activities'

    code = Column(String(10), primary_key=True, index=True)
    description = Column(Text, nullable=False)
    level = Column(String(20), nullable=False, index=True) 

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserTaxProfile(Base):
    __tablename__ = "user_tax_profiles"

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, foreign_key="users.id", index=True)
    regime_fiscale = Column(String, Enum(Regime), nullable=False)
    coefficiente_redditivita = Column(Float)
    aliquota_imposta = Column(Float)
    type_inps = Column(String)
    aliquota_inps = Column(Float)
    contibuto_fisso_inps = Column(Float)
    anno_inizio_attivita = Column(Integer)
    
class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(UUID, primary_key=True)
    profile_id = Column(UUID, foreign_key="user_tax_profiles.id", index=True)
    data_pagamento = Column(Date)
    data_incasso = Column(Date, nullable=True)
    data_incasso_prevista = Column(Date, nullable=True)
    amount = Column(Float)
    bollo = Column(Float, default=0.0)
    rivalsa_inps_addebitata = Column(Float, default=0.0)

Index('idx_invoices_data_incasso', Invoice.profile_id, Invoice.data_incasso)
Index('idx_invoices_data_incasso_prevista', Invoice.profile_id, Invoice.data_incasso_prevista)

class Expences(Base):
    __tablename__ = "expences"

    id = Column(UUID, primary_key=True)
    profile_id = Column(UUID, foreign_key="user_tax_profiles.id", index=True)
    amount = Column(Float)
    data_pagamento = Column(Date, nullable=True)
    is_contributo_inps = Column(Boolean, default=False)
    description = Column(String, nullable=True)
    
Index('idx_expences_data_pagamento', Expences.profile_id, Expences.data_pagamento)

class TaxDeadline(Base):
    __tablename__ = "tax_deadlines"

    id = Column(UUID, primary_key=True)
    profile_id = Column(UUID, foreign_key="user_tax_profiles.id", index=True)
    tipo_imposta = Column(String)
    data_scadenza = Column(Date)
    importo_previsto = Column(Float)
    importo_pagato = Column(Float, default=0.0)
    is_pagato = Column(Boolean, default=False)
    
Index('idx_tax_deadlines_data_scadenza', TaxDeadline.profile_id, TaxDeadline.data_scadenza)
    