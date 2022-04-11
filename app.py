from crypt import methods
from flask import Flask, request, render_template, redirect, session, url_for, flash
from flask_login import LoginManager
from db_levvo import *
from db_levvo import lerClienteEmail
from user import Cliente, Entregador
from authlib.integrations.flask_client import OAuth
import os


########### funções para cadastro de entrega

def criaDicionarioEntrega(endereco,bairro,uf,cidade,cep):
    dicionarioEntrega = {}
    dicionarioEntrega['endereco'],dicionarioEntrega['bairro'],dicionarioEntrega['uf'],dicionarioEntrega['cidade'],dicionarioEntrega['cep'] = endereco,bairro,uf,cidade,cep
    return dicionarioEntrega


def cadastrarEntrega(dicEnderecoColeta,dicEnderecoEntrega,descricao,id_cliente):
    enderecoColeta = criarEndereco(dicEnderecoColeta['endereco'],dicEnderecoColeta['bairro'],dicEnderecoColeta['uf'],dicEnderecoColeta['cidade'],dicEnderecoColeta['cep'])
    enderecoEntrega = criarEndereco(dicEnderecoEntrega['endereco'],dicEnderecoEntrega['bairro'],dicEnderecoEntrega['uf'],dicEnderecoEntrega['cidade'],dicEnderecoEntrega['cep'])
    entrega = criarEntrega(descricao,enderecoColeta.id,enderecoEntrega.id,id_cliente)
    return entrega


# Cria o objeto principal do Flask e do OAuth
app = Flask(__name__)
oauth = OAuth(app)


@app.route("/")
def index():
    return redirect('/login')

@app.route("/login")
def userpickn():
    session.clear()
    #Inicia validação somente se for enviado um post
    return render_template('userpick.html')

#Login Cliente
@app.route("/login/cliente", methods=['POST','GET'])
def loginCliente():
    session.clear()
    session['TIPO_USUARIO'] = 'cliente'
    #Inicia validação somente se for enviado um post
    if request.method == "POST":
        email = request.form['email']
        cliente = Cliente(email)
        if cliente.autentica(email, request.form['password']):
            session['EMAIL'] = email
            session['NOME'] = cliente.nome
            session['ID'] = cliente.id
            return redirect("/home")
        else:
            return render_template('index.html',mensagem=LOGIN_INVALIDO)
    return render_template('index.html', mensagem="")

# Login Entregador
@app.route("/login/entregador", methods=['POST','GET'])
def loginEntregador():
    session.clear()
    session['TIPO_USUARIO'] = 'entregador'
    #Inicia validação somente se for enviado um post
    if request.method == "POST":
        email = request.form['email']
        entregador = Entregador(email)
        if entregador.autentica(email, request.form['password']):
                session['EMAIL'] = entregador.email
                session['NOME'] = entregador.nome
                session['ID'] = entregador.id
                return redirect("/home")
        else:
            return render_template('index.html',mensagem=LOGIN_INVALIDO)
    return render_template('index.html', mensagem="")

@app.route("/cadastro/cliente", methods=['POST','GET'])
def cadastroCliente():
    session.clear()
    #Inicia validação somente se for enviado um post
    if request.method == "POST":
        criarCliente(request.form['nome'],request.form['email'],request.form['password'],request.form['telefone'])
    return render_template("cadastro_cliente.html")

@app.route("/cadastro/entregador", methods=['POST','GET'])
def cadastroEntregador():
    session.clear()
    #Inicia validação somente se for enviado um post
    if request.method == "POST":
        criarEntregador(request.form['nome'],request.form['email'],request.form['password'],request.form['telefone'],request.form['placa'].upper())
    return render_template("cadastro_entregador.html")



#Home (somente logado)
@app.route("/home", methods=['GET','POST'])
def home():
    #Se estiver logado exibe mensagem e nome de usuário, senão exibe acesso não permitido
    if 'NOME' in session:
        if request.method == "POST":
            dictEnderecoColeta = criaDicionarioEntrega(request.form['enderecoColeta'],request.form['bairroColeta'],request.form['ufColeta'],request.form['cidadeColeta'],request.form['cepColeta'])
            dictEnderecoEntrega = criaDicionarioEntrega(request.form['enderecoEntrega'],request.form['bairroEntrega'],request.form['ufEntrega'],request.form['cidadeEntrega'],request.form['cepEntrega'])
            cadastrarEntrega(dictEnderecoColeta,dictEnderecoEntrega,request.form['observacao'],session['ID'])
        return render_template('home.html',mensagem=f"Bem vindo ao Levvo, {session['NOME'].split(' ')[0]}", entregas = listarEntregas())
    else:
        return render_template('home.html',mensagem="Acesso não permitido")


@app.route('/facebook/')
def facebook():
   #configurações do facebook
    FACEBOOK_CLIENT_ID = '376389744363188' #os.environ.get('FACEBOOK_CLIENT_ID')
    FACEBOOK_CLIENT_SECRET = '49f23be22deee6544e4e0cc868e8c831' #os.environ.get('FACEBOOK_CLIENT_SECRET')
    oauth.register(
        name='facebook',
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_uri = url_for('facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)
 
@app.route('/facebook/auth/', methods=['GET','POST'])
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get(
        'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()
    if session['TIPO_USUARIO']=='cliente': user = Cliente(profile['email'])
    elif session['TIPO_USUARIO']=='entregador': user = Entregador(profile['email'])

    if user.autenticaFacebook(profile):
        session['EMAIL'],session['NOME'],session['ID'] = user.email,user.nome,user.id
        return redirect('/home')
    else:
        return redirect(url_for(f"login{type(user).__name__}",mensagem=LOGIN_INVALIDO))




if __name__ == "__main__":
    # Configura chave secreta para utilização da session no flask 
    SECRET_KEY = 'LEVAMOSATEVOCE!@#$@!(%&ssaas'
    app.config['SECRET_KEY'] = SECRET_KEY
    LOGIN_INVALIDO="E-mail ou senha incorretos. Por favor, tente outra vez."
    app.run(debug=True)