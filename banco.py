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

    cursor = conexao.cursor()


def cadastrar_usuario(dados_cadastro):
    cursor.execute(
        "INSERT INTO usuarios VALUES (?, ?)",
        (dados_cadastro["usuario"], dados_cadastro["senha"])
    )

    return "Usuário inserido com sucesso!"
