import pandas as pd
import hashlib
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from colorama import init, Fore, Style
from modules.paths import USERS_CSV_FILE, API_FILE, FONCTION_PROD_FILE, TRI_FILE, FONCTION_USERS_FILE, HASH_SESSIONS_FILE, ROCKYOU_FILE, PATHS_FILE
from modules.gestion_users.fonction_users import *
from modules.gestion_users.hash_sessions import *
from modules.gestion_prod.fonction_prod import *
from modules.password_comp.api import check_password
from modules.password_comp.rockyou import *

init(autoreset=True)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interface de Gestion")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")
        self.current_user = None
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")
        self.style.configure("TEntry", font=("Helvetica", 12))
        self.show_login_page()

    def show_login_page(self):
        self.clear_frame()

        label_welcome = ttk.Label(self, text="Bienvenue dans l'interface de gestion de l'inventaire")
        label_welcome.pack(pady=10)

        label_username = ttk.Label(self, text="Nom d'utilisateur")
        label_username.pack(pady=5)
        self.entry_username = ttk.Entry(self)
        self.entry_username.pack(pady=5)

        label_password = ttk.Label(self, text="Mot de passe")
        label_password.pack(pady=5)
        self.entry_password = ttk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        button_login = ttk.Button(self, text="Connexion", command=self.login)
        button_login.pack(pady=5)

        button_register = ttk.Button(self, text="Inscription", command=self.register)
        button_register.pack(pady=5)

    def show_inventory_page(self):
        self.clear_frame()

        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        inventory_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Inventaire", menu=inventory_menu)
        inventory_menu.add_command(label="Afficher l'inventaire", command=self.load_inventory)
        inventory_menu.add_command(label="Ajouter un produit", command=self.add_to_inventory)
        inventory_menu.add_command(label="Supprimer un produit", command=self.delete_from_inventory)
        inventory_menu.add_command(label="Modifier un produit", command=self.modify_product)
        inventory_menu.add_command(label="Rechercher un produit", command=self.recherche_pandas)
        inventory_menu.add_command(label="Trier l'inventaire", command=self.afficher_tri_pandas)
        inventory_menu.add_command(label="Déconnexion", command=self.logout)
        
        user_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Utilisateur", menu=user_menu)
        user_menu.add_command(label="Mettre à jour mon compte", command=self.update_user)

        if self.current_user == "admin":
            admin_menu = tk.Menu(menu_bar, tearoff=0)
            menu_bar.add_cascade(label="Admin", menu=admin_menu)
            admin_menu.add_command(label="Afficher les utilisateurs", command=self.afficher_users)
            admin_menu.add_command(label="Ajouter un utilisateur", command=self.add_users)
            admin_menu.add_command(label="Supprimer un utilisateur", command=self.delete_users)

        label_inventory = ttk.Label(self, text="Inventaire")
        label_inventory.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("Nom", "Quantité", "Prix"), show="headings")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Quantité", text="Quantité")
        self.tree.heading("Prix", text="Prix")
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)

        self.load_inventory()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        if check_password(password):
            if messagebox.askyesno("Mot de passe compromis", "Votre mot de passe est compromis. Voulez-vous le changer ?"):
                self.change_password(username)
                return

        if login(username, password):
            self.current_user = username
            self.show_inventory_page()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

    
    def logout(self):
        self.current_user = None
        for widget in self.winfo_children():
            widget.destroy()
        self.show_login_page()
        
        
    def change_password(self, username):
        while True:
            new_password = simpledialog.askstring("Nouveau mot de passe", "Veuillez entrer le nouveau mot de passe :", show='*')
            if not new_password:
                messagebox.showerror("Erreur", "Le mot de passe ne peut pas être vide")
                continue

            if check_password(new_password):
                messagebox.showerror("Erreur", "Votre nouveau mot de passe est compromis. Veuillez en choisir un autre.")
                continue

            df = pd.read_csv(USERS_CSV_FILE)
            hashed_password_data = hash(new_password)
            df.loc[df['username'] == username, 'password'] = hashed_password_data['hash']
            df.loc[df['username'] == username, 'salt'] = hashed_password_data['salt']
            df.to_csv(USERS_CSV_FILE, index=False)
            messagebox.showinfo("Succès", "Mot de passe mis à jour avec succès!")
            break

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        if username == "admin":
            messagebox.showerror("Erreur", "Vous ne pouvez pas créer un utilisateur avec le nom admin")
            return

        if is_in_rockyou(password):
            messagebox.showerror("Erreur", "Votre mot de passe est compromis. Veuillez en choisir un autre.")
            return

        df = pd.read_csv(USERS_CSV_FILE)
        if username in df['username'].values:
            messagebox.showerror("Erreur", "L'utilisateur existe déjà")
            return

        hashed_password_data = hash(password)
        try:
            with open(USERS_CSV_FILE, "a") as files:
                files.write(f"{username},{hashed_password_data['hash']},{hashed_password_data['salt']}\n")
            messagebox.showinfo("Succès", "Utilisateur ajouté avec succès!")
        except PermissionError:
            messagebox.showerror("Erreur", "Permissions insuffisantes pour ouvrir le fichier")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inconnue : {e}")

    def load_inventory(self):
        self.tree.delete(*self.tree.get_children())
        inventory_file = get_inventory_file(self.current_user)
        try:
            products = pd.read_csv(inventory_file)
            for index, row in products.iterrows():
                self.tree.insert("", "end", values=(row["Nom"], row["Quantité"], row["Prix"]))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement de l'inventaire : {e}")

    def add_to_inventory(self):
        name = simpledialog.askstring("Nom du produit", "Veuillez entrer le nom du produit (lettres uniquement) :")
        if not name.isalpha():
            messagebox.showerror("Erreur", "Nom invalide. Veuillez entrer uniquement des lettres.")
            return

        quantity = simpledialog.askinteger("Quantité du produit", "Veuillez entrer la quantité du produit (nombre entier positif) :")
        if quantity is None or quantity <= 0:
            messagebox.showerror("Erreur", "Quantité invalide. Veuillez entrer un nombre entier positif.")
            return

        prix = simpledialog.askfloat("Prix du produit", "Veuillez entrer le prix du produit (nombre positif) :")
        if prix is None or prix <= 0:
            messagebox.showerror("Erreur", "Prix invalide. Veuillez entrer un nombre positif.")
            return

        inventory_file = get_inventory_file(self.current_user)
        try:
            inventory = pd.read_csv(inventory_file)
        except FileNotFoundError:
            inventory = pd.DataFrame(columns=["Nom", "Quantité", "Prix"])

        new_product = pd.DataFrame({"Nom": [name], "Quantité": [quantity], "Prix": [prix]})
        inventory = pd.concat([inventory, new_product], ignore_index=True)
        inventory.to_csv(inventory_file, index=False)
        self.load_inventory()
        messagebox.showinfo("Succès", "Produit ajouté avec succès!")

    def delete_from_inventory(self):
        name = simpledialog.askstring("Nom du produit", "Veuillez entrer le nom du produit à supprimer :")

        inventory_file = get_inventory_file(self.current_user)
        df = pd.read_csv(inventory_file)
        if name not in df['Nom'].values:
            messagebox.showerror("Erreur", "Le produit n'existe pas.")
            return

        df = df[df['Nom'] != name]
        df.to_csv(inventory_file, index=False)
        self.load_inventory()
        messagebox.showinfo("Succès", "Produit supprimé avec succès!")

    def modify_product(self):
        name = simpledialog.askstring("Nom du produit", "Veuillez entrer le nom du produit à modifier :")

        inventory_file = get_inventory_file(self.current_user)
        df = pd.read_csv(inventory_file)
        if name not in df['Nom'].values:
            messagebox.showerror("Erreur", "Le produit n'existe pas.")
            return

        new_name = simpledialog.askstring("Nouveau nom", "Veuillez entrer le nouveau nom du produit (laissez vide pour ne pas changer) :")
        if new_name and not new_name.isalpha():
            messagebox.showerror("Erreur", "Nom invalide. Veuillez entrer uniquement des lettres.")
            return

        new_quantity = simpledialog.askinteger("Nouvelle quantité", "Veuillez entrer la nouvelle quantité du produit (laissez vide pour ne pas changer) :")
        if new_quantity is not None and new_quantity <= 0:
            messagebox.showerror("Erreur", "Quantité invalide. Veuillez entrer un nombre entier positif.")
            return

        new_prix = simpledialog.askfloat("Nouveau prix", "Veuillez entrer le nouveau prix du produit (laissez vide pour ne pas changer) :")
        if new_prix is not None and new_prix <= 0:
            messagebox.showerror("Erreur", "Prix invalide. Veuillez entrer un nombre positif.")
            return

        if new_name:
            df.loc[df['Nom'] == name, 'Nom'] = new_name
        if new_quantity is not None:
            df.loc[df['Nom'] == name, 'Quantité'] = new_quantity
        if new_prix is not None:
            df.loc[df['Nom'] == name, 'Prix'] = new_prix

        df.to_csv(inventory_file, index=False)
        self.load_inventory()
        messagebox.showinfo("Succès", "Produit modifié avec succès!")

    def recherche_pandas(self):
        nom = simpledialog.askstring("Recherche de produit", "Nom du produit à rechercher :").lower()

        inventory_file = get_inventory_file(self.current_user)
        df = pd.read_csv(inventory_file)
        result = df[df['Nom'].str.lower() == nom]

        if not result.empty:
            messagebox.showinfo("Résultat de la recherche", result[['Nom', 'Quantité', 'Prix']].to_string(index=False))
        else:
            messagebox.showinfo("Résultat de la recherche", "Produit non trouvé !!")

    def afficher_tri_pandas(self):
        choix = simpledialog.askstring("Type de tri", "Choisissez le type de tri:\n1. Tri par ordre alphabétique (Nom)\n2. Tri par quantité croissante\n3. Tri par prix croissant\n")

        inventory_file = get_inventory_file(self.current_user)
        df = pd.read_csv(inventory_file)

        if choix == '1':
            df = df.sort_values(by='Nom', ascending=True)
        elif choix == '2':
            df = df.sort_values(by='Quantité', ascending=True)
        elif choix == '3':
            df = df.sort_values(by='Prix', ascending=True)
        else:
            messagebox.showerror("Erreur", "Choix invalide. Aucun tri effectué.")
            return

        self.tree.delete(*self.tree.get_children())
        for index, row in df.iterrows():
            self.tree.insert("", "end", values=(row["Nom"], row["Quantité"], row["Prix"]))
        messagebox.showinfo("Succès", "Inventaire trié avec succès!")

    def afficher_users(self):
        try:
            users = pd.read_csv(USERS_CSV_FILE)
            messagebox.showinfo("Affichage des utilisateurs", users.to_string(index=False))
        except PermissionError:
            messagebox.showerror("Erreur", "Permissions insuffisantes pour ouvrir le fichier")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inconnue : {e}")

    def delete_users(self):
        name = simpledialog.askstring("Nom d'utilisateur", "Veuillez entrer le nom de l'utilisateur à supprimer :")

        if name not in open(USERS_CSV_FILE).read():
            messagebox.showerror("Erreur", "L'utilisateur n'existe pas")
            return

        try:
            with open(USERS_CSV_FILE, 'r') as file:
                content = file.readlines()
            with open(USERS_CSV_FILE, 'w') as file:
                for line in content:
                    if not line.startswith(name + ','):
                        file.write(line)
            messagebox.showinfo("Succès", "Utilisateur supprimé avec succès!")
        except FileExistsError:
            messagebox.showerror("Erreur", "Le fichier n'a pas été trouvé")
        except PermissionError:
            messagebox.showerror("Erreur", "Les droits ne sont pas suffisants pour ouvrir le fichier")

    def update_user(self):
        username = self.current_user
        new_password = simpledialog.askstring("Nouveau mot de passe", "Veuillez entrer le nouveau mot de passe :", show='*')
        if not new_password:
            messagebox.showerror("Erreur", "Le mot de passe ne peut pas être vide")
            return

        if check_password(new_password):
            messagebox.showerror("Erreur", "Votre nouveau mot de passe est compromis. Veuillez en choisir un autre.")
            return

        df = pd.read_csv(USERS_CSV_FILE)
        hashed_password_data = hash(new_password)
        df.loc[df['username'] == username, 'password'] = hashed_password_data['hash']
        df.loc[df['username'] == username, 'salt'] = hashed_password_data['salt']
        df.to_csv(USERS_CSV_FILE, index=False)
        messagebox.showinfo("Succès", "Mot de passe mis à jour avec succès!")

if __name__ == "__main__":
    app = Application()
    app.mainloop()