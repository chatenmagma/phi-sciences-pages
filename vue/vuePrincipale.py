from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from datetime import datetime
from pathlib import Path

from vue.vueAchat import VueAchat
from vue.vueAide import VueAide
from vue.vueHistorique import VueHistorique
from vue.vueProduit import VueProduit
from vue.vueStatetique import VueStatetique
from vue.vueServeurs import VueServeur

from model import *
from service import *

class VuePrincipale(Tk):
    """
    Vue principale avec les 200 pages
    """
    def __init__(self):
        super().__init__(None, None, "Tk", True, False, None)

        self.page: Page = Page()
        self.title(f"Pages de Phi-Sciences {Page.VERSION}")

        file: Path = Path(self.fichier_principal(self.get_annee_scolaire()))
        file_ancienne_annee: Path = Path(self.fichier_principal(self.get_annee_scolaire() - 1))

        if file.exists():
            with open(file, "r") as f:
                deserialise(f.read()).update(self.page)
                f.close()
        elif file_ancienne_annee.exists(): # On crée un nouveau fichier pour l'année en cours
            with open(file_ancienne_annee, "r") as f:
                deserialise(f.read()).update(self.page)
                f.close()
            
            # On vide l'historique et les page à solde 0€
            self.page.nettoyerAdherents()
            self.page.viderHistorique()

            self.commande_enrigistrer()

        self.config(menu=self.creerMenuBar())

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        for i in range(50):
            for j in range(4):
                self.creerPage(i + j * 50).grid(row=i, column=j, sticky="ew", padx=3)
    
    @staticmethod
    def genere_nom_fichier_sauvegarde_backup() -> str:
        """
        Donne le nom du fichier qui sert à faire des backup, il présise le temps
        """
        return f"pagePhiSciences_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"
    
    @staticmethod
    def get_annee_scolaire() -> int:
        return datetime.now().year + 1 if datetime.now().month >= 8 else datetime.now().year

    @staticmethod
    def fichier_principal(annee: int, nomfichier: str = "pagePhiSciences"):
        """
        Donne le nom du fichier principal avec l'année universitaire en cours
        """
        return f"{nomfichier}_{annee - 1}-{annee}.json"
    
    def commande_aide(self) -> None:
        VueAide(self)
    
    def commande_enrigistrer(self) -> None:
        with open(self.fichier_principal(self.get_annee_scolaire()), "w", encoding="utf-8") as f: 
            f.write(serialise(self.page))
            f.close()

    def commande_enrigistrer_sous(self) -> None:
        self.commande_enrigistrer()

        dir = Path(filedialog.askdirectory(title="Où allez-vous enrigistrer"))

        if not dir: return

        chemin: Path = Path(dir) / self.genere_nom_fichier_sauvegarde_backup()

        with open(chemin, "w", encoding="utf-8") as f: 
            f.write(serialise(self.page))
            f.close()

    def commande_payer(self, index: int) -> None:
        VueAchat(self, self.page, index)

        self.commande_enrigistrer()
    
    def commande_historique(self, index: int) -> None:
        if not self.page[index].estVide():
            VueHistorique(self, self.page, index)
    
    def commande_modifier_produits(self) -> None:
        VueProduit(self, self.page)
    
        self.commande_enrigistrer()

    def commande_modifier_serveurs(self) -> None:
        VueServeur(self, self.page)

        self.commande_enrigistrer()

    def commande_nettoyer(self) -> None:
        message = messagebox.askquestion(
            title="Demande pour le nettoyage des pages ?", 
            message="T'es sûr de nettoyer les pages de solde 0€, les pauvres adhérents qui n'auront plus de pages...."
        )
        if message == "yes":
            self.page.nettoyerAdherents()
        
        self.commande_enrigistrer()
    
    def commande_statetique(self) -> None:
        VueStatetique(self, self.page)

    def creerMenuBar(self) -> Menu:
        menuBar: Menu = Menu(self)

        # Partie fichierMenu

        fichierMenu: Menu = Menu(menuBar, tearoff=0)

        fichierMenu.add_command(label="Ouvrir")
        fichierMenu.add_command(label="Sauvegarder", command=self.commande_enrigistrer)
        fichierMenu.add_command(label="Sauvegarder à", command=self.commande_enrigistrer_sous)
        fichierMenu.add_separator()
        fichierMenu.add_command(label="Quitter", command=self.quit)

        menuBar.add_cascade(label="Fichier", menu=fichierMenu)

        # Partie editionMenu

        editionMenu: Menu = Menu(menuBar, tearoff=0)

        editionMenu.add_command(label="Nettoyage des pages", command=self.commande_nettoyer)
        editionMenu.add_command(label="Modification des produits", command=self.commande_modifier_produits)
        editionMenu.add_command(label="Edition du staff", command=self.commande_modifier_serveurs)

        menuBar.add_cascade(label="Edition", menu=editionMenu)

        menuBar.add_command(label="Statetiques", command=self.commande_statetique)

        menuBar.add_command(label="Aide", command=self.commande_aide)

        return menuBar
    
    @staticmethod
    def on_solde_changement_arriereplan_label(adherent: Adherent, label: Label):
        if adherent.estNegatif():
            label.config(bg="red", fg="white")
        elif adherent.estZero():
            label.config(bg="white", fg="black")
        else:
            label.config(bg="green", fg="white")
    @staticmethod
    def on_adherent_changement_creation_label(adherent: Adherent, label: Label):
        if adherent.estVide():
            label.config(bg="#f3d47e")
        else:
            label.config(bg="#b8ceeb")
        
    @staticmethod
    def on_sourris_sur_element(widget):
        widget.config(cursor="hand2", font=("Couriel", 10, "bold"))
    @staticmethod
    def on_sourris_sort_element(widget):
        widget.config(cursor="", font=("TkDefaultFont", 9, "normal"))

    def creerPage(self, index: int) -> Frame:
        entree = Frame(self, relief="ridge", bd=1)

        entree.columnconfigure(2, weight=1)

        adherent: Adherent = self.page[index]

        indexLabel: Label = Label(entree, text=f"{index + 1} |", anchor="e", width=4)
        indexLabel.grid(row=0, column=0, sticky="w")

        nomLabel: Label = Label(entree, textvariable=adherent.nomProperty, anchor="w")
        nomLabel.grid(row=0, column=1, sticky="w")

        prenomLabel: Label = Label(entree, textvariable=adherent.prenomProperty, anchor="w")
        prenomLabel.grid(row=0, column=2, sticky="ew")

        solde:Label = Label(entree, textvariable=adherent.soldeAffichageProperty, anchor="e", width=10)
        solde.grid(row=0, column=3, sticky="e", padx=3)

        self.page[index].soldeProperty.trace_add("write", lambda *args: self.on_solde_changement_arriereplan_label(self.page[index], solde))
        self.on_solde_changement_arriereplan_label(self.page[index], solde)

        self.page[index].nomProperty.trace_add(("write"), lambda *args: (
            self.on_adherent_changement_creation_label(self.page[index], indexLabel),
            self.on_adherent_changement_creation_label(self.page[index], prenomLabel),
            self.on_adherent_changement_creation_label(self.page[index], nomLabel)
        ))
        self.on_adherent_changement_creation_label(self.page[index], indexLabel)
        self.on_adherent_changement_creation_label(self.page[index], prenomLabel)
        self.on_adherent_changement_creation_label(self.page[index], nomLabel)

        widget = (indexLabel, entree, indexLabel, nomLabel, prenomLabel, solde)
        for w in widget:
            w.bind("<Button-1>", lambda event: self.commande_payer(index))
            w.bind("<Button-3>", lambda event: self.commande_historique(index))

            # Gestion de la sourris hoverlay sur les pages
            w.bind("<Enter>", lambda event: (
                self.on_sourris_sur_element(indexLabel),
                self.on_sourris_sur_element(nomLabel),
                self.on_sourris_sur_element(prenomLabel),
                self.on_sourris_sur_element(solde)
            ))
            w.bind("<Leave>", lambda event: (
                self.on_sourris_sort_element(indexLabel),
                self.on_sourris_sort_element(nomLabel),
                self.on_sourris_sort_element(prenomLabel),
                self.on_sourris_sort_element(solde)
            ))

        return entree

    def run(self):
        self.mainloop()

    def avantFermerProgramme(self):
        self.commande_enrigistrer()
        print("Merci d'avoir utiliser, au revoir ;)")