import pandas as pd
import hashlib
import os
from colorama import init, Fore, Style
from modules.paths import USERS_CSV_FILE, API_FILE, FONCTION_PROD_FILE, TRI_FILE, FONCTION_USERS_FILE, HASH_SESSIONS_FILE, ROCKYOU_FILE, PATHS_FILE
from modules.gestion_users.fonction_users import *
from modules.gestion_users.hash_sessions import *
from modules.gestion_prod.fonction_prod import *
from modules.password_comp.api import *
from modules.password_comp.rockyou import *

init(autoreset=True)


def get_inventory_file(user):
    if user in open(USERS_CSV_FILE).read():
        inventory_file = os.path.join('data','users',f'{user}.csv')
        if not os.path.exists(inventory_file):
            pd.DataFrame(columns=["Nom", "Quantité", "Prix"]).to_csv(inventory_file, index=False)
        return inventory_file

def afficher_inventory_csv(user):
    inventory_file = get_inventory_file(user)
    try:
        print("_______________________")
        print("Affichage des produits:")
        print("-----------------------")
        products = pd.read_csv(inventory_file)
        if products.empty:
            print(Fore.GREEN + "Votre inventaire est vide !!!\n")
        else:
            print(products)
    except PermissionError:
        print("Permissions insuffisantes pour ouvrir le fichier\n")
    except Exception as e:
        print(f"Erreur inconnue : {e}\n")

def add_to_inventory(user):
    while True:
        name = input(Fore.GREEN + "Veuillez entrer le nom du produit (lettres uniquement) : \n")
        if name.isalpha():
            break
        print(Fore.GREEN + "Nom invalide. Veuillez entrer uniquement des lettres\n.")

    while True:
        try:
            quantity = int(input(Fore.GREEN + "Veuillez entrer la quantité du produit (nombre entier positif) : \n"))
            if quantity > 0:
                break
            
            else:
                print(Fore.GREEN + "Quantité invalide. Veuillez entrer un nombre entier positif.\n")
        except ValueError:
            print(Fore.GREEN + "Quantité invalide. Veuillez entrer un nombre entier positif.\n")

    while True:
        try:
            prix = float(input(Fore.GREEN + "Veuillez entrer le prix du produit (nombre positif) : \n"))
            if prix > 0:
                break
            else:
                print(Fore.GREEN + "Prix invalide. Veuillez entrer un nombre positif.\n")
        except ValueError:
            print(Fore.GREEN + "Prix invalide. Veuillez entrer un nombre positif.\n")

    # Ouverture de l'inventaire
    print(Fore.YELLOW + "Ouverture de l'inventaire\n")
    inventory_file = get_inventory_file(user)
    # récupération de l'inventaire existant de l'utilisateur
    try:
        try:
            inventory = pd.read_csv(inventory_file)
        except FileNotFoundError as e:
            inventory = pd.DataFrame(columns=["Nom","Quantité","Prix"])
        # ajouter l'utilisateur
        new_product = pd.DataFrame({"Nom" : [name], "Quantité" : [quantity], "Prix" : [prix]})
        inventory = pd.concat([inventory, new_product], ignore_index=True)
        # mettre à jour le fichier
        inventory.to_csv(inventory_file, index=False)
    except PermissionError as e:
        print(f"Vous ne disposez pas des droits suffisants : {e}\n")
    except Exception as e:
        print(f"Erreur innatendu : {e}\n")

def delete_from_inventory(user):
    inventory_file = get_inventory_file(user)
    name = input("Veuillez entrer le nom du produit à supprimer : \n")

    
    df = pd.read_csv(inventory_file)

    
    if name not in df['Nom'].values:
        print("---------------------------------------")
        print("Le produit n'existe pas")
        print("---------------------------------------")
        print("Fermeture de l'inventaire ...")
        return

    # Supprimer le produit
    df = df[df['Nom'] != name]

    
    df.to_csv(inventory_file, index=False)

    print("---------------------------------------")
    print("Produit supprimé !!")
    print("---------------------------------------")
    print("Fermeture de l'inventaire")
    



 
def recherche_pandas(user):
    inventory_file = get_inventory_file(user)
    nom = input("Nom du produit à rechercher : \n").lower()
    
    df = pd.read_csv(inventory_file)

    # Utiliser une comparaison stricte pour une recherche exacte
    result = df[df['Nom'].str.lower() == nom]

    if not result.empty:
        print("--------------------------------")
        print("Résultat de la recherche :\n")
        print("--------------------------------")
        print(result[['Nom', 'Quantité', 'Prix']])
    else:
        print("Produit non trouvé !! ")


def afficher_tri_pandas(nom_fichier):
    """
    Demande à l'utilisateur quel type de tri il souhaite, puis trie le DataFrame en conséquence.

    :param df: DataFrame pandas à trier
    :return: DataFrame trié
    """
    df = pd.read_csv(nom_fichier)

    print("Choisissez le type de tri:\n")
    print("1. Tri par ordre alphabétique (Nom)\n")
    print("2. Tri par quantité croissante\n")
    print("3. Tri par prix croissant\n")
    
    choix = input("Entrez le numéro du tri souhaité:\n ")

    if choix == '1':
        df = df.sort_values(by='Nom', ascending=True)
    elif choix == '2':
        df = df.sort_values(by='Quantité', ascending=True)
    elif choix == '3':
        df = df.sort_values(by='Prix', ascending=True)
    else:
        print("Choix invalide. Aucun tri effectué.\n")
    
    print(df)
    return df