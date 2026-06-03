from tkinter import *
from tkinter import messagebox

from vue.messageErreurs import MessageErreurs

from model import *

class VueProduit(Toplevel):
    """
    Dialogue pour modifier tous les produis de l'association
    """
    def __init__(self, parent, page: Page):
        super().__init__(parent)

        self.title("Modification des produits en vente")

        self.page: Page = page

        self.produitsText: Text = Text(self)
        
        for k in page.produits.keys():
            if k == Page.AJOUT_COMMAND or k == Page.RETRAIT_COMMAND: continue
            self.produitsText.insert(END, f"{str(page.produits[k])}\n")

        self.produitsText.pack()

        self.creerButtonBasPage().pack()

    def creerButtonBasPage(self) -> Frame:
        bouttonEnBasFrame = Frame(self)

        annulerBoutton = Button(bouttonEnBasFrame, text="Annuler", command=self.destroy)
        annulerBoutton.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

        validerBoutton = Button(bouttonEnBasFrame, text="Validax", command=self.valider)
        validerBoutton.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        return bouttonEnBasFrame

    def valider(self) -> None:
        textProduits: list[str] = self.produitsText.get("1.0", "end-1c").split("\n")
        produits: list[Produit] = []

        prix: float = 0.0

        for ligne in textProduits:
            if ligne == "": continue

            element: str = ligne.split(" ", 2)

            if len(element) != 3:
                MessageErreurs.formatage("Vous devez d'abods dire combien ça coûte puis donner le nom du produit\nExemple de bon formatage de produit: 0,20€ boisson-chaude-amer café", ligne)
                return

            prixStr, categories, nomProduit = element

            try:
                prix = float(prixStr.replace(",", ".").replace("€", ""))

                if prix < 0:
                    MessageErreurs.valeur_negative(ligne)
                    return
            except ValueError:
                MessageErreurs.encodement(ligne)
                return
           
            
            produits.append(Produit(nomProduit, prix, Produit.trie_categories(categories)))
        
        produits.sort()
        
        self.page.setProduits(produits)

        self.destroy()