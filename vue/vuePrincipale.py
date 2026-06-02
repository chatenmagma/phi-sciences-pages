from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from pathlib import Path
from datetime import datetime

from model import *
from service import *

from vue.vueAchat import VueAchat
from vue.vueProduit import VueProduit
from vue.vueServeurs import VueServeur

class VuePrincipale(Tk):
    """
    Vue principale avec les 200 pages
    """
    def __init__(self):
        super().__init__(None, None, "Tk", True, False, None)

        self.page: Page = Page()
        self.title(f"Pages de Phi-Sciences {Page.VERSION}")

        file: Path = Path(self.fichierPrincipal())

        if file.exists():
            with open(file, "r") as f:
                deserialise(f.read()).update(self.page)
                f.close()

        self.config(menu=self.creerMenuBar())

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        for i in range(50):
            for j in range(4):
                self.creerPage(i + j * 50).grid(row=i, column=j, sticky="ew", padx=3)
    
    @staticmethod
    def genereNomFichierSauvegardeBackup() -> str:
        """
        Donne le nom du fichier qui sert à faire des backup, il présise le temps
        """
        return f"pagePhiSciences_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"
    @staticmethod
    def fichierPrincipal():
        """
        Donne le nom du fichier principal avec l'année universitaire en cours
        """
        anneUniv: int = 0

        if datetime.now().month >= 8: # en moins d'août
            anneUniv = datetime.now().year + 1
        else:
            anneUniv = datetime.now().year

        return f"pagePhiSciences_{anneUniv - 1}-{anneUniv}.json"
    
    def sauvegarderCommand(self) -> None:
        with open(self.fichierPrincipal(), "w", encoding="utf-8") as f: 
            f.write(serialise(self.page))
            f.close()
        print("sauvegarde du fichier principal est fait")
    def sauvegarderACommand(self) -> None:
        self.sauvegarderCommand()

        dir = Path(filedialog.askdirectory(title="Trouve ta sauvegarde"))

        if not dir: return

        cheminVersFichier: Path = Path(dir) / self.genereNomFichierSauvegardeBackup()

        with open(cheminVersFichier, "w", encoding="utf-8") as f: 
            f.write(serialise(self.page))
            f.close()

    def payerCommand(self, index: int) -> None:
        VueAchat(self, self.page, index)

        self.sauvegarderCommand()
    
    def modifProduitCommand(self) -> None:
        VueProduit(self, self.page)
    
        self.sauvegarderCommand()

    def modifServeursCommand(self) -> None:
        VueServeur(self, self.page)

        self.sauvegarderCommand()

    def nettoyageCommand(self) -> None:
        message = messagebox.askquestion(title="T SUR DE FËR SA?", message="T'es sûr de nettoyer les pages de solde 0€, les pauvres adhérents qui n'auront plus de pages....")
        if message == "yes":
            self.page.nettoyerAdherents()
        
        self.sauvegarderCommand()

    def creerMenuBar(self) -> Menu:
        menuBar: Menu = Menu(self)

        # Partie fichierMenu

        fichierMenu: Menu = Menu(menuBar, tearoff=0)

        fichierMenu.add_command(label="Ouvrir")
        fichierMenu.add_command(label="Sauvegarder", command=self.sauvegarderCommand)
        fichierMenu.add_command(label="Sauvegarder à", command=self.sauvegarderACommand)
        fichierMenu.add_separator()
        fichierMenu.add_command(label="Quitter", command=self.quit)

        menuBar.add_cascade(label="Fichier", menu=fichierMenu)

        # Partie editionMenu

        editionMenu: Menu = Menu(menuBar, tearoff=0)

        editionMenu.add_command(label="Nettoyage des pages", command=self.nettoyageCommand)
        editionMenu.add_command(label="Modification des produits", command=self.modifProduitCommand)
        editionMenu.add_command(label="Edition du staff", command=self.modifServeursCommand)

        menuBar.add_cascade(label="Edition", menu=editionMenu)

        return menuBar
    
    @staticmethod
    def changementDeFondLabel(adherent: Adherent, label: Label):
        if adherent.estNegatif():
            label.config(bg="red", fg="white")
        elif adherent.estZero():
            label.config(bg="white", fg="black")
        else:
            label.config(bg="green", fg="white")
        
    @staticmethod
    def on_surmoi(widget):
        widget.config(cursor="hand2", font=("Couriel", 10, "bold"))
    @staticmethod
    def on_sourrisQuiSort(widget):
        widget.config(cursor="", font=("TkDefaultFont", 9, "normal"))

    def creerPage(self, index: int) -> Frame:
        entree = Frame(self, relief="ridge", bd=1)

        entree.columnconfigure(2, weight=1)

        adherent: Adherent = self.page[index]

        indexLabel: Label = Label(entree, text=f"{index + 1}", anchor="e", width=3)
        indexLabel.grid(row=0, column=0, sticky="w")

        nomLabel: Label = Label(entree, textvariable=adherent.nomProperty, anchor="w")
        nomLabel.grid(row=0, column=1, sticky="w")

        prenomLabel: Label = Label(entree, textvariable=adherent.prenomProperty, anchor="w")
        prenomLabel.grid(row=0, column=2, sticky="ew")

        solde:Label = Label(entree, textvariable=adherent.soldeAffichageProperty, anchor="e", width=10)
        solde.grid(row=0, column=3, sticky="e", padx=3)

        self.page[index].soldeProperty.trace_add("write", lambda *args: self.changementDeFondLabel(self.page[index], solde))
        self.changementDeFondLabel(self.page[index], solde)

        widget = (indexLabel, entree, indexLabel, nomLabel, prenomLabel, solde)
        for w in widget:
            w.bind("<Button-1>", lambda event: self.payerCommand(index))

            # Gestion de la sourris hoverlay sur les pages
            w.bind("<Enter>", lambda event: (
                self.on_surmoi(indexLabel),
                self.on_surmoi(nomLabel),
                self.on_surmoi(prenomLabel),
                self.on_surmoi(solde)
            ))
            w.bind("<Leave>", lambda event: (
                self.on_sourrisQuiSort(indexLabel),
                self.on_sourrisQuiSort(nomLabel),
                self.on_sourrisQuiSort(prenomLabel),
                self.on_sourrisQuiSort(solde)
            ))

        return entree

    def run(self):
        self.mainloop()

    def avantFermerProgramme(self):
        self.sauvegarderCommand()
        print("Merci d'avoir utiliser, au revoir ;)")