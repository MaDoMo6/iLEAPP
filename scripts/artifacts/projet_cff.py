print("hello world")


# Artifact declaration, must be first
__artifacts_v2__ = {
    "parseSBBMobileDB": { # Same name as the main function
        "name": "SBB Mobile", # Title used in html report sidebar
        "description": "Permet de recueillir les données de l'application SBB Mobile",
        "author": "",
        "version": "1.0",
        "date": "2024-11-19",
        "requirements": "none",
        "category": "SBBMobile", # Category used in html report sidebar and also in selection menu...
        "notes": "",
        "paths": (
            '*/Documents/ch.sbb.coredata.reisendeoptionen.sqlite*',
            '*/Documents/ch.sbb.coredata.searchhistory.sqlite*',
            '*/ch.sbb.coredata.travelbuddy.trips.sqlite*',
            '*/SbbMobile.db'
        ), # list of paths containing useful information        
        "function": "parseSBBMobileDB" # Function started by the module
    }
}

from pathlib import Path
from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, open_sqlite_db_readonly



def parseSBBMobileDB(files_found, report_folder, seeker, wrap_text, time_offset) -> None:
    print(f"Files matching the paths pattern: {files_found}") 
    
    if not files_found:
        logfunc('No file found within SBB Mobile App folders, finishing module')
        return None

#reisendeoptionen.sqlite
    db_reisendeoptionen = None
    for file in files_found:
        file = Path(file)
        if file.name == "ch.sbb.coredata.reisendeoptionen.sqlite":
            db_reisendeoptionen = file
            print(f"DB file is {db_reisendeoptionen}") 
            break

    if db_reisendeoptionen is None:
        logfunc('Main database file not found, finishing module')
        return None

    # opening database file
    str_db_reisendeoptionen = str(db_reisendeoptionen)
    try:
        with open_sqlite_db_readonly(str_db_reisendeoptionen) as db:
            cursor = db.cursor()

        #première requete
            cursor.execute('''
            SELECT
                ZREISENDEPROFILE AS 'Nombre de profils', 
                ZNAME AS 'Nom', 
                ZCONTRACTSTATE AS 'Status', 
                ZTRAVELCLASS AS 'Classe', 
                ZVALIDFROM AS 'Début', 
                ZVALIDTO AS 'Echéance' 
            
            FROM ZABO

            ''')
            all_rows_abo = cursor.fetchall()

        #deuxième requete
            cursor.execute('''
            SELECT 
            
                ZNAME AS 'Nom', 
                ZVORNAME AS 'Prénom', 
                ZGEBURTSDATUM AS 'Date de naissance', 
                datetime(ZLASTSYNC + (strftime('%s', '2001-01-01')), 'unixepoch' )
            
            FROM ZREISENDEPROFILE

            ''')
            all_rows_profils = cursor.fetchall()

    except Exception as e:
        logfunc(f"Error reading database: {str(e)}")
        return None
    
    if len(all_rows_abo) == 0:
        logfunc('No data found, finishing module')
        return None



#searchhistory.sqlite
    db_searchhistory = None
    for file in files_found:
        file = Path(file)
        if file.name == "ch.sbb.coredata.searchhistory.sqlite":
            db_searchhistory = file
            print(f"DB file is {db_searchhistory}") 
            break

    if db_searchhistory is None:
        logfunc('Main database file not found, finishing module')
        return None

    # opening database file
    str_db_searchhistory = str(db_searchhistory)
    try:
        with open_sqlite_db_readonly(str_db_searchhistory) as db:
            cursor = db.cursor()

            cursor.execute('''
            SELECT 
                ZLON AS 'Longitude', 
                ZLAT AS 'Latitude', 
                ZFROM AS 'De', 
                ZTO AS 'A', 
                datetime(ZTIMESTAMP/ 1000, 'unixepoch') AS 'Timestamp' 
            FROM ZSEARCHRESULT

            ''')
            all_rows_recherche = cursor.fetchall()

    except Exception as e:
        logfunc(f"Error reading database: {str(e)}")
        return None
    
    if len(all_rows_abo) == 0:
        logfunc('No data found, finishing module')
        return None


#travelbuddy.trips.sqlite
    db_travelbuddy = None
    for file in files_found:
        file = Path(file)
        if file.name == "ch.sbb.coredata.travelbuddy.trips.sqlite":
            db_travelbuddy = file
            print(f"DB file is {db_travelbuddy}") 
            break

    if db_travelbuddy is None:
        logfunc('Main database file not found, finishing module')
        return None

    # opening database file
    str_db_travelbuddy = str(db_travelbuddy)
    try:
        with open_sqlite_db_readonly(str_db_travelbuddy) as db:
            cursor = db.cursor()

            cursor.execute('''
            SELECT 
                ZAPPID AS 'App ID', 
                ZCONNECTIONJSONDATA AS 'JSON', 
                ZSWISSPASSUSERID AS 'Swisspass User ID' 
            FROM ZLOCALTRIPCACHE

            ''')
            all_rows_travelbuddy = cursor.fetchall()


            cursor.execute('''
           SELECT 
                ZAPPID AS 'App ID', 
                ZMYJOURNEYID AS 'My Journey ID', 
                ZSUBSCRIPTIONID AS 'Subscription ID', 
                datetime(ZLASTCHANGEDATE + (strftime('%s', '2001-01-01')), 'unixepoch' ) AS 'Last Change Date' 
            FROM ZTRAVELBUDDYTRIP

            ''')
            all_rows_travelbuddy2 = cursor.fetchall()

    except Exception as e:
        logfunc(f"Error reading database: {str(e)}")
        return None

    if len(all_rows_abo) == 0:
        logfunc('No data found, finishing module')
        return None


