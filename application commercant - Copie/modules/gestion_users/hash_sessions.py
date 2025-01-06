import pandas as pd
import hashlib
import os
import uuid
from colorama import init, Fore, Style
from modules.gestion_prod.fonction_prod import get_inventory_file
from modules.paths import USERS_CSV_FILE, API_FILE, FONCTION_PROD_FILE, TRI_FILE, FONCTION_USERS_FILE, HASH_SESSIONS_FILE, ROCKYOU_FILE, PATHS_FILE
from modules.gestion_users.fonction_users import *
from modules.gestion_users.hash_sessions import *
from modules.gestion_prod.fonction_prod import *
from modules.password_comp.api import *
from modules.password_comp.rockyou import *

init(autoreset=True)

sessions = {}

def afficher_users():
    try:
        print("----------------------------")
        print("Affichage des identifiants :")
        print("----------------------------")
        users = pd.read_csv(USERS_CSV_FILE)
        print(users)
    except PermissionError:
        print(Fore.RED + Style.BRIGHT + "Permissions insuffisantes pour ouvrir le fichier")
    except Exception as e:
        print(Fore.RED + Style.BRIGHT +f"Erreur inconnue : {e}")

def hash(password)->dict:
    salt = os.urandom(16)
    hash_object = hashlib.sha256()
    hash_object.update(salt+password.encode())
    hashed_password = hash_object.hexdigest()
    return {"salt" : salt.hex(), "hash" : hashed_password}

def verify_users(password, hashed_password, salt) -> bool:
    salt_bytes = bytes.fromhex(salt)
    hash_object = hashlib.sha256()
    hash_object.update(salt_bytes + password.encode())
    return hash_object.hexdigest() == hashed_password




def check_users_file():
    try:
        users = pd.read_csv(USERS_CSV_FILE)
        if 'username' not in users.columns or 'password' not in users.columns or 'salt' not in users.columns:
            raise ValueError("Le fichier users.csv doit contenir les colonnes 'username', 'password' et 'salt'.")
    except pd.errors.ParserError as e:
        print(f"Erreur de format dans le fichier users.csv : {e}")
        return False
    return True



def login(user, password):
    get_inventory_file(user)
    if not os.path.exists(USERS_CSV_FILE):
        print("Le fichier des utilisateurs n'existe pas.")
        return False
    if not check_users_file():
        return False
    users = pd.read_csv(USERS_CSV_FILE)
    user_row = users[users['username'] == user]
    if not user_row.empty and verify_users(password, user_row.iloc[0]['password'], user_row.iloc[0]['salt']):
        user_id = str(uuid.uuid4())
        sessions[user] = user_id
        print(f"Utilisateur {user} connecté")
        return True
    if user_row.empty == check_password(password):
        print("Mot de passe incorrect.")
        return False
    else:
        print("Identifiant ou mot de passe incorrect.")
        return False

def logout(user):
    if user in sessions:
        del sessions[user]
        print(f"Utilisateur {user} déconnecté.")
    else:
        print(f"L'utilisateur {user} n'est pas connecté.")

def is_logged_in(user):
    return sessions.get(user, False)