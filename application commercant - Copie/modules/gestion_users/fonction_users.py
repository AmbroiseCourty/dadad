import pandas as pd
import hashlib
import os
from colorama import init, Fore, Style
from requests import session
from modules.paths import USERS_CSV_FILE, API_FILE, FONCTION_PROD_FILE, TRI_FILE, FONCTION_USERS_FILE, HASH_SESSIONS_FILE, ROCKYOU_FILE, PATHS_FILE 
from modules.gestion_users.fonction_users import *
from modules.gestion_users.hash_sessions import * 
from modules.gestion_users.hash_sessions import sessions
from modules.gestion_prod.fonction_prod import *
from modules.password_comp.api import *
from modules.password_comp.rockyou import *
from main import call_interface


init(autoreset=True)


def add_users():
    print(Fore.YELLOW + "Formulaire d'ajout d'un nouvel utilisateur\n")
    username = input(Fore.RED + " Veuillez entrer le nom d'utilisateur :\n")
    password = hash(input(Fore.RED + "Veuillez entrer le mot de passe :\n"))
    
    df = pd.read_csv(USERS_CSV_FILE)
    if username == "admin":
        print("---------------------------------------")
        print("Vous ne pouvez pas créer un utilisateur avec le nom admin")
        print("---------------------------------------")
        return 
    # if is_in_rockyou(password['hash']):
    #     print("---------------------------------------")
    #     print("Mot de passe compromis, veuillez choisir un autre mot de passe")
    #     print("---------------------------------------")
    #     return
    if username in df['username'].values:
        print(Fore.BLUE +"---------------------------------------")
        print(Fore.BLUE +"L'utilisateur existe déjà")
        print(Fore.BLUE +"---------------------------------------")
        return add_users()
    else :
        try:
            with open(USERS_CSV_FILE, "a") as files:
                print("Ajout de l'utilisateur dans la base de données ...")
                files.write(f"{username},{password['hash']},{password['salt']}\n") 
        except PermissionError:
            print("Permissions insuffisantes pour ouvrir le fichier")
        except Exception as e:
            print(f"Erreur inconnue : {e}")

def delete_users():
    name = str(input("Veuillez entrer le nom de l'utilisateur à supprimer : "))
    print("Ouverture de la base de données ...")
    if name not in open(USERS_CSV_FILE).read():
        print("---------------------------------------")
        print("L'utilisateur n'existe pas")
        print("---------------------------------------")
        print("Fermeture de la base de données ...")
        return
    try:
        with open(USERS_CSV_FILE, 'r') as file:
            content = file.readlines()
        with open(USERS_CSV_FILE, 'w') as file:
            for line in content:
                if not line.startswith(name + ','):
                    file.write(line)
    except FileExistsError:
        print("Le fichier n'a pas été trouvé")
    except PermissionError:
        print("Les droits ne sont pas suffisant pour ouvrir le fichier")
    print("---------------------------------------")
    print("Utilisateur supprimé !!")
    print("---------------------------------------")
    print("Fermeture de la base de données ...")


def update_users(username):
    print("Préparation de la mise à jour des utilisateurs...")
    name = input("Veuillez entrer votre nom d'utilisateur : ")

    # Vérifier si l'utilisateur est connecté et si le nom d'utilisateur correspond
    if name != username or name not in sessions:
        print("---------------------------------------")
        print("Vous ne pouvez modifier que votre propre mot de passe")
        print("---------------------------------------")
        return

    password = input("Veuillez entrer le nouveau mot de passe : ")
    print("Ouverture de la base de données ...")
    

    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv(USERS_CSV_FILE)

    # Vérifier si l'utilisateur existe
    if name not in df['username'].values:
        print("---------------------------------------")
        print("L'utilisateur n'existe pas")
        print("---------------------------------------")
        print("Fermeture de la base de données ...")
        return

    # Générer un nouveau sel et hacher le mot de passe
    hashed_password_data = hash(password)
    hashed_password = hashed_password_data["hash"]
    salt = hashed_password_data["salt"]

    # Mettre à jour le mot de passe et le sel de l'utilisateur
    df.loc[df['username'] == name, 'password'] = hashed_password
    df.loc[df['username'] == name, 'salt'] = salt

    # Sauvegarder les modifications dans le fichier CSV
    df.to_csv(USERS_CSV_FILE, index=False)

    print("---------------------------------------")
    print("Mot de passe mis à jour !!")
    print("---------------------------------------")
    print("Fermeture de la base de données ...")

def afficher_users():
    try:
        print("____________________________")
        print("Affichage des identifiants :")
        print("----------------------------")
        users = pd.read_csv(USERS_CSV_FILE)
        print(users)
    except PermissionError:
        print("Permissions insuffisantes pour ouvrir le fichier")
    except Exception as e:
        print(f"Erreur inconnue : {e}")


def update_password_comprised(username):
    print("Préparation de la mise à jour des utilisateurs...")
    name = input("Veuillez entrer votre nom d'utilisateur : ")

    # Vérifier si l'utilisateur est connecté et si le nom d'utilisateur correspond
    if name != username or name not in sessions :
        print("---------------------------------------")
        print("Vous ne pouvez modifier que votre propre mot de passe")
        print("---------------------------------------")
        return update_password_comprised(username)
    
    
    password = input("Veuillez entrer le nouveau mot de passe : ")
    print("Ouverture de la base de données ...")

    if check_password(password):
        print("---------------------------------------")
        print("Mot de passe compromis, veuillez choisir un autre mot de passe")
        print("---------------------------------------")
        return update_password_comprised(username)
        

    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv(USERS_CSV_FILE)

    # Vérifier si l'utilisateur existe
    if name not in df['username'].values :
        print("---------------------------------------")
        print("L'utilisateur n'existe pas")
        print("---------------------------------------")
        
        return update_password_comprised(username)

    # Générer un nouveau sel et hacher le mot de passe
    hashed_password_data = hash(password)
    hashed_password = hashed_password_data["hash"]
    salt = hashed_password_data["salt"]

    # Mettre à jour le mot de passe et le sel de l'utilisateur
    df.loc[df['username'] == name, 'password'] = hashed_password
    df.loc[df['username'] == name, 'salt'] = salt

    # Sauvegarder les modifications dans le fichier CSV
    df.to_csv(USERS_CSV_FILE, index=False)

    print("---------------------------------------")
    print("Mot de passe mis à jour !!")
    print("---------------------------------------")
    print("Retour au menu !!")
    return call_interface()