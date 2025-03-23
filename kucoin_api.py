import requests

# Lista das 10 principais criptomoedas com os pares "USDT"
top_10_cryptos = [
    "BTC-USDT", "ETH-USDT", "BNB-USDT", "XRP-USDT", "ADA-USDT", 
    "DOGE-USDT", "SOL-USDT", "DOT-USDT", "MATIC-USDT", "LTC-USDT"
]

# Base URL da API pública da KuCoin para obter o preço
url = 'https://api.kucoin.com/api/v1/market/orderbook/level1'

# Função para obter o preço de cada criptomoeda
def get_crypto_prices(cryptos):
    prices = {}
    for crypto in cryptos:
        response = requests.get(url, params={'symbol': crypto})
        
        if response.status_code == 200:
            data = response.json()
            prices[crypto] = data['data']['price']
        else:
            prices[crypto] = 'Erro'
    
    return prices

# Obtendo os preços das criptomoedas
prices = get_crypto_prices(top_10_cryptos)

# Exibindo os preços
for crypto, price in prices.items():
    print(f'O preço de {crypto} é: ${price}')
