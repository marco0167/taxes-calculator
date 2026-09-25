import uuid

from sqlalchemy import UUID, Boolean, Column, Date, Enum, Float, ForeignKey, Index, Numeric, String, Table, Text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from app.database import Base
from app.schemas import user_tax_profile
from app.schemas.business_schemas import Level, Regime
from app.schemas.user_tax_profile import AliquotaImpostaSostitutiva
    
user_riduzioni_association = Table(
    'user_riduzioni_link',
    Base.metadata,
    Column(
        'user_tax_profiles_id', 
        UUID(as_uuid=True), 
        ForeignKey('user_tax_profiles.id', ondelete='CASCADE'), 
        primary_key=True
    ),
    Column(
        '   ', 
        UUID(as_uuid=True), 
        ForeignKey('riduzioni.id', ondelete='CASCADE'), 
        primary_key=True
    )
)

class BusinessActivityModel(Base):
    __tablename__ = 'business_activities'

    code = Column(String(10), primary_key=True, index=True)
    description = Column(Text, nullable=False)
    level = Column(String(20), Enum(Level), nullable=False, index=True)
    
class CassaPrevidenzialeModel(Base):
    __tablename__ = 'casse_previdenziali'

    id = Column(String(36), primary_key=True)
    nome = Column(String(100), nullable=False, index=True)
    descrizione = Column(String(250), index=True)
    aliquota_fattura_percentuale = Column(Numeric(5, 2), default=0.00)
    aliquota_reddito_percentuale = Column(Numeric(5, 2), default=0.00)
    tipo_minimale = Column(String(50), nullable=True)
    minimale_reddito = Column(Float, default=0.00)
    note_agevolazioni = Column(Text)

class RiduzioniModel(Base):
    __tablename__ = 'riduzioni'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    descrizione = Column(String(250), index=True)
    percentuale_riduzione = Column(Numeric(5, 2), default=0.00, nullable=False)
    target_applicazione = Column(Enum(user_tax_profile.TargetRiduzione), nullable=True, default=user_tax_profile.TargetRiduzione.CONTRIBUTI_FISSI)
    regimi_fiscali_applicabili = Column(
        postgresql.ARRAY(Enum(Regime, create_type=False, values_callable=lambda x: [e.name for e in x])), 
        nullable=True
    )
    

class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserTaxProfileModel(Base):
    __tablename__ = "user_tax_profiles"

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey(UserModel.id), index=True)
    regime_fiscale = Column(postgresql.SMALLINT, Enum(Regime), nullable=False)
    codice_ateco = Column(String, ForeignKey(BusinessActivityModel.code), index=True)
    coefficiente_redditivita = Column(Float)
    cassa_previdenziale = Column(String(36), ForeignKey(CassaPrevidenzialeModel.id), index=True)
    aliquota_imposta = Column(Float, Enum(AliquotaImpostaSostitutiva), nullable=False)
    aliquota_inps = Column(Numeric(5, 2), default=0.00)
    aliquota_inps_personale = Column(Numeric(5, 2), default=0.00)
    contibuto_fisso_inps = Column(Numeric(10, 2), default=0.00)
    anno_inizio_attivita = Column(postgresql.SMALLINT)
    riduzioni_applicabili = relationship(
        "RiduzioniModel", 
        secondary=user_riduzioni_association,
        backref="user_tax_profiles"
    )

class InvoiceModel(Base):
    __tablename__ = "invoices"

    id = Column(UUID, primary_key=True)
    profile_id = Column(UUID, ForeignKey(UserTaxProfileModel.id), index=True)
    data_pagamento = Column(Date)
    data_incasso = Column(Date, nullable=True)
    data_incasso_prevista = Column(Date, nullable=True)
    amount = Column(Float)
    bollo = Column(Float, default=0.0)
    rivalsa_inps_addebitata = Column(Float, default=0.0)

Index('idx_invoices_data_incasso', InvoiceModel.profile_id, InvoiceModel.data_incasso)
Index('idx_invoices_data_incasso_prevista', InvoiceModel.profile_id, InvoiceModel.data_incasso_prevista)

class ExpencesModel(Base):
    __tablename__ = "expences"

    id = Column(UUID, primary_key=True)
    profile_id = Column(UUID, ForeignKey(UserTaxProfileModel.id), index=True)
    amount = Column(Float)
    data_pagamento = Column(Date, nullable=True)
    is_contributo_inps = Column(Boolean, default=False)
    description = Column(String, nullable=True)
    
Index('idx_expences_data_pagamento', ExpencesModel.profile_id, ExpencesModel.data_pagamento)

class TaxDeadlineModel(Base):
    __tablename__ = "tax_deadlines"

    id = Column(UUID, primary_key=True)
    profile_id = Column(UUID, ForeignKey(UserTaxProfileModel.id), index=True)
    tipo_imposta = Column(String)
    data_scadenza = Column(Date)
    importo_previsto = Column(Float)
    importo_pagato = Column(Float, default=0.0)
    is_pagato = Column(Boolean, default=False)
    
Index('idx_tax_deadlines_data_scadenza', TaxDeadlineModel.profile_id, TaxDeadlineModel.data_scadenza)
    