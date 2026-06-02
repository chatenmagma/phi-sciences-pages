from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from datetime import datetime

from model import *

class VueAchat(Toplevel):
    def __init__(self, parent, page: Page, index: int):
        super().__init__(parent)

        self.title(f"Vous achetez quoi ? PAGE n°{index + 1}")

        self.page: Page = page
        self.adherent: Adherent = page[index]
        
        self.nouveauNom: StringVar = StringVar(value=self.adherent.getNom())
        self.nouveauPrenom: StringVar = StringVar(value=self.adherent.getPrenom())

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
        
        if self.choixServeur.get() != "":
            listServeur.selection_set(0)
    
    def filterProduit(self, listProduit: Listbox) -> None:
        listProduit.delete(0, END)

        for produit in list(self.page.produits.keys()):
            if self.choixProduit.get() == "" or produit.lower().startswith(self.choixProduit.get().lower()):
                listProduit.insert(END, produit)
        
        if self.choixProduit.get() != "":
            listProduit.selection_set(0)
    
    def creerAchat(self) -> Frame:
        achatFrame: Frame = Frame(self)

        # Partie QUOI? (choix produit)
        produitLabel: Label = Label(achatFrame, text="QUOI?")
        produitLabel.grid(row=0, column=0)
        produitEntry: Entry = Entry(achatFrame, textvariable=self.choixProduit)
        produitEntry.grid(row=1, column=0)
        produitList: Listbox = Listbox(achatFrame)

        produitEntry.bind("<KeyRelease>", lambda event: self.filterProduit(produitList))
        produitEntry.bind("<Return>", lambda event: self.choixProduit.set(list(self.page.produits.keys())[produitList.curselection()[0]]))
        produitList.bind("<<ListboxSelect>>", lambda event: self.choixProduit.set(list(self.page.produits.keys())[produitList.curselection()[0]]))
        self.filterProduit(produitList)

        produitList.grid(row=2, column=0, sticky="nsew")

        # Partie QUI? (choix serveur)
        serverLabel: Label = Label(achatFrame, text="QUI?")
        serverLabel.grid(row=0, column=1)
        serveurEntry: Entry = Entry(achatFrame, textvariable=self.choixServeur)
        serveurEntry.grid(row=1, column=1)
        serveurList: Listbox = Listbox(achatFrame)
        
        serveurEntry.bind("<KeyRelease>", lambda event: self.filterServeur(serveurList))
        serveurEntry.bind("<Return>", lambda event: self.choixServeur.set(self.page.serveurs[serveurList.curselection()[0]]))
        serveurList.bind("<<ListboxSelect>>", lambda event: self.choixServeur.set(self.page.serveurs[serveurList.curselection()[0]]))
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
        if(self.nouveauNom.get() != ""): self.adherent.nomProperty.set(self.nouveauNom.get().upper())
        if(self.nouveauPrenom.get() != ""): self.adherent.prenomProperty.set(self.nouveauPrenom.get().capitalize())

        if self.adherent.nomProperty.get() == "":
            messagebox.showerror(title="C'est qui cet adhérent", message="L'adhérent n'a pas de nom de famille")
            return
        if self.adherent.prenomProperty.get() == "":
            messagebox.showerror(title="C'est qui cet adhérent", message="L'adhérent n'a pas de prenom")
            return

        if self.choixProduit.get() == "":
            messagebox.showerror(title="Erreur C KWA TACHETE", message="T'as oublié de mettre un produit dans QUOI?...")
            return
        if self.choixServeur.get() == "":
            messagebox.showerror(title="Erreur C KI FAI LAKSION", message="C'est quiqui fait l'action, tu dois mettre un serveur dans QUI?...")
            return
        
        if self.choixProduit.get() not in list(self.page.produits.keys()):
            messagebox.showerror(title="C KWAH CE TRUC?", message="Ce produit n'existe pas...")
            return
        if self.choixServeur.get() not in self.page.serveurs:
            messagebox.showerror(title="EST-CE ANONYMOUS KI NOUS PIRATE !!!!", message="Je ne connais pas ce serveur, je veux lui payer sa girafe à lui ;)")
            return
        if (self.choixProduit.get() == "ajout" or self.choixProduit.get() == "retrait") and self.ptetreValeur.get() == "":
            messagebox.showerror(title="OU EST LA VALEUR !!!!", message="Pour tout ajout ou retrait, veuillez explecitement mettre la valeur...")
            return
        
        valeur: float = 0.0

        if (self.choixProduit.get() == Page.AJOUT_COMMAND) or (self.choixProduit.get() == Page.RETRAIT_COMMAND):
            try:
                if self.choixProduit.get() == "ajout":
                    valeur = float(self.ptetreValeur.get())

                    if valeur < 0:
                        messagebox.showerror(title="Erreur T CON", message="La valeur doit être toujours positif....")
                        return
            except:
                messagebox.showerror(title="ERREUR DE TYPAGE DE VALEUR", message="La valeur est un chiffre, et ça doit être de la forme << 0.5 >> avec un POINT")
                return
        else:
            valeur = self.page.produits[self.choixProduit.get()].prix
        
      
        self.adherent.payer(Achat(self.choixProduit.get(), valeur, datetime.now(), self.choixServeur.get()))

        self.destroy()