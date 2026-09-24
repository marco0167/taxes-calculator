from decimal import Decimal

def calculate_annual_net(
    _reddito_annuo: float, 
    _contributi_fissi: float,
    _agevolazione_contributiva: float,
    _coefficiente: float,
    _quota_percentuale_inps: float,
    _minimale_reddito: float,
    _imposta_sostitutiva: float
):
    ra = Decimal(_reddito_annuo) # Fatturato
    cf = Decimal(_contributi_fissi) # Contributi fissi
    ac = Decimal(_agevolazione_contributiva) # Agevolazione contributiva
    co = Decimal(_coefficiente) # Coefficiente
    qpi = Decimal(_quota_percentuale_inps) # Quota percentuale imponibile
    mr = Decimal(_minimale_reddito) # Minimale reddito
    imp_s = Decimal(_imposta_sostitutiva) # Imposta sostitutiva
    
    quota_eccedenza = Decimal(0)

    imponibile = ra * co
    if imponibile > mr:
        quota_eccedenza = (imponibile - mr) * qpi
  
    contributi = cf + quota_eccedenza
    if ac > 0:
        contributi = contributi * (1 - ac)
        
    base_imponibile_netta = imponibile - contributi
    netto = ra - (base_imponibile_netta * imp_s) - contributi  

    return format(netto, '.2f')

# For approximative calculation of the net for a "preventivo"
def calculate_net_quote(
    _lordo_preventivo: float, 
    _agevolazione_contributiva: float,
    _coefficiente: float,
    _quota_percentuale_inps: float,
    _imposta_sostitutiva: float
):
    lp = Decimal(_lordo_preventivo) # Fatturato
    ac = Decimal(_agevolazione_contributiva) # Agevolazione contributiva
    co = Decimal(_coefficiente) # Coefficiente
    qpi = Decimal(_quota_percentuale_inps) # Quota percentuale imponibile
    imp_s = Decimal(_imposta_sostitutiva) # Imposta sostitutiva
    
    contributi = lp * co * qpi * (1 - ac)
    imposta_sostitutiva = (lp - contributi) * co * imp_s
    netto = lp - contributi - imposta_sostitutiva
    
    return format(netto, '.2f')

def calculate_net_quote_with_estimated(
    _reddito_annuo_stimato: float,
    _lordo_preventivo: float,
    _contributi_fissi: float,
    _agevolazione_contributiva: float,
    _coefficiente: float,
    _quota_percentuale_inps: float,
    _minimale_reddito: float,
    _imposta_sostitutiva: float
):
    ras = Decimal(_reddito_annuo_stimato) # Reddito annuo stimato
    lp = Decimal(_lordo_preventivo) # Fatturato
    cf = Decimal(_contributi_fissi) # Contributi fissi
    ac = Decimal(_agevolazione_contributiva) # Agevolazione contributiva
    co = Decimal(_coefficiente) # Coefficiente
    qpi = Decimal(_quota_percentuale_inps) # Quota percentuale imponibile
    mr = Decimal(_minimale_reddito) # Minimale reddito
    imp_s = Decimal(_imposta_sostitutiva) # Imposta sostitutiva
    
    eccedenza = Decimal(0)
    contributi_fissi = cf * (1 - ac)
    peso = lp / ras
    quota_inps_fissa = contributi_fissi * peso
    reddito_imponibile = lp * co
    
    if ras > mr:
        eccedenza = (reddito_imponibile - (mr * peso)) * qpi * (1 - ac)
    
    contributi = quota_inps_fissa + eccedenza
    base_tassabile = reddito_imponibile - contributi
    imposta_sostitutiva = base_tassabile * imp_s
    netto = lp - contributi - imposta_sostitutiva
    
    return format(netto, '.2f')