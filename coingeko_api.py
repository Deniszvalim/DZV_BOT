import requests

# Lista das 10 principais criptomoedas no formato de ids do CoinGecko
top_10_cryptos = [
    "bitcoin", "ethereum", "binancecoin", "ripple", "cardano", 
    "dogecoin", "solana", "polkadot", "matic-network", "litecoin"
]

# Base URL da API do CoinGecko
url = 'https://api.coingecko.com/api/v3/simple/price'

# Função para obter o preço de cada criptomoeda
def get_crypto_prices(cryptos):
    crypto_ids = ','.join(cryptos)
    response = requests.get(url, params={'ids': crypto_ids, 'vs_currencies': 'usd'})
    
    if response.status_code == 200:
        data = response.json()
        return {crypto: data[crypto]['usd'] for crypto in cryptos}
    else:
        return {'Error': 'Unable to fetch data'}

# Obtendo os preços das criptomoedas
prices = get_crypto_prices(top_10_cryptos)

# Exibindo os preços
for crypto, price in prices.items():
    print(f'O preço de {crypto} é: ${price}')
