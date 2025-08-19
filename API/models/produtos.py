from pydantic import BaseModel
from typing import Optional

class Produto(BaseModel):
    id: int
    nome: str
    preco: float
    estoque: int
    ultima_atualizacao: Optional[str] = None
