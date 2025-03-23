import requests

# Lista das 10 principais criptomoedas com os pares "BRL" (Real Brasileiro)
top_10_cryptos = [
    "BTC-BRL", "ETH-BRL", "BNB-BRL", "XRP-BRL", "ADA-BRL",
    "DOGE-BRL", "SOL-BRL", "DOT-BRL", "MATIC-BRL", "LTC-BRL"
]

# Base URL da API pública do Mercado Bitcoin
url = 'https://www.mercadobitcoin.net/api/v3/tickers'

# Função para obter o preço de cada criptomoeda
def get_crypto_prices(cryptos):
    prices = {}
    for crypto in cryptos:
        response = requests.get(f"{url}/{crypto}")
        
        if response.status_code == 200:
            data = response.json()
            prices[crypto] = data['ticker']['buy']  # Pegando o preço de compra
        else:
            prices[crypto] = 'Erro'
    
    return prices

# Obtendo os preços das criptomoedas
prices = get_crypto_prices(top_10_cryptos)

# Exibindo os preços
for crypto, price in prices.items():
    print(f'O preço de {crypto} é: R${price}')
