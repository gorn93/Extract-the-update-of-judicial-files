#ArithmeticError

#lien code de juridiction ---> L instances --> carte dossier complet
# liste dicision

# etape 1 : reference = code + juridiction + annee
# etape 2 :https://www.mahakim.ma/middleware/api/SuiviDossiers/ListeJuridictions2Instance?CodeDossier=(juridiction) (ID : CA)
# etape 3 : choose the court
# etape 4 : https://www.mahakim.ma/middleware/api/SuiviDossiers/Juridictions1Instance?CodeDossier=(juridiction)&idJuridiction2Instance= (ID : TPI)
# etape 5 out put : https://www.mahakim.ma/middleware/api/SuiviDossiers/CarteDossier?numeroCompletDossier=(Referencecomplet)&idjuridiction=(ID TPI) ? ID file
# etape 6 : https://www.mahakim.ma/middleware/api/SuiviDossiers/ListeDicisions?idDossier=(ID File)&typeaffaire=DP 



import requests
import pandas as pd
from datetime import datetime
import numpy as np
    

def ctx (year,juridict,reference,idCA,idTPI) :
    

    api = "https://www.mahakim.ma/middleware/api/SuiviDossiers/"

    link2 = api + "ListeJuridictions2Instance?CodeDossier=" + str(juridict)

    etape1 = requests.get(link2,verify = False)


    CA = etape1.json()
    coursA = CA.get('data',[])
    coursA = pd.DataFrame(coursA, columns=['idJuridiction', 'nomJuridiction'])
    coursA = coursA.to_numpy()
    #print (coursA)
    IDjuridiction = idCA



    link3 = api+"Juridictions1Instance?CodeDossier="+str(juridict)+"&idJuridiction2Instance="+str(IDjuridiction)

    etape4 = requests.get(link3,verify=False)
    TPI = etape4.json()                                                                        

    Trib = TPI.get('data',[])
    Trib = pd.DataFrame(Trib, columns=['idJuridiction', 'nomJuridiction'])
    Trib = Trib.to_numpy()
    #print (Trib)
    IDtribunal = idTPI


    link4 = api +"CarteDossier?numeroCompletDossier="+str(year)+str(juridict)+str(reference)+"&idjuridiction="+str(IDtribunal)
    etape5 = requests.get(link4,verify=False)
    mapfile = etape5.json()


    claimfile = mapfile.get('data',[])

    Idfile = claimfile['idDossierCivil']
    typeaffaire = claimfile['affaire']

    link5 = api+"ListeDicisions?idDossier="+str(Idfile)+"&typeaffaire="+str(typeaffaire)
    etape6 = requests.get(link5,verify=False)
    steps = etape6.json()

    stepp = steps.get('data', [])

    finalstep = stepp[0]
    decision = finalstep['contenuDecision']
    nextdate = finalstep['dateTimeNextAudience']
    datefinal = finalstep['dateTimeDecision']
    datefinal = datefinal[:10]
    dateformat = "%d/%m/%Y"
    datefinale=datetime.strptime(datefinal,dateformat)
    
    link6 = api + "ListeParties?idDossier=" + str(Idfile)+"&typeaffaire="+str(typeaffaire)
    etape7 = requests.get(link6,verify=False)
    parts = etape7.json()
    
    nomPrenomPartie = [entry['nomPrenomPartie'] for entry in parts['data']]
    rolePartie = [entry['rolePartie'] for entry in parts['data']]
    codeTypePersonne = ["personne morale" if entry['codeTypePersonne'] == "PM" else "personne physique" for entry in parts['data']]

    listedesparties = pd.DataFrame({'nomPrenomPartie': nomPrenomPartie, 'rolePartie': rolePartie, 'codeTypePersonne': codeTypePersonne})
       
    if nextdate=='' :
        return decision ,datefinale,listedesparties
                
    else :
            return decision, nextdate, listedesparties
              
listdes= pd.read_excel('list.xlsx')

listdes[['Output1', 'Output2','typess']] = listdes.apply(lambda row: pd.Series(ctx(row['year'], row['juridiction'], row['reference'],row['CAcode'],row['TPIcode'])), axis=1)
listdes.to_excel('lista.xlsx', index=False)

