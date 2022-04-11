from db_levvo import lerClienteEmail, lerEntregadorEmail

class Usuario:
    def autentica(self, email, senha):
        try:
            if self.email == email and self.password == senha:
                return True
        except:
            return False
        return False
    
    def autenticaFacebook(self,profile):
        try:
            if profile['email'] == self.email:
                return True
        except:
            return False
        return False


class Cliente(Usuario):
    def __init__(self, email):
        dbUser = lerClienteEmail(email)
        if dbUser is not None:
            self.id = dbUser.id
            self.nome = dbUser.nome
            self.email = dbUser.email
            self.password = dbUser.senha
            self.telefone = dbUser.telefone

class Entregador(Usuario):
    def __init__(self, email):
        dbUser = lerEntregadorEmail(email)
        if dbUser is not None:
            self.id = dbUser.id
            self.nome = dbUser.nome
            self.email = dbUser.email
            self.password = dbUser.senha
            self.telefone = dbUser.telefone
            self.placa = dbUser.placa

