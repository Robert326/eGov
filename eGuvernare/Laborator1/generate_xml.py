import xml.etree.ElementTree as ET
import os

def genereaza_xml(cerere, numar, data):
    radacina = ET.Element("cerere", numar = numar, data = data)

    contribuabil = ET.SubElement(radacina, "contribuabil")

    cnp = ET.SubElement(contribuabil,"cnp")
    cnp.text = cerere["cnp"]

    nume = ET.SubElement(contribuabil,"nume")
    nume.text = cerere["nume"]

    prenume = ET.SubElement(contribuabil,"prenume")
    prenume.text = cerere["prenume"]

    email = ET.SubElement(contribuabil,"email")
    email.text = cerere["email"]

    telefon = ET.SubElement(contribuabil,"telefon")
    telefon.text = cerere["telefon"]

    cladire = ET.SubElement(radacina,"cladire")

    localitate = ET.SubElement(cladire,"localitate")
    localitate.text = cerere["localitate"]

    adresa = ET.SubElement(cladire,"adresa")
    adresa.text = cerere["adresa"]

    tip = ET.SubElement(cladire,"tip")
    tip.text = cerere["tip"]

    valoare = ET.SubElement(cladire,"valoare")
    valoare.text = str(cerere["valoare"])

    an_fiscal = ET.SubElement(cladire,"an_fiscal")
    an_fiscal.text = cerere["an_fiscal"]

    calcul = ET.SubElement(radacina,"calcul")

    cota = ET.SubElement(calcul,"cota")
    cota.text = str(cerere["cota"])

    impozit = ET.SubElement(calcul,"impozit")
    impozit.text = str(cerere["impozit"])

    bonificatie = ET.SubElement(calcul,"bonificatie")
    bonificatie.text = str(cerere["bonificatie"])

    total = ET.SubElement(calcul,"total")
    total.text = str(cerere["total"])

    plata = ET.SubElement(radacina, "plata")

    beneficiar = ET.SubElement(plata,"beneficiar")
    beneficiar.text = cerere["beneficiar"]

    iban = ET.SubElement(plata,"iban")
    iban.text = cerere["iban"]

    ET.indent(radacina)
    text = ET.tostring(radacina, encoding="unicode")
    folder = os.path.join(os.path.dirname(__file__), "generate")
    os.makedirs(folder, exist_ok=True)
    cale = os.path.join(folder, "cerere_" + numar + ".xml")
    with open(cale, "w", encoding="utf-8") as f:
        f.write(text)
    return text

