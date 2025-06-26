from core.interfaces.InterfaceRepository import InterfaceRepository

class AutenticadorUsuario():
    def __init__(self,personalRepo:InterfaceRepository):
        self.personalRepo = personalRepo

    def AutenticarUsuario(self, usuario:dict):

        cpf = usuario.get("cpf", None)
        senha = usuario.get("senha", None)


        if not cpf or not senha:
            raise Exception("Os campos não foram completamente preenchidos")

        query = self.personalRepo.consultarCpf(cpf)

        if not query:
            raise Exception("Esse cpf não existe.")

        if not (query.get("senha") == senha):
            raise Exception("Senha errada")

        return True