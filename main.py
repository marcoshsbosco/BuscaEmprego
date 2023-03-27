from flask import Flask, render_template, request, make_response, session, redirect
import banco
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)
url_externo = "http://boscola.ddns.net:5000/"


@app.route("/criarvaga", methods=["GET"])
def criar_vaga_front():
    return render_template("criar_vaga.html")


@app.route("/logout", methods=["GET"])
def logout_front():
    return render_template("logout.html")


@app.route("/cadastrar", methods=["GET"])
def cadastrar_front():
    return render_template("cadastrar.html")


@app.route("/login", methods=["GET"])
def login_front():
    if "usuario" not in session:
        return render_template("login.html")
    else:
        return "Usuário já logado!", 200


@app.route("/api/vagasresumidas", methods=["GET"])
def vagas_resumidas():
    resposta = banco.vagas_resumidas()

    return resposta, 200


@app.route("/api/deletarvaga", methods=["POST"])
def deletar_vaga():
    id_vaga = request.json

    resposta = banco.deletar_vaga(id_vaga)

    return resposta, 200


@app.route('/api/criarvaga', methods=['POST'])
def criar_vaga():
    dados_vaga = {}

    for item in request.form.items():
        dados_vaga.update({item[0]: item[1]})

    dados_vaga["id_usuario"] = session["usuario"]

    resposta = banco.cadastrar_vaga(dados_vaga)

    return resposta, 201


@app.route('/api/cadastrar', methods=['POST'])
def cadastrar():
    dados_cadastro = {}

    for item in request.form.items():
        dados_cadastro.update({item[0]: item[1]})

    resposta = banco.cadastrar_usuario(dados_cadastro)

    if resposta == "Esse usuário já existe.":
        return resposta, 200

    return resposta, 201


@app.route('/api/login', methods=["POST"])
def login():
    dados_login = {}

    for item in request.form.items():
        dados_login.update({item[0]: item[1]})

    resposta = banco.autenticar_usuario(dados_login)

    if resposta[0] == "Usuário autenticado com sucesso!":
        session["usuario"] = resposta[1]

    return resposta[0], 200


@app.route("/api/logout", methods=["POST"])
def logout():
    if "usuario" in session:
        del session["usuario"]

    return "Logout realizado com sucesso!", 200


if __name__ == '__main__':
    banco.inicializar()

    app.run(debug=True, host='0.0.0.0')
