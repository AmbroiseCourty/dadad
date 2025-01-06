import pandas as pd
import hashlib
import os
import chardet
from colorama import init, Fore, Style
from modules.paths import USERS_CSV_FILE, API_FILE, FONCTION_PROD_FILE, TRI_FILE, FONCTION_USERS_FILE, HASH_SESSIONS_FILE,  PATHS_FILE, ROCKYOU_FILE, HASH_CSV_FILE
from modules.gestion_users.fonction_users import *
from modules.gestion_users.hash_sessions import *
from modules.gestion_prod.fonction_prod import *
from modules.password_comp.api import *
from modules.password_comp.rockyou import *

init(autoreset=True)

#
#
#
#
#
#Nous n'avons pas eu le temps de finir l'intégration de la fonctionnalité de vérification de mot de passe compromis via rockyou.
#
#
#
#
#

sample = 100000

def hash_rockyou():
    try:
        with open(ROCKYOU_FILE, 'rb') as file:
            raw_data = file.read(sample)
            result = chardet.detect(raw_data)
            encoding = result['encoding']
        write_file = open(HASH_CSV_FILE, 'w', encoding=encoding,errors="replace")
        with open(ROCKYOU_FILE, encoding=encoding, errors="replace") as file:
            for line in file:
                hash_object = hashlib.sha256()
                hash_object.update(line.encode())
                write_file.write(hash_object.hexdigest() + "\n")
        write_file.close()                          
    except FileNotFoundError as e:
        print(f"Fichier non trouvé : {e}")
    except PermissionError as e:
        print(f"Vous n'avez pas les doits : {e}")
    except Exception as e:
        print(f"Erreur inconnue : {e}")

def is_in_rockyou(password)->bool:
    try:
        with open(HASH_CSV_FILE, 'rb') as file:
            raw_data = file.read(sample)
            result = chardet.detect(raw_data)
            encoding = result['encoding']
        with open(HASH_CSV_FILE, encoding=encoding, errors='replace') as file:
            for line in file:
                hash_object = hashlib.sha256()
                hash_object.update(password.encode())
                if hash_object.hexdigest()==line.strip():
                    print("Hit")
                    return True
    except FileNotFoundError as e:
        print(f"Le fichier n'a pas été trouvé : {e}")
    except PermissionError as e:
        print(f"Vos droits ne sont pas suffisants : {e}")
    except Exception as e:
        print(f"Erreur inconnue : {e}")