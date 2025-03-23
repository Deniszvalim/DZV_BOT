import requests

# Lista das 10 principais criptomoedas com os pares "USDT"
top_10_cryptos = [
    "XBTUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", 
    "DOGEUSDT", "SOLUSDT", "DOTUSDT", "MATICUSDT", "LTCUSDT"
]

# Base URL da API pública da Kraken
url = 'https://api.kraken.com/0/public/Ticker'

# Função para obter o preço de cada criptomoeda
def get_crypto_prices(cryptos):
    prices = {}
    for crypto in cryptos:
        response = requests.get(url, params={'pair': crypto})
        
        if response.status_code == 200:
            data = response.json()
            prices[crypto] = data['result'][list(data['result'].keys())[0]]['c'][0]
        else:
            prices[crypto] = 'Erro'
    
    return prices

# Obtendo os preços das criptomoedas
prices = get_crypto_prices(top_10_cryptos)

# Exibindo os preços
for crypto, price in prices.items():
    print(f'O preço de {crypto} é: ${price}')
