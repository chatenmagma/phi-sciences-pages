import json
from dataclasses import asdict

from model import *

from datetime import datetime

class AdapterJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def serialise(data: Page) -> str:
    """
    Transforme le modèle vers un chaîne de caractère pour sauvegarder dans un fichier en JSON
    """
    return json.dumps(asdict(PageDTO.from_page(data)), indent=2, cls=AdapterJSONEncoder)
def deserialise(data: str) -> PageDTO:
    """
    Transforme un texte provenant JSON vers une type contenant lesdites données
    """
    return PageDTO.from_dict(json.loads(data))