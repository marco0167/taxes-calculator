

from app.services.general_calculator import calculate
from app.services.net_calculator import calculate_annual_net, calculate_net_quote, calculate_net_quote_with_estimated

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


def main():
    print(f"Netto annuale: {calculate_annual_net(30000, INPS_FISSO, AGEVOLAZIONE_CONTRIBUTIVA, COEFFICIENTE, QUOTA_PERCENTUALE_INPS, MINIMALE_REDDITO, ALIQUOTA_IMPOSTA_SOSTITUTIVA)}€")
    print(f"Netto preventivo: {calculate_net_quote(1000, AGEVOLAZIONE_CONTRIBUTIVA, COEFFICIENTE, QUOTA_PERCENTUALE_INPS, ALIQUOTA_IMPOSTA_SOSTITUTIVA)}€")
    print(f"Netto stimato: {calculate_net_quote_with_estimated(30000, 1000, INPS_FISSO, AGEVOLAZIONE_CONTRIBUTIVA, COEFFICIENTE, QUOTA_PERCENTUALE_INPS, MINIMALE_REDDITO, ALIQUOTA_IMPOSTA_SOSTITUTIVA)}€")

    value = calculate(
        REDDITO_STIMATO,
        COEFFICIENTE,
        0,
        0,
        ALIQUOTA_IMPOSTA_SOSTITUTIVA,
        GESTIONE_SEPARATA,
        0
    )
    print(value)
    print(f"Da pagare a Giugno: {value['june_payment']['total']}, \nDa pagare a Novembre: {value['november_payment']['total']}")

if __name__ == "__main__": 
    main()