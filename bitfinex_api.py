import requests

# Lista das 10 principais criptomoedas com os pares "USDT"
top_10_cryptos = [
    "btcusdt", "ethusdt", "bnbusdt", "xrpusdt", "adausdt", 
    "dogeusdt", "solusdt", "dotusdt", "maticusdt", "ltcusdt"
]

# Base URL da API pública da Bitfinex
url = 'https://api.bitfinex.com/v1/pubticker'

# Função para obter o preço de cada criptomoeda
def get_crypto_prices(cryptos):
    prices = {}
    for crypto in cryptos:
        response = requests.get(f"{url}/{crypto}")
        
        if response.status_code == 200:
            data = response.json()
            prices[crypto] = data['last_price']
        else:
            prices[crypto] = 'Erro'
    
    return prices

# Obtendo os preços das criptomoedas
prices = get_crypto_prices(top_10_cryptos)

# Exibindo os preços
for crypto, price in prices.items():
    print(f'O preço de {crypto} é: ${price}')