#sbbmobile.db
    db_sbbmobiledb = None
    for file in files_found:
        file = Path(file)
        if file.name == "SbbMobile.db":
            db_sbbmobiledb = file
            print(f"DB file is {db_sbbmobiledb}") 
            break

    if db_sbbmobiledb is None:
        logfunc('Main database file not found, finishing module')
        return None

    # opening database file
    str_db_sbbmobiledb = str(db_sbbmobiledb)
    try:
        with open_sqlite_db_readonly(str_db_sbbmobiledb) as db:
            cursor = db.cursor()

            cursor.execute('''
            SELECT 
                normalized_name AS 'Saisie', 
                name AS 'Recherche', 
                latitude AS 'Latitude', 
                longitude AS 'Longitude', 
                datetime(timestamp, 'unixepoch') AS 'Timestamp', 
                type AS 'Type' 
            FROM StandortVerlauf

            ''')
            all_rows_standortverlauf = cursor.fetchall()

    except Exception as e:
        logfunc(f"Error reading database: {str(e)}")
        return None

    if len(all_rows_abo) == 0:
        logfunc('No data found, finishing module')
        return None


#____________________________________________________

    #création du rapport HTML
    report = ArtifactHtmlReport('SBB Mobile - AMSA')

 # 1er page HTML: Abonnements
    description_abo = 'Les information sur l\'abonnement'
    report.start_artifact_report(report_folder, 'Abonnements', description_abo)
    report.add_script()

    data_headers_abo = ('Nombre de profils', 'Nom', 'Status', 'Classe', 'Début', 'Echéance')
    report.write_artifact_data_table(data_headers_abo, all_rows_abo, str_db_reisendeoptionen)
    report.end_artifact_report()


 # 2ème page HTML: Profil des voyageurs
    description_profils = 'Les information sur les voyageurs'
    report.start_artifact_report(report_folder, 'Profil des voyageurs', description_profils)
    report.add_script()

    data_headers_profils = ('Nom', 'Prenom', 'Date de naissance', 'Last Synchronisation')
    report.write_artifact_data_table(data_headers_profils, all_rows_profils, str_db_reisendeoptionen)
    report.end_artifact_report()


 # 3ème page HTML: Résultats des recherches
    description_recherche = 'Résultats des recherches'
    report.start_artifact_report(report_folder, 'Recherches', description_recherche)
    report.add_script()

    data_headers_recherche = ('Longitude', 'Latitude', 'De', 'A', 'Timestamp')
    report.write_artifact_data_table(data_headers_recherche, all_rows_recherche, str_db_searchhistory)
    report.end_artifact_report()


 # 4ème page HTML: Résultats des recherches
    description_travelbuddy = 'Voyages enregistrés'
    report.start_artifact_report(report_folder, 'Travelbuddy', description_travelbuddy)
    report.add_script()

    data_headers_travelbuddy = ('App ID', 'JSON', 'Swisspass User ID')
    report.write_artifact_data_table(data_headers_travelbuddy, all_rows_travelbuddy, str_db_travelbuddy)
    report.end_artifact_report()


# 5ème page HTML: Résultats des recherches
    description_traveluddy2 = 'Voyages enregistrés'
    report.start_artifact_report(report_folder, 'Travelbuddy Voyges', description_traveluddy2)
    report.add_script()

    data_headers_travelbuddy2 = ('App ID', 'My Journey ID', 'Subscription ID', 'Last Change Date')
    report.write_artifact_data_table(data_headers_travelbuddy2, all_rows_travelbuddy2, str_db_travelbuddy)
    report.end_artifact_report()


 # 6ème page HTML: Résultats des recherches
    description_standortverlauf = 'Standort Verlauf'
    report.start_artifact_report(report_folder, 'Standort Verlauf', description_standortverlauf)
    report.add_script()

    data_headers_standortverlauf = ('Saisie', 'Recherche', 'Latitude', 'Longitude', 'Timestamp', 'Type')
    report.write_artifact_data_table(data_headers_standortverlauf, all_rows_standortverlauf, str_db_sbbmobiledb)
    report.end_artifact_report()





#génération du fichier tsv
    tsvname = f'SBB Mobile'
    tsv(report_folder, data_headers_abo, all_rows_abo, tsvname)

    tlactivity = f'SBB Mobile'
    timeline(report_folder, tlactivity, all_rows_abo, data_headers_abo)

    return None




