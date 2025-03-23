import requests

# URL da API pública da Coinbase para obter o preço "spot" do Bitcoin
url = 'https://api.coinbase.com/v2/prices/spot?currency=USD'

# Realizando a requisição GET para obter o preço
response = requests.get(url)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    data = response.json()
    # Pegando o preço do Bitcoin em USD
    bitcoin_price = data['data']['amount']
    print(f'O preço atual do Bitcoin é: ${bitcoin_price}')
else:
    print(f"Erro ao acessar a API da Coinbase: {response.status_code}")
