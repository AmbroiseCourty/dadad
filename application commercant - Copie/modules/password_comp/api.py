import pandas as pd
import hashlib
import os
import requests
from colorama import init, Fore, Style
from modules.paths import USERS_CSV_FILE, API_FILE, FONCTION_PROD_FILE, TRI_FILE, FONCTION_USERS_FILE, HASH_SESSIONS_FILE, PATHS_FILE
from modules.gestion_users.fonction_users import *
from modules.gestion_users.hash_sessions import *
from modules.gestion_prod.fonction_prod import *
from modules.password_comp.api import *
from modules.password_comp.rockyou import *

init(autoreset=True)

def check_password(password):
    hash_object = hashlib.sha1()
    hash_object.update(password.encode())
    hash = hash_object.hexdigest().upper()
    prefix = hash[:5]
    suffix = hash[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        response = requests.get(url)
    except requests.exceptions.HTTPError as e:
        print(f"Erreur HTTP : {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Erreur de connexion : {e}")
    except requests.exceptions.Timeout as e:
        print(f"Requête expirée : {e}")
    except requests.exceptions.RequestException as e:
        print(f"Une erreur est survenue : {e}")
    if suffix in response.text:
            return True
            
    else:
        return False

def ask_password():
    password = str(input("Veuillez entrer un mot de passe à tester : "))
    print("Lancement de la vérification du mot de passe...")
    if check_password(password):
        print("Ton mot de passe n'est pas sécurisé !")
    else:
        print("Ton mot de passe est sécurisé pour le moment...")