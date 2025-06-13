from datetime import datetime
class Aluno():
    def __init__(self, aluno):
        self.id = aluno.get("_id")
        self.nome = aluno.get('nome','')
        self.telefone = aluno.get('telefone')
        self.cpf = aluno.get('cpf')
        self.data_nascimento = aluno.get('data_nascimento')
        self.email = aluno.get('email')
        self.senha = aluno.get('senha')
        self.status = aluno.get('status')
        self.plano = aluno.get('plano')
        self.data_assinatura = aluno.get('data_assinatura')
        self.data_renovacao = aluno.get('data_renovacao')
        self.personal = aluno.get('personal')
        self.sessoes = aluno.get('sessoes',[])
