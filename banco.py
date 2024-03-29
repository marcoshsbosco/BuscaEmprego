import mariadb


cursor = None


def inicializar():
    global cursor

    conexao = mariadb.connect(
        user="buscaemprego",
        password="buscaemp_api",
        host="boscola.ddns.net",
        port=3306,
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
        "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
        (dados_cadastro["usuario"], dados_cadastro["senha"])
    )

    return "Usuário inserido com sucesso!"


def autenticar_usuario(dados_login):
    cursor.execute(
        "SELECT id, usuario, senha FROM usuarios WHERE usuario = ?",
        (dados_login["usuario"],)
    )
    usuario = cursor.fetchone()

    if not usuario:
        return "Usuário não encontrado."
    elif usuario["senha"] != dados_login["senha"]:
        return "Senha incorreta."

    return "Usuário autenticado com sucesso!", usuario["id"]


def cadastrar_vaga(dados_vaga):
    cursor.execute(
        "INSERT INTO vagas (cargo, funcao, salario, horas, lugar, contato, id_usuario) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (dados_vaga["cargo"], dados_vaga["funcao"], dados_vaga["salario"], dados_vaga["horas"], dados_vaga["lugar"], dados_vaga["contato"], dados_vaga["id_usuario"])
    )

    return "Vaga inserida com sucesso!"


def deletar_vaga(id_vaga):
    cursor.execute(
        "DELETE FROM vagas WHERE id = ?",
        (id_vaga,)
    )

    return "Vaga deletada com sucesso!"


def vagas_resumidas(dados_filtro=None):
    dql = "SELECT v.id, u.usuario, v.funcao, v.salario FROM vagas v JOIN usuarios u ON v.id_usuario = u.id"

    salario = None
    funcao = None

    if dados_filtro:
        if "salario" in dados_filtro:
            salario = dados_filtro["salario"]
        if "funcao" in dados_filtro:
            funcao = dados_filtro["funcao"]

    if salario or funcao:
        dql += " WHERE"

        if salario and funcao:
            dql += " salario > (?) AND v.funcao LIKE ?"

            cursor.execute(
                dql,
                (salario, f"%{funcao}%",)
            )
        elif salario:
            dql += " salario > (?)"

            cursor.execute(
                dql,
                (salario,)
            )
        elif funcao:
            dql += " v.funcao LIKE ?"

            print(dql)
            print(funcao)

            cursor.execute(
                dql,
                (f"%{funcao}%",)
            )
    else:
        cursor.execute(dql)

    query = cursor.fetchall()

    return query


def vagas(id_usuario):
    cursor.execute(
        "SELECT v.id, u.usuario, v.funcao, v.salario, v.cargo, v.horas, v.lugar, v.contato FROM vagas v JOIN usuarios u ON v.id_usuario = u.id WHERE v.id_usuario = (?);",
        (id_usuario,)
    )

    query = cursor.fetchall()

    return query


def vaga(id_vaga):
    cursor.execute(
        "SELECT * FROM vagas WHERE id = (?);",
        (id_vaga,)
    )

    query = cursor.fetchone()

    return query


def usuario(id_usuario):
    cursor.execute(
        "SELECT usuario FROM usuarios WHERE id = (?);",
        (id_usuario,)
    )

    query = cursor.fetchone()

    return query
