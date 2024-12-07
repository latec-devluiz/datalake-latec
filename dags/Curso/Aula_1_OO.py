class Produto:

    # Metodo construtor   
    def __init__(self,nome, codigo, preco, quantidade):
         # cria uma instancia de Produto
        self.__nome = nome
        self.__codigo = codigo
        self.__preco = preco
        self.__quantidade = quantidade


    # Retorna o nome do produto
    def obtem_nome(self):
        return self.__nome


    def obtem_codigo(self):
        return self.__codigo
    
    def obtem_preco(self):
        return self.__preco



# testes da classe
if __name__ == "__main__":
 p1 = Produto("Camisa Social", 123456, 45.56, 1000)
 p2 = Produto("Calça Jeans", 423564, 98.12, 500)
 print("Oferta do dia:", p1.obtem_nome())
 print("Oferta da semana:", p2.obtem_nome())
