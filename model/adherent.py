from dataclasses import dataclass
from tkinter import StringVar, DoubleVar

from model.produit import Achat

class Adherent:
    """
    Contenant tous les données des adhérents dont l'historique des achats. L'achat le plus récent se situe en haut de la pile
    """
    def __init__(self, nom: str = "", prenom: str = "", solde: float = 0):
        self.nomProperty: StringVar = StringVar(value=nom)
        self.prenomProperty: StringVar = StringVar(value=prenom)
        self.soldeProperty: DoubleVar = DoubleVar(value=solde)
        self.soldeAffichageProperty: StringVar = StringVar(value=f"{solde}€")

        self.achats: list[Achat] = []

    def renomer(self, nom: str, prenom: str) -> None:
        self.nomProperty.set(nom)
        self.prenomProperty.set(prenom)
    
    def payer(self, achat: Achat) -> None:
        self.achats.insert(0, achat)

        if achat.nom == "ajout":
            self.setSolde(self.getSolde() + achat.prix)
        else:
            self.setSolde(self.getSolde() - achat.prix)
    def supprimer(self) -> None:
        if(self.estVide()): return

        self.renomer("", "")
        self.setSolde(0)
        self.achats = []

    def estNegatif(self) -> bool:
        return self.getSolde() < 0
    def estVide(self) -> bool:
        return len(self.getNom()) == 0 and len(self.getPrenom()) == 0
    def estZero(self) -> bool:
        return self.getSolde() == 0

    def getNom(self) -> str:
        return self.nomProperty.get()
    def getPrenom(self) -> str:
        return self.prenomProperty.get()
    def getSolde(self) -> float:
        return self.soldeProperty.get()
    def getAchats(self) -> list[Achat]:
        return self.achats

    def setSolde(self, solde: float) -> None:
        self.soldeProperty.set(solde)
        self.soldeAffichageProperty.set(f"{solde}€")
    
@dataclass
class AdherentDTO:
    nom: str
    prenom: str
    solde: float
    achats: list[Achat]

    @classmethod
    def from_adherent(cls, data: Adherent):
        return AdherentDTO(
            data.getNom(),
            data.getPrenom(),
            data.getSolde(),
            data.getAchats()
        )
    
    def from_dict(data: dict):
        return AdherentDTO(
            data["nom"],
            data["prenom"],
            data["solde"],
            [Achat.from_dict(a) for a in data["achats"]]
        )
    
    def update(self, adherent: Adherent) -> None:
        adherent.renomer(self.nom, self.prenom)
        adherent.setSolde(self.solde)
        adherent.achats = self.achats
        
    