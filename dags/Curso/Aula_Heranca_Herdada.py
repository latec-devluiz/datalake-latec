from Aula_Heranca import Produto

class ProdutoCritico(Produto):
    def __init__(self, nome, codigo, preco, quantidade, estoque_min):
        super().__init__(nome, codigo, preco, quantidade)
        self._estoque_min = estoque_min