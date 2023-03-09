from flask import Flask, render_template, request, Response
import banco


app = Flask(__name__)
url_externo = "http://boscola.ddns.net:5000/"


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados_cadastro = request.json

    resposta = banco.cadastrar_usuario(dados_cadastro)

    return resposta, 201


if __name__ == '__main__':
    banco.inicializar()

    app.run(debug=True, host='0.0.0.0')
