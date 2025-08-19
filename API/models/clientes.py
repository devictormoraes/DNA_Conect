from pydantic import BaseModel
from typing import Optional

class Cliente(BaseModel):
    id: int
    nome: str
    documento: str
    endereco: Optional[str] = None
