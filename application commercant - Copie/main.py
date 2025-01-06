import pandas as pd 
import hashlib
import os
import tkinter as tk 
from colorama import init, Fore, Style
from modules.paths import USERS_CSV_FILE, API_FILE, FONCTION_PROD_FILE, TRI_FILE, FONCTION_USERS_FILE, HASH_SESSIONS_FILE, ROCKYOU_FILE, PATHS_FILE
from modules.gestion_users.fonction_users import *
from modules.gestion_users.hash_sessions import *
from modules.gestion_prod.fonction_prod import *
from modules.password_comp.api import *
from modules.password_comp.rockyou import *





init(autoreset=True)

def call_interface():
    print(Fore.CYAN + Style.BRIGHT + "\nBienvenue dans l'interface de gestion de l'inventaire et des utilisateurs\n")
    register = input(Fore.YELLOW + "Voulez-vous vous inscrire ? (Oui : 1, J'ai déjà un compte : 2) :\n ")
    if register == "1":
        if add_users():
            print(Fore.CYAN + "Votre compte a bien été créé !\n")
    
    elif register == "2":
        user = input(Fore.YELLOW + "Veuillez entrer votre nom d'utilisateur :\n ")
        password = input(Fore.YELLOW + "Veuillez entrer votre mot de passe :\n ")
        
        if login(user, password):
            if check_password(password) == True:
                print(Fore.RED + "Mot de passe compromis, veuillez changer de mot de passe !!")
                return update_password_comprised(user)
            admin = user == "admin" and password == "admin"
            choose = 1
            while choose != 0:
                print(Fore.GREEN + Style.BRIGHT + "\n---------")
                print(Fore.GREEN + Style.BRIGHT + "INVENTAIRE")
                print(Fore.GREEN + Style.BRIGHT + "---------")
                print(Fore.BLUE + "1 - Afficher l'inventaire ; 2 - Ajouter à l'inventaire ; 3 - Supprimer de l'inventaire ; 4 - Trier l'inventaire ; 5 - Recherche un produit")
                print(Fore.GREEN + Style.BRIGHT + "---------")
                print(Fore.GREEN + Style.BRIGHT + "SECURITE")
                print(Fore.GREEN + Style.BRIGHT + "---------")
                print(Fore.BLUE + "6 - Vérification de mot de passe ; 7 - Alerte de sécurité")
                
                if admin:
                    print(Fore.MAGENTA + Style.BRIGHT + "-----")
                    print(Fore.MAGENTA + Style.BRIGHT + "ADMIN")
                    print(Fore.MAGENTA + Style.BRIGHT + "-----")
                    print(Fore.RED + "8 - Afficher les utilisateurs ; 9 - Ajouter un utilisateur ; 10 - Supprimer un utilisateur")
                    
                print(Fore.GREEN + Style.BRIGHT + "-----------------------")
                print(Fore.GREEN + Style.BRIGHT + "AUTRES")
                print(Fore.GREEN + Style.BRIGHT + "-----------------------")
                print(Fore.BLUE + "11 - Mettre à jour un utilisateur ; 12- Quitter l'interface")
                print(Fore.GREEN + Style.BRIGHT + "-----------------------")
                
                choose = input(Fore.YELLOW + "Veuillez choisir une méthode : \n")
                choose = int(choose)
                if choose == 1:
                    afficher_inventory_csv(user)
                elif choose == 2:
                    add_to_inventory(user)
                elif choose == 3:
                    delete_from_inventory(user)
                elif choose == 4:
                    afficher_tri_pandas(get_inventory_file(user))
                elif choose == 5:
                    recherche_pandas(user)
                elif choose == 6:
                    ask_password()
                elif choose == 7:
                    pass
                elif admin:
                    if choose == 8:
                        afficher_users()
                    elif choose == 9:
                        add_users()
                    elif choose == 10:
                        delete_users()
                if choose == 11:
                    update_users()
                elif choose == 12:
                    print(Fore.CYAN + "Merci d'avoir utilisé l'interface. Au revoir!\n")
                    break

if __name__ == "__main__":
    call_interface()
    
    


