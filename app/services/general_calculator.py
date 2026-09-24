from decimal import Decimal

def calculate(
    _reddito_stimato: int,
    _coefficente: float,
    _inps_pagata: float,
    _acconto_inps_anno_precedente: float,
    _imposta_sostitutiva: float,
    _gestione_separata: float,
    _acconto_tasse_anno_precedente: float
):
    reddito_stimato = Decimal(_reddito_stimato)
    coefficente = Decimal(_coefficente)
    inps_pagata = Decimal(_inps_pagata)
    acconto_inps_anno_precedente = Decimal(_acconto_inps_anno_precedente)
    imposta_sostitutiva = Decimal(_imposta_sostitutiva)
    gestione_separata = Decimal(_gestione_separata)
    acconto_tasse_anno_precedente = Decimal(_acconto_tasse_anno_precedente)
    
    imponibile_lordo = reddito_stimato * coefficente
    print("imponibile lordo: ", format(imponibile_lordo, '.2f'))
    
    imponibile_netto = imponibile_lordo - inps_pagata
    print("imponibile netto: ", format(imponibile_netto, '.2f'))
    
    total_tax_due = imponibile_netto * imposta_sostitutiva
    print("tasse dovute: ", format(total_tax_due, '.2f'))
    
    total_inps_due = imponibile_lordo * gestione_separata
    print("inps dovute: ", format(total_inps_due, '.2f'))
    
    # Saldo da pagare a giugno
    tax_balance = total_tax_due - acconto_tasse_anno_precedente
    print("saldo tasse: ", format(tax_balance, '.2f'))
    inps_balance = total_inps_due - acconto_inps_anno_precedente
    print("saldo inps: ", format(inps_balance, '.2f'))
    
    
    return {
        'june_payment': {
            'balance': format(tax_balance + inps_balance, '.2f'),
            'tax_advance': format(total_tax_due * Decimal(0.5), '.2f'), # Primo acconto tasse
            'inps_advance': format(total_inps_due * Decimal(0.4), '.2f'), # Primo acconto Inps
            'total': format(tax_balance + inps_balance + total_tax_due * Decimal(0.5) + total_inps_due * Decimal(0.4), '.2f')
        },
        'november_payment': {
            'tax_advance': format(total_tax_due * Decimal(0.5), '.2f'), # Secondo acconto tasse
            'inps_advance': format(total_inps_due * Decimal(0.4), '.2f'), # Secondo acconto Inps
            'total': format(total_tax_due * Decimal(0.5) + total_inps_due * Decimal(0.4), '.2f')
        },
    }
    