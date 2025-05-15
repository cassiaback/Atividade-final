import requests
import os
from dotenv import load_dotenv

load_dotenv()

noticias_pesquisadas = []


def buscar_noticias(noticias, tema):

    api_key = os.getenv("API_KEY_NEWS")

    if not api_key:
        raise ValueError("API Key não encontrada nas variáveis "
                        "de ambiente.")

    url = "https://newsapi.org/v2/everything"

    headers = {
        'X-Api-Key': api_key
    }

    params = {
        'q': tema,
        'language': "pt",
        'page': 2
    }

    resposta = requests.get(url=url, headers=headers, params=params)
    print(resposta.status_code)

    resposta_json = resposta.json()

    #print("Site da notícia de posição 7:", resposta_json["articles"][7]["source"]["name"])

    titulos = []

    for artigo in resposta_json["articles"][:noticias]:
        print("\n" + "-" * 90)
        print("Título:", artigo["title"])
        print("\nDescrição:", artigo["description"])
        print("\nURL:", artigo["url"])
        print("-" * 90)
    
        titulos.append(artigo["title"])

    return titulos

def menu():
    """
    Exibe o menu principal e retorna a opção escolhida pelo usuário.
    """
    print("\n\n\n" + "-" * 90)
    print("Menu de opções:")
    print("-" * 90)
    print("0 - Sair")
    print("1 - Ver notícias:")

 
    while True:
        opcao = input("\nEscolha uma opção: ").strip()
        if opcao in {"0", "1"}:
            return opcao
        else:
            print("\nOpção inválida. Tente novamente.")

# Loop principal
while True:
    opcao = menu()

    if opcao == "0":
        print("\nEncerrando o programa.")
        print("\nHistórico de Pesquisas:\n")

        if not noticias_pesquisadas:
            print("Nenhuma notícia foi pesquisada.")
        else:
            for i, item in enumerate(noticias_pesquisadas, 1):
                print("-" * 90)
                print(f"Busca {i}")
                print(f"Tema: {item['tema']}")
                print(f"Quantidade de notícias: {item['quantidade']}")
                print("Títulos:")
                for titulo in item["titulos"]:
                    print(f" - {titulo}")
                print("-" * 90)
        break

    elif opcao == "1":
        try:
            quantidade = int(input("\n\nQuantas notícias você quer ver? "))
            tema = input("\n\nQual tema você gostaria de ver? ")

            titulos = buscar_noticias(quantidade, tema)

            # Salva a busca no histórico
            noticias_pesquisadas.append({
                "tema": tema,
                "quantidade": len(titulos),
                "titulos": titulos
            })

        except ValueError:
            print("Entrada inválida. Por favor, insira números válidos para a quantidade.")