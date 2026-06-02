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
    return json.dumps(asdict(PageDTO.from_page(data)), indent=2, cls=AdapterJSONEncoder)
def deserialise(data: str) -> PageDTO:
    return PageDTO.from_dict(json.loads(data))