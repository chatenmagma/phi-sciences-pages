from dataclasses import dataclass

from model.adherent import Adherent, AdherentDTO
from model.produit import Produit

class Page:
    MAX_ADHERENTS: int = 200
    AJOUT_COMMAND: str = "ajout"
    RETRAIT_COMMAND: str = "retrait"
    VERSION: str = "v1.0"

    def __init__(self):
        self.serveurs: list[str] = []
        self.president: str = ""
        self.adherents: list[Adherent] = [Adherent() for _ in range(Page.MAX_ADHERENTS)]

        self.produits: dict[str, Produit] = {}
        self.setProduits([Produit("Diane", 0.1)])
    
    def getAdherents(self) -> list[Adherent]:
        return self.adherents
    def getProduit(self, nom: str) -> Produit|None:
        if(nom not in self.produits.keys()):
            return None
        return self.produits[nom]

    def nettoyerAdherents(self) -> None:
        """
        Il nettoie les pages c'est-à-dire il enlève tout adhérents qui ont pour solde 0€
        """
        for adherent in self.adherents:
            if(adherent.estZero()): adherent.supprimer()
        
        print("Nettoyage effectué")
    
    def setProduits(self, produits: list[Produit]) -> None:
        self.produits = { Page.AJOUT_COMMAND: Produit(Page.AJOUT_COMMAND, 0.0), Page.RETRAIT_COMMAND: Produit(Page.RETRAIT_COMMAND, 0.0) }
        
        for p in produits:
            if p.nom == Page.AJOUT_COMMAND or p.nom == Page.RETRAIT_COMMAND: continue

            self.produits[p.nom] = p
    
    def setServeurs(self, nouveauServeurs: list[str]) -> None:
        self.serveurs = [s for s in nouveauServeurs if s != ""]

        self.serveurs.sort()

    def __getitem__(self, index: int|str) -> Adherent:
        if type(index) == int:
            return self.adherents[index]
        if type(index) == str:
            return self.adherents[int(index)]

@dataclass
class PageDTO:
    serveurs: list[str]
    president: str
    adherents: dict[int, AdherentDTO]
    produits: list[Produit]

    @classmethod
    def from_page(cls, data: Page) -> PageDTO:
        return PageDTO(
            [serveur for serveur in data.serveurs],
            data.president,
            { i: AdherentDTO.from_adherent(data[i]) for i in range(Page.MAX_ADHERENTS) if not data[i].estVide() },
            [Produit(p.nom, p.prix) for p in data.produits.values() if p.nom != Page.AJOUT_COMMAND and p.nom != Page.RETRAIT_COMMAND]
        )

    @staticmethod
    def from_dict(data: dict) -> PageDTO:
        return PageDTO(
            data["serveurs"],
            data["president"],
            { i:AdherentDTO.from_dict(v) for i, v in data["adherents"].items() },
            [Produit(**p) for p in data["produits"]]
        )
    
    def update(self, page: Page) -> None:
        for k, v in self.adherents.items():
            v.update(page[k])
        for p in self.produits:
            page.produits[p.nom] = p

        page.serveurs = self.serveurs
        page.president = self.president