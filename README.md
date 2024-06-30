# Extract the Update of Judicial Files

This project provides a Python script that extracts updates on judicial files from the Moroccan judicial system's online services.

## Requirements

- Python 3.x
- `requests` library
- `pandas` library
- `numpy` library

You can install the required libraries using `pip`:

```sh
pip install requests pandas numpy
How It Works
The script performs the following steps to retrieve judicial file information:

Reference: Construct a reference using the code, jurisdiction, and year.
Fetch Jurisdictions: Use the API to get the list of jurisdictions for the specified code.
Choose the Court: Select the appropriate court from the list.
Fetch Tribunal: Use the API to get the list of tribunals for the specified jurisdiction.
Get File Details: Retrieve the file details using the constructed reference and selected tribunal ID.
Get Decisions: Extract the decisions related to the file.
Get Parties: List the parties involved in the case.
Usage
Place your list of cases in an Excel file named list.xlsx. The file should have columns for year, juridiction, reference, CAcode, and TPIcode.

Run the script:

sh

python script.py
The script will process each row in the Excel file, fetch the relevant judicial file details, and save the output to lista.xlsx.
Script
python

import requests
import pandas as pd
from datetime import datetime
import numpy as np

def ctx(year, juridict, reference, idCA, idTPI):
    api = "https://www.mahakim.ma/middleware/api/SuiviDossiers/"
    
    link2 = api + "ListeJuridictions2Instance?CodeDossier=" + str(juridict)
    etape1 = requests.get(link2, verify=False)
    CA = etape1.json()
    coursA = CA.get('data', [])
    coursA = pd.DataFrame(coursA, columns=['idJuridiction', 'nomJuridiction'])
    coursA = coursA.to_numpy()
    IDjuridiction = idCA

    link3 = api + "Juridictions1Instance?CodeDossier=" + str(juridict) + "&idJuridiction2Instance=" + str(IDjuridiction)
    etape4 = requests.get(link3, verify=False)
    TPI = etape4.json()
    Trib = TPI.get('data', [])
    Trib = pd.DataFrame(Trib, columns=['idJuridiction', 'nomJuridiction'])
    Trib = Trib.to_numpy()
    IDtribunal = idTPI

    link4 = api + "CarteDossier?numeroCompletDossier=" + str(year) + str(juridict) + str(reference) + "&idjuridiction=" + str(IDtribunal)
    etape5 = requests.get(link4, verify=False)
    mapfile = etape5.json()
    claimfile = mapfile.get('data', [])
    Idfile = claimfile['idDossierCivil']
    typeaffaire = claimfile['affaire']

    link5 = api + "ListeDicisions?idDossier=" + str(Idfile) + "&typeaffaire=" + str(typeaffaire)
    etape6 = requests.get(link5, verify=False)
    steps = etape6.json()
    stepp = steps.get('data', [])
    finalstep = stepp[0]
    decision = finalstep['contenuDecision']
    nextdate = finalstep['dateTimeNextAudience']
    datefinal = finalstep['dateTimeDecision']
    datefinal = datefinal[:10]
    dateformat = "%d/%m/%Y"
    datefinale = datetime.strptime(datefinal, dateformat)

    link6 = api + "ListeParties?idDossier=" + str(Idfile) + "&typeaffaire=" + str(typeaffaire)
    etape7 = requests.get(link6, verify=False)
    parts = etape7.json()
    nomPrenomPartie = [entry['nomPrenomPartie'] for entry in parts['data']]
    rolePartie = [entry['rolePartie'] for entry in parts['data']]
    codeTypePersonne = ["personne morale" if entry['codeTypePersonne'] == "PM" else "personne physique" for entry in parts['data']]
    listedesparties = pd.DataFrame({'nomPrenomPartie': nomPrenomPartie, 'rolePartie': rolePartie, 'codeTypePersonne': codeTypePersonne})

    if nextdate == '':
        return decision, datefinale, listedesparties
    else:
        return decision, nextdate, listedesparties

listdes = pd.read_excel('list.xlsx')
listdes[['Output1', 'Output2', 'typess']] = listdes.apply(lambda row: pd.Series(ctx(row['year'], row['juridiction'], row['reference'], row['CAcode'], row['TPIcode'])), axis=1)
listdes.to_excel('lista.xlsx', index=False)
Notes
Ensure that you handle API requests properly and be mindful of the rate limits.
This script disables SSL verification (verify=False) for the requests. This might expose you to security risks. Enable SSL verification in a production environment.
License
This project is licensed under the MIT License - see the LICENSE file for details.

javascript

Replace `script.py` with the actual name of your Python script if it differs.
