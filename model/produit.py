from dataclasses import dataclass
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

    @staticmethod
    def from_dict(data: dict) -> Achat:
        return Achat(
            data["nom"],
            data["prix"],
            datetime.fromisoformat(data["quand"]),
            data["qui"]
        )

    def getQuandFormat(self) -> str:
        return self.quand.strftime("%d/%m/%Y %H:%M")
    
    def __str__(self) -> str:
        return f"{self.prix}€ {self.nom} par {self.qui} le {self.quand.strftime("%d/%m/%Y à %H:%M:%S")}"
    

@dataclass
class Produit:
    """
    Les données nécessaire pour les produits
    """
    nom: str
    prix: float

    def __lt__(self, other):
        if type(other) == str:
            return self.nom < other
        if type(other) == Produit:
            return self.nom < other.nom