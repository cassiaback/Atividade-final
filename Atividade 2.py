import requests

login = []

def menu():
    """
    Exibe o menu principal e executa as ações com base na opção escolhida pelo usuário.
    """
    while True:
        print("-" * 90)
        print("MENU".center(90))
        print("-" * 90)
        print("0 - Sair")
        print("1 - Entrar com user")
        print("2 - Adicionar user")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "0":
            print("\nEncerrando o programa.")
            break
        elif opcao == "1":
            print("\nVocê escolheu: Entrar com user")
            if usuario():
                break
        elif opcao == "2":
            print("\nVocê escolheu: Adicionar user")
            adicionar_user()
        else:
            print("\nOpção inválida. Tente novamente.")

    return opcao


def usuario():
    """
    Função para permitir que o usuário faça login com o email e senha.
    """
    email = input("\nDigite o e-mail: ")
    senha = input("Digite a senha: ")

    for user in login:
        if user["email"] == email and user["senha"] == senha:
            print(f"\nLogin bem-sucedido! Bem-vindo(a), {user['nome']}.")
            menu_usuario_logado(user)
            return True
    print("\nE-mail ou senha incorretos. Tente novamente.")
    return False


def adicionar_user():
    """
    Função para adicionar um novo usuário à lista.
    """
    print("\n\n")
    print("-" * 90)
    nome = input("\nDigite o nome do usuário: ")
    email = input("\nDigite o e-mail do usuário: ")
    senha = input("\nDigite uma senha de acesso: ")
    print("-" * 90)

    user = {"nome": nome, "email": email, "senha": senha, "id": len(login) + 1}
    login.append(user)
    print(f"User {nome} adicionado(a) com sucesso!")


def visualizar_posts(user_id=None):
    """
    Mostra posts da API. Se for passado um user_id, filtra os posts por esse usuário.
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    if user_id:
        url += f"?userId={user_id}"

    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            posts = resposta.json()
            print(f"\n--- Exibindo {len(posts)} post(s) ---")
            for post in posts:
                print(f"\nID: {post['id']}")
                print(f"Título: {post['title']}")
                print(f"Conteúdo: {post['body']}")
        else:
            print("Erro ao buscar posts.")
    except Exception as e:
        print("Erro na requisição:", e)


def criar_post(user_id):
    """
    Permite que o usuário crie um novo post (simulado via API).
    """
    print("\n\n" + "--- Criar novo post ---".center(50))
    titulo = input("\n\nTítulo do post: ")
    corpo = input("Conteúdo do post: ")

    novo_post = {
        "title": titulo,
        "body": corpo,
        "userId": user_id
    }

    try:
        resposta = requests.post("https://jsonplaceholder.typicode.com/posts", json=novo_post)
        if resposta.status_code == 201:
            post_criado = resposta.json()
            print("\nPost criado com sucesso!")
            print(f"ID do novo post: {post_criado['id']}")
        else:
            print("Erro ao criar post.")
    except Exception as e:
        print("Erro na requisição:", e)


def visualizar_comentarios():
    """
    Permite visualizar comentários de um post específico.
    """
    post_id = input("Digite o ID do post para ver os comentários: ")

    if not post_id.isdigit():
        print("ID inválido. Use apenas números.")
        return

    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"

    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            comentarios = resposta.json()
            print(f"\n--- Comentários do post {post_id} ---")
            for comentario in comentarios:
                print(f"\nNome: {comentario['name']}")
                print(f"Email: {comentario['email']}")
                print(f"Comentário: {comentario['body']}")
        else:
            print("Erro ao buscar comentários.")
    except Exception as e:
        print("Erro na requisição:", e)


def menu_usuario_logado(usuario_logado):
    """
    Exibe o menu de ações disponíveis após login.
    """
    interacoes = {
        "posts_visualizados": 0,
        "comentarios_visualizados": 0,
        "posts_criados": 0
    }

    while True:
        print("\n\n" + "--- MENU DO USUÁRIO ---".center(50))
        print(f"\nUsuário logado: {usuario_logado['nome']}")
        print("\n\n1 - Ver todos os posts")
        print("2 - Ver meus posts")
        print("3 - Ver posts de outro usuário")
        print("4 - Criar novo post")
        print("5 - Ver comentários de um post")
        print("6 - Sair e ver resumo")
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            visualizar_posts()
            interacoes["posts_visualizados"] += 1

        elif opcao == "2":
            visualizar_posts(usuario_logado["id"])
            interacoes["posts_visualizados"] += 1

        elif opcao == "3":
            outro_id = input("Digite o ID do outro usuário: ")
            if outro_id.isdigit():
                visualizar_posts(int(outro_id))
                interacoes["posts_visualizados"] += 1
            else:
                print("ID inválido.")

        elif opcao == "4":
            criar_post(usuario_logado["id"])
            interacoes["posts_criados"] += 1

        elif opcao == "5":
            visualizar_comentarios()
            interacoes["comentarios_visualizados"] += 1

        elif opcao == "6":
            print("\nResumo da sessão:")
            print(f"- Posts visualizados: {interacoes['posts_visualizados']}")
            print(f"- Comentários visualizados: {interacoes['comentarios_visualizados']}")
            print(f"- Posts criados: {interacoes['posts_criados']}")
            break
        else:
            print("Opção inválida.")


# Início do programa
while True:
    opcao = menu()
    if opcao == "0":
        break
