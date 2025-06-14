
class PersonalEntity():

    def __init__(self, kwargs):

        self.nome = kwargs.get('nome')
        self.senha = kwargs.get('senha')
        self.telefone = kwargs.get('telefone')
        self.email = kwargs.get('email')
        self.cpf = kwargs.get('cpf')
        self.salario = kwargs.get('salario')
        self.acesso = kwargs.get('acesso')
        self.cref = kwargs.get('cref')