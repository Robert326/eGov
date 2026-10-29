from flask import Flask, render_template, request
import validari as v
import calcule as c
from generate_xml import genereaza_xml
from generate_ordin import genereaza_ordin
from datetime import datetime
import database

app = Flask(__name__)
database.creeaza_tabel()

@app.route("/")
def index():
    return render_template("formular.html")

@app.route('/trimite', methods=['POST'])
def get_form():
    date = dict(request.form)
    localitati = c.incarca_localitati()
    print(request.form)

    erori = v.valideaza_cererea(date, localitati)

    if erori:
        return {"erori": erori}, 400

    localitate = localitati[date["localitate"]]

    if date["tip_cladire"] == "R":
        cota = localitate["cota_rezidentiala"]
    else:
        cota = localitate["cota_nerezidentiala"]

    valoare_impozabila = float(date["valoare_impozabila"])
    plata_integrala = date.get("plata") == "on"
    rezultat = c.calculeaza(valoare_impozabila,cota,plata_integrala)


    cerere = {
        # contribuabil
        "cnp": date["cnp"],
        "nume": date["nume"],
        "prenume": date["prenume"],
        "email": date["email"],
        "telefon": date["telefon"],

        # cladire
        "localitate": date["localitate"],
        "adresa": date["adresa_cladirii"],
        "tip": date["tip_cladire"],
        "valoare": valoare_impozabila,
        "an_fiscal": date["an_fiscal"],

        # calcul (facut pe server)
        "cota": cota,
        "impozit": rezultat["impozit"],
        "bonificatie": rezultat["bonificatie"],
        "total": rezultat["total"],

        # plata (din localitati.json, nu din browser)
        "beneficiar": localitate["beneficiar"],
        "iban": localitate["iban"],
    }

    # numar inregistrare si data cererii
    acum = datetime.now()
    data = acum.strftime("%Y-%m-%d %H:%M")

    id_cerere = database.salveaza_cerere(cerere,data)
    numar = str(id_cerere)

    text_xml = genereaza_xml(cerere,numar,data)
    database.salveaza_xml(id_cerere,text_xml)

    # ordin de plata (txt)
    genereaza_ordin(cerere,numar,data)

    return cerere


if __name__ == "__main__":
    app.run(port=5001)