import mariadb


cursor = None


def inicializar():
    global cursor

    conexao = mariadb.connect(
        user="buscaemprego",
        password="buscaemp_api",
        host="localhost",
        port=5000,
        database="buscaemprego"
    )

    conexao.autocommit = True

    cursor = conexao.cursor(dictionary=True)


def cadastrar_usuario(dados_cadastro):
    cursor.execute(
        "SELECT usuario FROM usuarios WHERE usuario = ?",
        (dados_cadastro["usuario"],)
    )
    usuario = cursor.fetchone()

    if usuario:
        return "Esse usuário já existe."

    cursor.execute(
        "INSERT INTO usuarios VALUES (?, ?)",
        (dados_cadastro["usuario"], dados_cadastro["senha"])
    )

    return "Usuário inserido com sucesso!"


def autenticar_usuario(dados_login):
    cursor.execute(
        "SELECT usuario, senha FROM usuarios WHERE usuario = ?",
        (dados_login["usuario"],)
    )

    usuario = cursor.fetchone()

    if not usuario:
        return "Usuário não encontrado."
    elif usuario["senha"] != dados_login["senha"]:
        return "Senha incorreta."

    return "Usuário autenticado com sucesso!"
