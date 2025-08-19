from fastapi import APIRouter
from models.produtos import Produto
from typing import List

router = APIRouter()

# Simulação de dados
produtos_db = [
    Produto(id=1, nome="Produto A", preco=10.5, estoque=100),
    Produto(id=2, nome="Produto B", preco=5.0, estoque=50)
]

@router.get("/produtos", response_model=List[Produto])
def listar_produtos():
    return produtos_db
