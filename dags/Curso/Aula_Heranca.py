class Produto:
    '''Define a classe Produto.'''
    
    # Construtor da classe Produto
    def __init__(self, nome, codigo, preco, quantidade):
        '''Cria uma instância de Produto.'''
        self._nome = nome
        self._codigo = codigo
        self._preco = preco
        self._quantidade = quantidade
    
    # Retorna o nome do produto
    def obtem_nome(self):
        return self._nome
    
    # Retorna o código do produto
    def obtem_codigo(self):
        return self._codigo
    
    # Retorna o preço corrente do produto
    def obtem_preco(self):
        return self._preco
    
    # Devolve True se o novo preço for maior que o anterior
    def altera_preco(self, novo_preco):
        pp = self._preco
        self._preco = novo_preco
        if novo_preco > pp:
            return True
        return False
    
    # Devolve False se a quantidade de produtos requerida não estiver disponível
    def altera_quantidade(self, novo_pedido):
        if novo_pedido > self._quantidade:
            return False
        self._quantidade -= novo_pedido
        return True
