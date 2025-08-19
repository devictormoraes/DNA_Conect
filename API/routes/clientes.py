from fastapi import APIRouter
from models.clientes import Cliente
from typing import List

router = APIRouter()

# Simulação de dados
clientes_db = [
    Cliente(id=1, nome="João da Silva", documento="12345678900"),
    Cliente(id=2, nome="Maria Souza", documento="98765432100")
]

@router.get("/clientes", response_model=List[Cliente])
def listar_clientes():
    return clientes_db
