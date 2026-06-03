from dataclasses import dataclass
from tkinter import StringVar, DoubleVar

from model.produit import Achat

class Adherent:
    """
    Contenant tous les données des adhérents dont l'historique des achats. L'achat le plus récent se situe en haut de la pile
    """
    def __init__(self, page, nom: str = "", prenom: str = "", solde: float = 0):
        self.page = page
        self.nomProperty: StringVar = StringVar(value=nom)
        self.prenomProperty: StringVar = StringVar(value=prenom)
        self.soldeProperty: DoubleVar = DoubleVar()
        self.soldeAffichageProperty: StringVar = StringVar()

        self.setSolde(solde)

        self.achats: list[int] = []

    def renomer(self, nom: str, prenom: str) -> None:
        self.nomProperty.set(nom)
        self.prenomProperty.set(prenom)
    
    def payer(self, achat: Achat, indiceHistorique: int) -> None:
        self.achats.insert(0, indiceHistorique)

        if achat.nom == "ajout":
            self.setSolde(self.getSolde() + achat.prix)
        else:
            self.setSolde(self.getSolde() - achat.prix)

    def supprimer(self) -> None:
        if(self.estVide()): return

        self.renomer("", "")
        self.setSolde(0.0)
        self.achats = []
    
    def viderAchat(self) -> None:
        self.achats = []

    def estNegatif(self) -> bool:
        """
        Dit si l'adhérent a un solde négatif
        """
        return self.getSolde() < 0.0
    def estVide(self) -> bool:
        """
        Dit si l'adhérent n'est pas initialisé, c'est-à-dire que pour le modèle cette page à cette indice a personne
        """
        return self.getNom() == "" and self.getPrenom() == ""
    def estZero(self) -> bool:
        """
        Dit si l'adhérent a un solde nul (c'est-à-dire 0)
        """
        return (self.getSolde() * 100 / 100) == 0.00

    def getNom(self) -> str:
        return self.nomProperty.get()
    def getPrenom(self) -> str:
        return self.prenomProperty.get()
    def getSolde(self) -> float:
        return self.soldeProperty.get()
    def getIndicesAchats(self) -> list[int]:
        """
        Donne l'indice de l'historique venant du modèle des achats de la page. Le premier élément est l'achat le plus récent
        """
        return self.achats
    def getAchats(self) -> list[Achat]:
        """
        Donne l'historique de tous les achats de la page. Le premier élément est l'achat le plus récent
        """
        return [self.page.getHistorique()[i] for i in self.getIndicesAchats()]
    
    def setAchats(self, nouveauxAchats: list[int]) -> None:
        self.achats = nouveauxAchats.copy()
    def setSolde(self, solde: float) -> None:
        self.soldeProperty.set(solde)
        self.soldeAffichageProperty.set(f"{solde:.2f}€".replace(".", ","))
    
    def getDernierAchat(self) -> Achat:
        return self.page.getHistorique()[self.achats[0]]
    def getAchat(self, index: int) -> Achat:
        return self.page.getHistorique()[index]
    
@dataclass
class AdherentDTO:
    nom: str
    prenom: str
    solde: float
    achats: list[int]

    @classmethod
    def from_adherent(cls, data: Adherent):
        return AdherentDTO(
            data.getNom(),
            data.getPrenom(),
            data.getSolde(),
            data.achats
        )
    
    def from_dict(data: dict):
        return AdherentDTO(
            data["nom"],
            data["prenom"],
            data["solde"],
            data["achats"]
        )
    
    def update(self, adherent: Adherent) -> None:
        adherent.renomer(self.nom, self.prenom)
        adherent.setSolde(self.solde)
        adherent.setAchats(self.achats)
        
    