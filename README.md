# api-facebook-login

## Oauth
### é implementado para obter autenticação de serviços online. Neste caso foi utilizado para autenticação do Facebook.

* Cliente (Levvo): É o aplicativo ou serviço tentando se conectar ao outro serviço:

* Provedor (Facebook): É o serviço ao qual o cliente se conecta.
* Authorization URL : É a URL fornecida pelo provedor para o qual o cliente envia solicitações.
``` 
authorize_url='https://www.facebook.com/dialog/oauth'
```

* Envio e autenticação:
  * o aplicativo cliente envia uma solicitação de autorização para a URL de autorização do provedor.
  * O usuário se autentica no site do provedor (Facebook) e permite que os recursos sejam utilizados pelo serviço ao cliente.
  * o provedor envia o código de autorização ao cliente.
  * O cliente envia o código de autorização ao servidor de autorização do provedor.
  * o provedor envia os tokens do cliente que podem ser usados para acessar os recursos do usuário.
  
