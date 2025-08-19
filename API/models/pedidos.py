from pydantic import BaseModel
from typing import List
from .produtos import Produto

class ItemPedido(BaseModel):
    produto_id: int
    quantidade: int

class Pedido(BaseModel):
    id_vendedor: int
    cliente_id: int
    itens: List[ItemPedido]
    data: str
