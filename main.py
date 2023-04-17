from flask import Flask, render_template, request, make_response, session, redirect
import banco
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)
url_externo = "http://boscola.ddns.net:5000"


@app.route("/vaga/<id_vaga>", methods=["GET"])
def vaga_expandida(id_vaga):
    vaga = banco.vaga(id_vaga)

    return render_template("vaga.html", vaga=vaga, empresa=banco.usuario(vaga["id_usuario"]))


@app.route("/manutencao", methods=["GET"])
def manutencao_front():
    if "usuario" in session:
        return render_template("manutencao.html")
    else:
        return redirect(f"{url_externo}/login")


@app.route("/", methods=["GET"])
def listar_vagas_front():
    return render_template("listar_vagas.html", data={"vagas": banco.vagas_resumidas(), "usuario": None if "usuario" not in session else session["usuario"]})


@app.route("/criarvaga", methods=["GET"])
def criar_vaga_front():
    if "usuario" in session:
        return render_template("criar_vaga.html")
    else:
        return redirect(f"{url_externo}/login")


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


@app.route("/api/vaga", methods=["POST"])
def vaga():
    id_vaga = request.form["id_vaga"]

    resposta = banco.vaga(id_vaga)

    return resposta, 200


@app.route("/api/vagas", methods=["GET"])
def vagas():
    resposta = banco.vagas(session["usuario"])

    return resposta


@app.route("/api/vagasresumidas", methods=["POST"])
def vagas_resumidas():
    dados_filtro = request.form

    resposta = banco.vagas_resumidas(dados_filtro)

    return resposta, 200


@app.route("/api/deletarvaga", methods=["POST"])
def deletar_vaga():
    id_vaga = request.form["id_vaga"]

    resposta = banco.deletar_vaga(id_vaga)

    return resposta, 200


@app.route('/api/criarvaga', methods=['POST'])
def criar_vaga():
    dados_vaga = {}

    for item in request.form.items():
        dados_vaga.update({item[0]: item[1]})

    dados_vaga["id_usuario"] = session["usuario"]

    resposta = banco.cadastrar_vaga(dados_vaga)

    return redirect(f"{url_externo}/")


@app.route('/api/cadastrar', methods=['POST'])
def cadastrar():
    dados_cadastro = {}

    for item in request.form.items():
        dados_cadastro.update({item[0]: item[1]})

    resposta = banco.cadastrar_usuario(dados_cadastro)

    if resposta == "Esse usuário já existe.":
        return resposta, 200

    return redirect(f"{url_externo}/")


@app.route('/api/login', methods=["POST"])
def login():
    dados_login = {}

    for item in request.form.items():
        dados_login.update({item[0]: item[1]})

    resposta = banco.autenticar_usuario(dados_login)

    if resposta[0] == "Usuário autenticado com sucesso!":
        session["usuario"] = resposta[1]

    return redirect(f"{url_externo}/")


@app.route("/api/logout", methods=["POST"])
def logout():
    if "usuario" in session:
        del session["usuario"]

    return "OK", 200


if __name__ == '__main__':
    banco.inicializar()

    app.run(debug=True, host='0.0.0.0')
