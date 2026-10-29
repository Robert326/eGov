import os
import sqlite3

CALE_DB = os.path.join(os.path.dirname(__file__), "cereri.db")

def creeaza_tabel():
    conexiune = sqlite3.connect(CALE_DB)
    conexiune.execute("""
        CREATE TABLE IF NOT EXISTS cereri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            cnp TEXT,
            nume TEXT,
            prenume TEXT,
            email TEXT,
            telefon TEXT,
            localitate TEXT,
            adresa TEXT,
            tip TEXT,
            valoare REAL,
            an_fiscal INTEGER,
            cota REAL,
            impozit REAL,
            bonificatie REAL,
            total REAL,
            beneficiar TEXT,
            iban TEXT,
            xml TEXT
        )
    """)
    conexiune.commit()
    conexiune.close()

def salveaza_cerere(cerere, data):
    conexiune = sqlite3.connect(CALE_DB)
    cursor = conexiune.execute(
        """
        INSERT INTO cereri(
            data, cnp, nume, prenume, email, telefon,
            localitate, adresa, tip, valoare, an_fiscal,
            cota, impozit, bonificatie, total, beneficiar, iban
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data, cerere["cnp"], cerere["nume"], cerere["prenume"], cerere["email"], cerere["telefon"],
            cerere["localitate"], cerere["adresa"], cerere["tip"], cerere["valoare"], cerere["an_fiscal"],
            cerere["cota"], cerere["impozit"], cerere["bonificatie"], cerere["total"], cerere["beneficiar"], cerere["iban"],
        
        )
    )
    id_cerere = cursor.lastrowid
    conexiune.commit()
    conexiune.close()
    return id_cerere

def salveaza_xml(id_cerere, text_xml):
    conexiune = sqlite3.connect(CALE_DB)
    conexiune.execute(
        "UPDATE cereri SET xml = ? WHERE id = ?",
        (text_xml, id_cerere),
    )
    conexiune.commit()
    conexiune.close()