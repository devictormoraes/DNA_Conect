from pydantic import BaseModel
from typing import List, Optional

# ----------------------
# Produto
# ----------------------


class Produto(BaseModel):
    id: int
    nome: str
    preco: float


# ----------------------
# Cliente
# ----------------------
class Cliente(BaseModel):
    id: Optional[int] = None
    nome: str
    documento: str


# ----------------------
# Item do Pedido
# ----------------------
class PedidoItem(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float


# ----------------------
# Pedido
# ----------------------
class Pedido(BaseModel):
    id: Optional[int] = None
    cliente_id: int
    itens: List[PedidoItem]
    total: float
