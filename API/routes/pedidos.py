from fastapi import APIRouter
from models.pedidos import Pedido

router = APIRouter()

@router.post("/pedidos")
def receber_pedido(pedido: Pedido):
    # Aqui futuramente você salvará no Firebird
    print(f"Pedido recebido: {pedido}")
    return {"status": "sucesso", "mensagem": "Pedido registrado com sucesso"}
