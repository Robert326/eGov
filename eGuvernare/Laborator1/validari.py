import re
import math

def cnp_valid(cnpText):
    if len(cnpText) != 13 or not cnpText.isdigit():
        return False
    suma = 0
    verificator = "279146358279"

    for i in range (12) :
        suma += int(cnpText[i]) * int(verificator[i])

    rest = suma % 11
    cifraControl = 0

    if (rest == 10):
        cifraControl = 1
    else:
        cifraControl = rest

    return cifraControl == int(cnpText[12])

def telefon_valid(telefon):
    return re.fullmatch(r"07[0-9]{8}", telefon) is not None

def email_valid(email):
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is not None

def nume_persoana_valid(nume):
    return re.fullmatch(r"[A-Za-zăâîșțĂÂÎȘȚ \-]+", nume) is not None

def exista_localitatea(cod_localitate, localitati):
    return cod_localitate in localitati

def tip_corect(tip):
    return tip in ("R", "N")

def an_corect(valoare):
    try:
        numar = int(valoare)
    except ValueError:
        return False # daca nu introduce numar si e ("abc")

    if math.isfinite(numar) is False:
        return False

    return 2000 <= numar <= 2030

def adresa_cladire(adresa):
    return adresa.strip() != ""

def valoare_impozabila_check(valoare):
    try:
        numar = float(valoare)
    except ValueError:
        return False # daca nu introduce numar si e ("abc")

    if math.isfinite(numar) is False:
        return False

    if numar <= 0:
        return False

    return True

def valideaza_cererea(date, localitati):
    erori = []

    if (not cnp_valid(date.get("cnp", ""))):
        erori.append("Cnp Invalid!")
    
    if (not telefon_valid(date.get("telefon", ""))):
        erori.append("Număr de telefon invalid!")
    
    if (not email_valid(date.get("email", ""))):
        erori.append("Email invalid!")

    if (not nume_persoana_valid(date.get("nume", ""))):
        erori.append("Nume invalid!")

    if (not nume_persoana_valid(date.get("prenume", ""))):
        erori.append("Prenume invalid!")

    if (not valoare_impozabila_check(date.get("valoare_impozabila", ""))):
        erori.append("Valoare impozabila invalida!")

    if (not exista_localitatea(date.get("localitate", ""), localitati)):
        erori.append("Localitate inexistenta!")

    if (not tip_corect(date.get("tip_cladire"))):
        erori.append("Tip clădire inexistent!")

    if (not an_corect(date.get("an_fiscal",""))):
        erori.append("An fiscal incorect!")

    if (not adresa_cladire(date.get("adresa_cladirii", ""))):
        erori.append("Adresa clădirii lipsește!")

    if (date.get("declaratie") != "on"):
        erori.append("Declarația nu a fost bifată!")

    return erori
