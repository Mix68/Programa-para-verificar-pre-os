import re
import requests

# Função para validar CPF
def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = 0 if soma1 % 11 < 2 else 11 - soma1 % 11
    soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = 0 if soma2 % 11 < 2 else 11 - soma2 % 11
    return cpf[-2:] == f"{digito1}{digito2}"

# Função para validar email
def validar_email(email):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

# Função para validar telefone
def validar_telefone(telefone):
    return bool(re.match(r'^\(\d{2}\) \d{4,5}-\d{4}$', telefone))

# Função para buscar menor preço no Mercado Livre
def buscar_produto_mercadolivre(produto):
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={produto.replace(' ', '%20')}"
    resposta = requests.get(url)

    if resposta.status_code != 200:
        return None, None

    dados = resposta.json().get('results', [])
    if not dados:
        return None, None

    menor_preco = min(item['price'] for item in dados)
    link_oferta = next(item['permalink'] for item in dados if item['price'] == menor_preco)

    return menor_preco, link_oferta

# Programa principal
if __name__ == "__main__":
    nome = input("Digite seu nome completo: ")

    cpf = input("Digite seu CPF: ")
    while not validar_cpf(cpf):
        print("CPF inválido. Tente novamente.")
        cpf = input("Digite seu CPF: ")

    email = input("Digite seu email: ")
    while not validar_email(email):
        print("Email inválido. Tente novamente.")
        email = input("Digite seu email: ")

    telefone = input("Digite seu telefone (formato (99) 99999-9999): ")
    while not validar_telefone(telefone):
        print("Telefone inválido. Tente novamente.")
        telefone = input("Digite seu telefone: ")

    produto = "Teclado Yamaha PSR-E473"
    preco, link = buscar_produto_mercadolivre(produto)

    print(f"\nOlá, {nome}!")
    if preco and link:
        print(f"Produto: {produto}\nMenor Preço: R$ {preco:.2f}\nLink: {link}")
    else:
        print("Produto não encontrado.")

    # Pausa no final
    input("\nPressione Enter para sair...")
