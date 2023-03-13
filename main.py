from flask import Flask, render_template, request, make_response, session
import banco
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)
url_externo = "http://boscola.ddns.net:5000/"


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados_cadastro = request.json

    resposta = banco.cadastrar_usuario(dados_cadastro)

    return resposta, 201


@app.route('/login', methods=["POST"])
def login():
    if "usuario" not in session:
        dados_login = request.json

        resposta = banco.autenticar_usuario(dados_login)

        if resposta == "Usuário autenticado com sucesso!":
            session["usuario"] = dados_login["usuario"]

    return resposta, 200


if __name__ == '__main__':
    banco.inicializar()

    app.run(debug=True, host='0.0.0.0')
