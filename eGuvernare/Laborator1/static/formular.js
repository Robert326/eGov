/*
"BUC01": {                                      -> Cod = BUC01
    "nume": "București, Sector 1",
    "beneficiar": "DGITL Sector 1 (simulat)",
    "iban": "RO62TREZ70121A3005300000",
    "cota_rezidentiala": 0.1,
    "cota_nerezidentiala": 0.5
  }

*/

let localitati = {};

const listaLocalitati = document.getElementById("localitate");
const beneficiar = document.getElementById("beneficiar");
const iban = document.getElementById("iban");
const tipCladire = document.getElementById("tip_cladire");
const cota = document.getElementById("cota");
const valoare_impozabila = document.getElementById("valoare_impozabila");
const impozit_anual = document.getElementById("impozit_anual");
const bonificatie = document.getElementById("bonificatie");
const plata = document.getElementById("plata");
const totalPlata = document.getElementById("total_plata");
const cnp = document.getElementById("cnp");
const dataNasterii = document.getElementById("data_nasterii");
const sex = document.getElementById("sex");
const eroareCnp = document.getElementById("eroare_cnp");

async function incarcaLocalitati() {
    const raspuns = await fetch("/static/localitati.json");

    const date = await raspuns.json();
    localitati = date;

    for (const cod in date) {
        const optiune = document.createElement("option");
        optiune.value = cod;
        optiune.textContent = date[cod].nume;
        listaLocalitati.appendChild(optiune);
    }
}

incarcaLocalitati();

listaLocalitati.addEventListener("change", function () {
    const cod = listaLocalitati.value;

    if (cod === "") {
        beneficiar.value = "";
        iban.value = "";
    } else {
        const localitate = localitati[cod];
        beneficiar.value = localitate.beneficiar;
        iban.value = localitate.iban;
    }
    recalculeaza();
});

tipCladire.addEventListener("change", function () {
    recalculeaza();
});

function recalculeaza() {
    const tip = tipCladire.value;
    if (listaLocalitati.value === "" || tip === "") {
        cota.value = "";
        impozit_anual.value = "";
        bonificatie.value = "";
        totalPlata.value = "";
        return;
    }
    const localitate = localitati[listaLocalitati.value];
    let procentCota = 0;
    if (tip === "R") {
        cota.value = localitate.cota_rezidentiala;
        procentCota = Number(cota.value);
    } else if (tip === "N") {
        cota.value = localitate.cota_nerezidentiala;
        procentCota = Number(cota.value);
    }

    let valoare = Number(valoare_impozabila.value);

    if (valoare <= 0) {
        impozit_anual.value = "";
        bonificatie.value = "";
        totalPlata.value = "";
        return;
    }

    let impozitFinal = (valoare * procentCota) / 100;
    let bonificatiaSuma;
    if (plata.checked) {
        bonificatiaSuma = (impozitFinal * 10) / 100;
    } else {
        bonificatiaSuma = 0;
    }

    let total = impozitFinal - bonificatiaSuma;

    impozit_anual.value = impozitFinal.toFixed(2);
    bonificatie.value = bonificatiaSuma.toFixed(2);
    totalPlata.value = total.toFixed(2);
}

valoare_impozabila.addEventListener("input", function () {
    recalculeaza();
});

plata.addEventListener("change", function () {
    recalculeaza();
});

function dateCNP() {
    let S = cnp.value[0];
    let secol;
    let gender;

    if (S === "1") {
        secol = "19";
        gender = "Masculin";
    } else if (S === "2") {
        secol = "19";
        gender = "Feminin";
    } else if (S === "5") {
        secol = "20";
        gender = "Masculin";
    } else if (S === "6") {
        secol = "20";
        gender = "Feminin";
    } else {
        dataNasterii.value = "";
        sex.value = "";
        return;
    }

    let year = cnp.value.slice(1, 3);
    let month = cnp.value.slice(3, 5);
    let day = cnp.value.slice(5, 7);

    let birthday = day + "." + month + "." + secol + year;

    dataNasterii.value = birthday;
    sex.value = gender;
}

cnp.addEventListener("input", function () {
    if (cnp.value.length !== 13) {
        sex.value = "";
        dataNasterii.value = "";
        eroareCnp.textContent = "";
        cnp.setCustomValidity("");
        return;
    }

    if (verifyCNP(cnp.value) == false) {
        sex.value = "";
        dataNasterii.value = "";
        eroareCnp.textContent = "CNP Invalid!";
        cnp.setCustomValidity("CNP Invalid!");
    } else {
        eroareCnp.textContent = "";
        cnp.setCustomValidity("");
        dateCNP();
    }
});

function verifyCNP(cnpText) {
    let sum = 0;
    const number = "279146358279";
    for (let i = 0; i < 12; i++) {
        sum = sum + Number(cnpText[i]) * Number(number[i]);
    }

    let rest = sum % 11;
    let cifraControl = 0;

    if (rest === 10) {
        cifraControl = 1;
    } else {
        cifraControl = rest;
    }

    return cifraControl === Number(cnpText[12]);
}
