from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from datetime import datetime

from model import *

class VueAchat(Toplevel):
    """
    Dialogue pour faire payer des choses aux adhérents
    """
    def __init__(self, parent, page: Page, index: int):
        super().__init__(parent)

        self.title(f"Vous achetez quoi ? PAGE n°{index + 1}")

        self.index: int = index

        self.page: Page = page
        
        self.nouveauNom: StringVar = StringVar(value=page[index].getNom())
        self.nouveauPrenom: StringVar = StringVar(value=page[index].getPrenom())

        self.choixProduit: StringVar = StringVar()
        self.choixServeur: StringVar = StringVar()
        self.ptetreValeur: StringVar = StringVar()

        self.creerAchat().grid(row = 0, column=0)        
        self.creerInfoAdherent().grid(row=0, column=1)
        self.creerButtonBasPage().grid(row=1, column=0)

        self.grid_columnconfigure(0, weight=1)
    
    def filterServeur(self, listServeur: Listbox) -> None:
        listServeur.delete(0, END)

        for serveur in self.page.serveurs:
            if self.choixServeur.get() == "" or serveur.lower().startswith(self.choixServeur.get().lower()):
                listServeur.insert(END, serveur)
        
        if listServeur.size() > 0:
            listServeur.selection_set(0)
    
    def filterProduit(self, listProduit: Listbox) -> None:
        listProduit.delete(0, END)

        for produit in list(self.page.produits.keys()):
            if self.choixProduit.get() == "" or produit.lower().startswith(self.choixProduit.get().lower()):
                listProduit.insert(END, produit)
        
        if listProduit.size() > 0:
            listProduit.selection_set(0)
    
    def on_produit_selectione(self, event, produitList: Listbox):
        """Gère la gestion d'un produit"""
        selection = produitList.curselection()

        if selection: self.choixProduit.set(produitList.get(selection[0]))
    
    def on_produit_entree(self, envent, produitList: Listbox):
        """Gère la gestion d'un produit quand on appuie sur la touche entrée"""
        selection = produitList.curselection()

        if selection: self.choixProduit.set(produitList.get(selection[0]))
    
    def on_serveur_selectione(self, event, serveurList: Listbox):
        """Gère la gestion d'un produit"""
        selection = serveurList.curselection()

        if selection: self.choixServeur.set(serveurList.get(selection[0]))
    
    def on_serveur_entree(self, envent, serveurList: Listbox):
        """Gère la gestion d'un produit quand on appuie sur la touche entrée"""
        selection = serveurList.curselection()

        if selection: self.choixServeur.set(serveurList.get(selection[0]))
    
    
    def creerAchat(self) -> Frame:
        achatFrame: Frame = Frame(self)

        # Partie QUOI? (choix produit)
        produitLabel: Label = Label(achatFrame, text="QUOI?")
        produitLabel.grid(row=0, column=0)
        produitEntry: Entry = Entry(achatFrame, textvariable=self.choixProduit)
        produitEntry.grid(row=1, column=0)
        produitList: Listbox = Listbox(achatFrame)

        produitEntry.bind("<KeyRelease>", lambda event: self.filterProduit(produitList))
        produitEntry.bind("<Return>", lambda event: self.on_produit_entree(event, produitList))
        produitList.bind("<<ListboxSelect>>", lambda event: self.on_produit_selectione(event, produitList))
        self.filterProduit(produitList)

        produitList.grid(row=2, column=0, sticky="nsew")

        # Partie QUI? (choix serveur)
        serverLabel: Label = Label(achatFrame, text="QUI?")
        serverLabel.grid(row=0, column=1)
        serveurEntry: Entry = Entry(achatFrame, textvariable=self.choixServeur)
        serveurEntry.grid(row=1, column=1)
        serveurList: Listbox = Listbox(achatFrame)
        
        serveurEntry.bind("<KeyRelease>", lambda event: self.filterServeur(serveurList))
        serveurEntry.bind("<Return>", lambda event: self.on_serveur_entree(event, serveurList))
        serveurList.bind("<<ListboxSelect>>", lambda event: self.on_serveur_selectione(event, serveurList))
        self.filterServeur(serveurList)

        serveurList.grid(row=2, column=1, sticky="nsew")

        # Partie Valeur?
        valeurLabel: Label = Label(achatFrame, text="Valeur(Pour ajout ou retrait)")
        valeurLabel.grid(row=0, column=3)
        valeurEntry:Entry = Entry(achatFrame, textvariable=self.ptetreValeur)
        valeurEntry.grid(row=1, column=3)

        return achatFrame

    def creerInfoAdherent(self) -> Frame:
        infoAdherentFrame = Frame(self)

        nomLabel: Label = Label(infoAdherentFrame, text="Nom:")
        nomLabel.grid(row=0, column=0, sticky="e")
        
        prenomLabel: Label = Label(infoAdherentFrame, text="Prenom:")
        prenomLabel.grid(row=1, column=0, sticky="e") 

        self.nomEntry: Entry = Entry(infoAdherentFrame, textvariable=self.nouveauNom)
        self.nomEntry.grid(row=0, column=1)
        self.prenomEntry: Entry = Entry(infoAdherentFrame, textvariable=self.nouveauPrenom)
        self.prenomEntry.grid(row=1, column=1)

        return infoAdherentFrame

    def creerButtonBasPage(self) -> Frame:
        bouttonEnBasFrame = Frame(self)

        annulerBoutton = Button(bouttonEnBasFrame, text="Annuler", command=self.destroy)
        annulerBoutton.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

        validerBoutton = Button(bouttonEnBasFrame, text="Validax", command=self.valider)
        validerBoutton.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        return bouttonEnBasFrame
    
    def valider(self):
        if self.nouveauNom.get() == "":
            messagebox.showerror(title="C'est qui cet adhérent", message="L'adhérent n'a pas de nom de famille")
            return
        if self.nouveauPrenom.get() == "":
            messagebox.showerror(title="C'est qui cet adhérent", message="L'adhérent n'a pas de prenom")
            return

        if self.choixProduit.get() == "":
            messagebox.showerror(title="Devez dire quoi acheté", message="Vous avez oublié de mettre un produit dans QUOI?")
            return
        if self.choixServeur.get() == "":
            messagebox.showerror(title="C'est qui fait l'action d'achat (un membre du staff)", message="Vous avez oublié de mettre un membre dans QUI?")
            return
        
        if self.choixProduit.get() not in list(self.page.produits.keys()):
            messagebox.showerror(title="Produit inconnu", message="Ce produit est inconnu dans la liste, vous pouvez l'ajouté sur edition > modif produit")
            return
        if self.choixServeur.get() not in self.page.serveurs:
            messagebox.showerror(title="Membre du staff inconnu", message="Ce membre est inconnu dans la liste, vous pouvez l'ajouté sur edition > modif staff")
            return
        if (self.choixProduit.get() == Page.AJOUT_COMMAND or self.choixProduit.get() == Page.RETRAIT_COMMAND) and self.ptetreValeur.get() == "":
            messagebox.showerror(title="Manque la donnée valeur", message="Pour tout ajout ou retrait, vous devez mettre la valeur")
            return
        
        valeur: float = 0.0

        # Recupe la valeur c-à-d son prix
        if (self.choixProduit.get() == Page.AJOUT_COMMAND) or (self.choixProduit.get() == Page.RETRAIT_COMMAND):
            try:
                if self.choixProduit.get() == Page.AJOUT_COMMAND or self.choixProduit.get() == Page.RETRAIT_COMMAND:
                    valeur = float(self.ptetreValeur.get().replace(",", ".")) # On remplace la virgule par un point, c'est plus pratique ;)

                    if valeur < 0:
                        messagebox.showerror(title="Erreur valeur negative", message="La valeur doit être toujours positif")
                        return
            except:
                messagebox.showerror(title="Erreur du chiffre de valeur", message="Vous devez écrire un chiffre sous la forme 23,55 ou 0,34. De plus ce chiffre doit être positif")
                return
        else: # On recupère la valeur du produit
            valeur = self.page.produits[self.choixProduit.get()].prix
        
        # Demande de confirmation de payer un adhérent n'ayant pas assez pour payer le choix
        if self.choixProduit.get() != Page.AJOUT_COMMAND and self.page[self.index].getSolde() - valeur < 0 and messagebox.askquestion(title="Adhérent n'ayant la solde suffisante /!\\", message="Voulez-vous vraiment faire payer un adhérence qui n'a pas assez dans sa solde ?") == "no":
            return
        
        # On met le nouveau nom et prénom à l'adhérent

        self.page[self.index].nomProperty.set(self.nouveauNom.get().upper())
        self.page[self.index].prenomProperty.set(self.nouveauPrenom.get().capitalize())
      
        self.page.payer(self.index, Achat(self.choixProduit.get(), valeur, datetime.now(), self.choixServeur.get(), self.index))

        self.destroy()