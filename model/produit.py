from dataclasses import dataclass
from typing import ClassVar
from datetime import datetime

@dataclass
class Achat:
    """
    Servant à stocker les données utiles de l'achat
    """
    nom: str
    prix: float
    quand: datetime
    qui: str
    page: int

    @staticmethod
    def from_dict(data: dict) -> "Achat":
        return Achat(
            data["nom"],
            data["prix"],
            datetime.fromisoformat(data["quand"]),
            data["qui"],
            data["page"]
        )

    def getQuandFormat(self) -> str:
        return self.quand.strftime("%d/%m/%Y %H:%M")
    
    def __str__(self) -> str:
        return f"{self.prix:.2f}€ {self.nom} par {self.qui} le {self.quand.strftime("%d/%m/%Y à %H:%M:%S")} a la page {self.page}"
    

@dataclass
class Produit:
    """
    Les données nécessaire pour les produits
    """

    TOUS_CATEGORIES: ClassVar[list[str]] = ["boisson", "bière", "soft", "sucré", "salé", "amer", "pétillant", "nourriture", "végétarien", "formule", "chaud", "évènement", "inconnue"]

    CATEGORIE_BOISSON: ClassVar[str] = "boisson"
    CATEGORIE_BIERE: ClassVar[str] = "bière"
    CATEGORIE_SOFT: ClassVar[str] = "soft"

    CATEGORIE_SUCREE: ClassVar[str] = "sucré"
    CATEGORIE_SALEE: ClassVar[str] = "salé"
    CATEGORIE_AMER: ClassVar[str] = "amer"
    CATEGORIE_PETILLANT: ClassVar[str] = "pétillant"

    CATEGORIE_NOURRITURE: ClassVar[str] = "nourriture"
    CATEGORIE_VEGETARIEN: ClassVar[str] = "végétarien"
    CATEGORIE_FORMULE: ClassVar[str] = "formule"
    
    CATEGORIE_CHAUD: ClassVar[str] = "chaud"
    CATEGORIE_FROID: ClassVar[str] = "froid"
    
    CATEGORIE_EVENEMENT: ClassVar[str] = "évènement"
    CATEGORIE_INCONNUE: ClassVar[str] = "inconnue"

    nom: str
    prix: float
    categorie: str = CATEGORIE_INCONNUE

    @staticmethod
    def unification_categories(*categories: str) -> str:
        tmp = [c for c in categories if c in Produit.TOUS_CATEGORIES]
        
        if len(tmp) == 0:
            return Produit.CATEGORIE_INCONNUE

        tmp.sort()

        return "-".join(tmp)
    
    @staticmethod
    def trie_categories(categories: str):
        return Produit.unification_categories(*categories.split("-"))

    def est_categorie(self, categorie: str) -> bool:
        return categorie in self.categorie.split("-")
    
    def __str__(self) -> str:
        return f"{self.prix:.2f}€ {self.categorie} {self.nom}"

    def __lt__(self, other):
        if type(other) == str:
            return self.nom < other
        if type(other) == Produit:
            return self.nom < other.nom