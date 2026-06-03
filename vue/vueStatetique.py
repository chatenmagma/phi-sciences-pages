from tkinter import *
from tkinter import messagebox

from model import *

class VueStatetique(Toplevel):
    """
    Dialogue pour voir les statétiques
    """
    def __init__(self, parent, page: Page):
        super().__init__(parent)

        self.title("Statétique")

        totalAchatLabel: Label = Label(self, text=f"Nombre d'achats efectués: {page.get_nombre_achats()}")
        totalAchatLabel.pack()

        totalBiereLabel: Label = Label(self, text=f"Nombre de bière: {page.get_nombre_achats(Produit.CATEGORIE_BIERE)}")
        totalBiereLabel.pack()

        self.creerButtonBasPage().pack()

    def creerButtonBasPage(self) -> Frame:
        bouttonEnBasFrame = Frame(self)

        validerBoutton = Button(bouttonEnBasFrame, text="Quitter", command=self.destroy)
        validerBoutton.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        return bouttonEnBasFrame