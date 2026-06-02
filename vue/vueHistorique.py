from tkinter import *
from tkinter import messagebox

from model import *

class VueHistorique(Toplevel):
    """
    Dialogue pour voir l'historique d'achat d'une page
    """
    def __init__(self, parent, page: Page, index: int):
        super().__init__(parent)

        self.title(f"Vu historique page n°{index}")

        nomEtPrenomLabel: Label = Label(self, text=f"{page[index].getNom()} {page[index].getPrenom()}", font=("Arial", 12, "bold"))
        nomEtPrenomLabel.pack()

        achatList: Listbox = Listbox(self, width=50, height=50)
        achatList.pack()

        for achat in page[index].getAchats():
            achatList.insert(END, str(achat))

        self.creerButtonBasPage().pack()

    def creerButtonBasPage(self) -> Frame:
        bouttonEnBasFrame = Frame(self)

        validerBoutton = Button(bouttonEnBasFrame, text="Quitter", command=self.destroy)
        validerBoutton.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        return bouttonEnBasFrame