from dataclasses import dataclass

from model.adherent import Adherent, AdherentDTO
from model.produit import Produit, Achat

class Page:
    """
    Est le mdoèle de tout le projet. Il sert à gérer les 200 pages contenant des adhérents
    """
    MAX_ADHERENTS: int = 200
    AJOUT_COMMAND: str = "ajout"
    RETRAIT_COMMAND: str = "retrait"
    VERSION: str = "v1.0"

    def __init__(self):
        self.serveurs: list[str] = []
        self.president: str = ""
        self.adherents: list[Adherent] = [Adherent(self) for _ in range(Page.MAX_ADHERENTS)]
        self.historique: list[Achat] = []

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
        
    def get_nombre_achats(self, categorie: str = "") -> int:
        if categorie == "":
            return len([a for a in self.historique if a.nom != Page.AJOUT_COMMAND and a.nom != Page.RETRAIT_COMMAND])
        
        return len([a for a in self.historique if (a.nom != Page.AJOUT_COMMAND and a.nom != Page.RETRAIT_COMMAND) and self.produits[a.nom].est_categorie(categorie)])
    
    def setServeurs(self, nouveauServeurs: list[str]) -> None:
        self.serveurs = [s for s in nouveauServeurs if s != ""]

        self.serveurs.sort()
    
    def getHistorique(self) -> list[Achat]:
        return self.historique

    def setHistorique(self, nouveauHistorique: list[Achat]) -> None:
        self.historique = nouveauHistorique.copy()
    
    def payer(self, index: int, achat: Achat):
        self[index].payer(achat, len(self.getHistorique()))
        self.historique.append(achat)

    def viderHistorique(self):
        self.historique = []
        for adherent in self.adherents: adherent.viderAchat()
    
    def getDernierAchat(self) -> Achat:
        return self.historique[-1]

    def __getitem__(self, index: int|str) -> Adherent:
        if type(index) == int:
            return self.adherents[index]
        if type(index) == str:
            return self.adherents[int(index)]

@dataclass
class PageDTO:
    """
    Type de données pour le modèle servant à la sauvegarde du fichier
    """
    serveurs: list[str]
    president: str
    adherents: dict[int, AdherentDTO]
    produits: list[Produit]
    historique: list[Achat]

    @classmethod
    def from_page(cls, data: Page) -> PageDTO:
        """
        Donnee le type donnée 
        """
        return PageDTO(
            [serveur for serveur in data.serveurs],
            data.president,
            { i: AdherentDTO.from_adherent(data[i]) for i in range(Page.MAX_ADHERENTS) if not data[i].estVide() },
            [Produit(p.nom, p.prix) for p in data.produits.values() if p.nom != Page.AJOUT_COMMAND and p.nom != Page.RETRAIT_COMMAND],
            data.getHistorique()
        )

    @staticmethod
    def from_dict(data: dict) -> PageDTO:
        return PageDTO(
            data["serveurs"],
            data["president"],
            { i:AdherentDTO.from_dict(v) for i, v in data["adherents"].items() },
            [Produit(**p) for p in data["produits"]],
            [Achat.from_dict(h) for h in data["historique"]]
        )
    
    def update(self, page: Page) -> None:
        """
        Met à jour le modèle avec le type de donnée
        """
        for k, v in self.adherents.items(): # Parcours la liste des adhérents
            v.update(page[k])
        
        page.setProduits(self.produits)
        page.setHistorique(self.historique)

        page.serveurs = self.serveurs
        page.president = self.president