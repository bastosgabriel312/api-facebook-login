import email
from sqlalchemy import create_engine, delete,ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, insert, delete,select
import pymysql
from sqlalchemy.ext.declarative import declarative_base
   
#base para criação de engine#

Base = declarative_base()
   
#Conectanto e criando a máquina para utilizar o sql alchemy
engine = create_engine('ENGINE')
Session = sessionmaker(bind=engine)
db_session = Session()
   
class Cliente(Base):
   __tablename__ = 'tb_cliente'
   id = Column(Integer, primary_key=True)
   nome = Column(String(100))
   email = Column(String(50))
   senha = Column(String(50))
   telefone = Column(String(20))

   
class Entregador(Base):
   __tablename__ = 'tb_entregador'
   id = Column(Integer, primary_key=True)
   nome = Column(String(100))
   email = Column(String(50))
   senha = Column(String(50))
   telefone = Column(String(20))
   placa = Column(String(10))
   
class Entrega(Base):
   __tablename__ = 'tb_entrega'
   id = Column(Integer, primary_key=True)
   descricao = Column(String(200))
   id_endereco_coleta = Column(Integer)
   id_endereco_final = Column(Integer)
   id_cliente = Column(Integer, ForeignKey('tb_entrega.id'))
   id_entregador = Column(Integer, ForeignKey('tb_entrega.id'))
   

class Endereco(Base):
   __tablename__ = 'tb_endereco'
   id = Column(Integer, primary_key=True)
   endereco = Column(String(300))
   bairro = Column(String(100))
   uf = Column(String(2))
   cidade = Column(String(100))
   cep = Column(String(10))
   

#Realiza a criação das tabelas solicitadas
Base.metadata.create_all(engine)
   
############ CRUD #################

############ CLIENTE #################
def criarCliente(nome,email,senha,telefone):
   cliente = Cliente(nome = nome,email = email,senha = senha,telefone = telefone)
   db_session.add(cliente)
   db_session.commit()
   return cliente

def lerCliente(id):
   for cliente in db_session.query(Cliente).filter_by(id=id):
      return cliente

def lerClienteEmail(email):
   cliente = db_session.query(Cliente).filter_by(email=email).one()
   return cliente


def editarNomeCliente(id,novoNome):
   cliente = db_session.query(Cliente).filter(Cliente.id == id).one()
   cliente.nome = novoNome
   db_session.commit()
   return cliente


def editarEmailCliente(id,novoEmail):
   cliente = db_session.query(Cliente).filter(Cliente.id == id).one()
   cliente.email = novoEmail
   db_session.commit()
   return cliente

def editarSenhaCliente(id,novaSenha):
   cliente = db_session.query(Cliente).filter(Cliente.id == id).one()
   cliente.senha = novaSenha
   db_session.commit()
   return cliente

def editarTelefoneCliente(id,novoTelefone):
   cliente = db_session.query(Cliente).filter(Cliente.id == id).one()
   cliente.telefone = novoTelefone
   db_session.commit()
   return cliente

############ ENTREGADOR #################

def criarEntregador(nome,email,senha,telefone, placa):
   entregador = Entregador(nome = nome,email = email,senha = senha,telefone = telefone,placa = placa)
   db_session.add(entregador)
   db_session.commit()
   return entregador

def lerEntregador(id):
   for entregador in db_session.query(Entregador).filter_by(id=id).one():
      return entregador

def lerEntregadorEmail(email):
   try:
      entregador = db_session.query(Entregador).filter_by(email=email).one()
      return entregador
   except:
      return


def editarNomeEntregador(id,novoNome):
   entregador = db_session.query(Entregador).filter(Entregador.id == id).one()
   entregador.nome = novoNome
   db_session.commit()
   return entregador

def editarEmailEntregador(id,novoEmail):
   entregador = db_session.query(Entregador).filter(Entregador.id == id).one()
   entregador.email = novoEmail
   db_session.commit()
   return entregador

def editarSenhaEntregador(id,novaSenha):
   entregador = db_session.query(Entregador).filter(Entregador.id == id).one()
   entregador.senha = novaSenha
   db_session.commit()
   return entregador

def editarTelefoneEntregador(id,novoTelefone):
   entregador = db_session.query(Entregador).filter(Entregador.id == id).one()
   entregador.telefone = novoTelefone
   db_session.commit()
   return entregador


############ ENTREGA #################

def criarEntrega(descricao,id_endereco_coleta,id_endereco_final,id_cliente):
   entrega = Entrega(descricao = descricao,id_endereco_coleta = id_endereco_coleta,id_endereco_final = id_endereco_final,id_cliente=id_cliente)
   db_session.add(entrega)
   db_session.commit()
   return entrega

def listarEntregas():
   entregas = []
   for entrega in db_session.query(Entrega):
         entregas.append(entrega)
   return entregas

def lerEntrega(id):
   for entrega in db_session.query(Entrega).filter_by(id=id):
      return entrega

def listaEntregasCliente(email):
   cliente = lerClienteEmail(email)
   if cliente is not None:
      listaEntregas = []
      for entrega in db_session.query(Entrega).filter_by(id_cliente=cliente.id):
         enderecoColeta = lerEndereco(entrega.id_endereco_coleta)
         enderecoFinal = lerEndereco(entrega.id_endereco_final)
         entrega = {
                  'N Entrega': entrega.id,
                  'Descricao': entrega.descricao,
                  'Endereço de Coleta': f'{enderecoColeta.endereco}, {enderecoColeta.bairro } - {enderecoColeta.cidade} / {enderecoColeta.uf}',
                  'Endereço de Final': f'{enderecoFinal.endereco}, {enderecoFinal.bairro} - {enderecoFinal.cidade} / {enderecoFinal.uf}',
                  }
         listaEntregas.append(entrega)
      return listaEntregas
   else:
      return False
      
def editarDescricaoEntrega(id,novaDescricao):
   entrega = db_session.query(Entrega).filter(Entrega.id == id).one()
   entrega.descricao = novaDescricao
   db_session.commit()
   return entrega

def editarEnderecoColetaEntrega(id,numero,complemento,cep,id_bairro):
   entrega = db_session.query(Entrega).filter(Entrega.id == id).one()
   novoEndereco = criarEndereco(numero,complemento,cep,id_bairro)
   entrega.id_endereco_coleta = novoEndereco.id
   db_session.commit()
   return entrega

def editarEnderecoFinalEntrega(id,numero,complemento,cep,id_bairro):
   entrega = db_session.query(Entrega).filter(Entrega.id == id).one()
   novoEndereco = criarEndereco(numero,complemento,cep,id_bairro)
   entrega.id_endereco_entrega = novoEndereco.id
   db_session.commit()
   return entrega

############ ENDERECO #################

def criarEndereco(endereco,bairro,uf, cidade,cep):
   endereco = Endereco(endereco=endereco,bairro=bairro,uf=uf, cidade=cidade,cep=cep)
   db_session.add(endereco)
   db_session.commit()
   return endereco

def lerEndereco(id):
   for endereco in db_session.query(Endereco).filter_by(id=id):
      return endereco





#Insere dados do usuário na tabela usuários
# cliente = Cliente(nome="Vinicius",email="vinicius@gmail.com",senha="vinicius123",telefone="11991677867")
 


#novoCliente = criarCliente("Gabriel Bastos","bastosgabriel312@gmail.com",123456, "11991111111")
# novoEntregador = criarEntregador("Matheus Evangelista dos Santos","matheus.evangelista@gmail.com",123456,"11991672327","ABC1234")
# db_session.add(novoEntregador)
# db_session.commit()

#print(novoCliente)
#Select de dados dados