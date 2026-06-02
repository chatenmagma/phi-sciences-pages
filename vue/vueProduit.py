from tkinter import *
from tkinter import messagebox

from model import *

class VueProduit(Toplevel):
    def __init__(self, parent, page: Page):
        super().__init__(parent)

        self.title("Modification des produits en vente")

        self.page: Page = page

        self.produitsText: Text = Text(self)
        
        for k in page.produits.keys():
            if k == Page.AJOUT_COMMAND or k == Page.RETRAIT_COMMAND: continue
            self.produitsText.insert(END, f"{page.produits[k].prix} {k}\n")

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

        for produit in textProduits:
            if produit == "": continue

            try:
                prixStr, nomProduit = produit.split(" ", 1)

                try:
                    prix = float(prixStr)

                    if prix < 0:
                        messagebox.showerror(title="Erreur T CON", message=f"Ligne \"{produit}\": La valeur doit être toujours positif....")
                        return
                except:
                    messagebox.showerror(title="ERREUR DE TYPAGE DE VALEUR", message=f"Ligne \"{produit}\": La valeur est un chiffre, et ça doit être de la forme << 0.5 >> avec un POINT")
                    return
            except:
                messagebox.showerror(title="Errer, de formatage", message=f"Ligne \"{produit}\": il manque un truc ça doit être de la forme \"3.4 Corsendonk\"")
                return
            
            produits.append(Produit(nomProduit, prix))
        
        produits.sort()
        
        self.page.setProduits(produits)

        self.destroy()