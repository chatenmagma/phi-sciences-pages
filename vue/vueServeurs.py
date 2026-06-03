from tkinter import *

from vue.messageErreurs import MessageErreurs

from model import *

class VueServeur(Toplevel):
    """
    Dialogue pour modifier les serveurs et le président
    """
    def __init__(self, parent, page: Page):
        super().__init__(parent)

        self.title("Modification des serveurs")

        self.page: Page = page

        self.nouveauPresident: StringVar = StringVar(value=page.president)

        presidentSection: Frame = Frame(self)
        presidentLabel: Label = Label(presidentSection, text="President:")
        presidentLabel.grid(row=0, column=0, sticky="e")

        presidentEntry: Entry = Entry(presidentSection, textvariable=self.nouveauPresident)
        presidentEntry.grid(row=0, column=1)
        
        presidentSection.pack()

        self.serveurText: Text = Text(self)

        self.serveurText.insert(END, "\n") # Pour le président mort
        
        for s in page.serveurs:
            self.serveurText.insert(END, f"{s}\n")

        self.serveurText.pack()

        self.creerButtonBasPage().pack()

    def creerButtonBasPage(self) -> Frame:
        bouttonEnBasFrame = Frame(self)

        annulerBoutton = Button(bouttonEnBasFrame, text="Annuler", command=self.destroy)
        annulerBoutton.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

        validerBoutton = Button(bouttonEnBasFrame, text="Validax", command=self.valider)
        validerBoutton.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        return bouttonEnBasFrame

    def valider(self) -> None:
        if self.nouveauPresident.get() == "":
            MessageErreurs.manque_valeur("president")
            return

        nouveauServeurs: list[str] = self.serveurText.get("1.0", "end-1c").split("\n")

        if self.nouveauPresident.get() not in nouveauServeurs:
            MessageErreurs.valeur_indesponible("president")
            return

        self.page.president = self.nouveauPresident.get()
        self.page.setServeurs(nouveauServeurs)

        self.destroy()