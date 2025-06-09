from dataclasses import dataclass
from datetime import datetime

@dataclass
class Cocktail:
    id: int
    name: str
    url: str
    description: str
    created_at: datetime


@dataclass
class Ingredient:
    id: int
    name: str
    created_at: datetime