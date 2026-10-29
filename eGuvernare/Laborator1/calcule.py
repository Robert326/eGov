import json
import os

CALE_LOCALITATI = os.path.join(os.path.dirname(__file__), "static", "localitati.json")


def incarca_localitati():
    with open(CALE_LOCALITATI, encoding="utf-8") as fisier:
        return json.load(fisier)


def calculeaza(valoare, cota, plata_integrala):
    impozit = valoare * cota / 100

    if plata_integrala:
        bonificatie = impozit * 10 / 100
    else:
        bonificatie = 0

    total = impozit - bonificatie

    return {
        "impozit": round(impozit, 2),
        "bonificatie": round(bonificatie, 2),
        "total": round(total, 2),
    }
