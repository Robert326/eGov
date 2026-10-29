import os

def genereaza_ordin(cerere, numar, data):
    if cerere["tip"] == "R":
        tip = "rezidentiala"
    else:
        tip = "nerezidentiala"

    explicatie = ("Impozit cladire " + tip + " an fiscal " + str(cerere["an_fiscal"])
                  + ", " + cerere["adresa"] + ", cerere nr. " + numar)

    linie = "=" * 60
    text = "\n".join([
        linie,
        "                      ORDIN DE PLATA",
        linie,
        "Numar: " + numar,
        "Data:  " + data,
        "",
        "PLATITOR",
        "  Nume:      " + cerere["nume"] + " " + cerere["prenume"],
        "  CNP:       " + cerere["cnp"],
        "  Email:     " + cerere["email"],
        "  Telefon:   " + cerere["telefon"],
        "",
        "BENEFICIAR",
        "  Denumire:  " + cerere["beneficiar"],
        "  IBAN:      " + cerere["iban"],
        "  Banca:     Trezoreria Statului",
        "",
        "DETALII CALCUL",
        "  Valoare impozabila: " + format(cerere["valoare"], ".2f") + " lei",
        "  Cota:               " + str(cerere["cota"]) + " %",
        "  Impozit:            " + format(cerere["impozit"], ".2f") + " lei",
        "  Bonificatie:        " + format(cerere["bonificatie"], ".2f") + " lei",
        "",
        "SUMA DE PLATA: " + format(cerere["total"], ".2f") + " lei",
        "",
        "Explicatii: " + explicatie,
        linie,
        "",
    ])

    folder = os.path.join(os.path.dirname(__file__), "generate")
    os.makedirs(folder, exist_ok=True)
    cale = os.path.join(folder, "ordin_" + numar + ".txt")
    with open(cale, "w", encoding="utf-8") as f:
        f.write(text)
    return text
