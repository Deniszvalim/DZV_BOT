import asyncio
import time
import requests
from binance.client import Client
from telegram import Bot
from secrets import api_key, api_secret, telegram_token, chat_id

# Conectar à API da Binance
binance_client = Client(api_key, api_secret)

# Conectar ao Telegram
bot = Bot(token=telegram_token)

# Lista das 10 principais criptomoedas
top_10_cryptos = ["XRPUSDT", "SOLUSDT"]

# Função para obter os preços da Binance
def get_binance_prices():
    prices = {}
    for symbol in top_10_cryptos:
        ticker = binance_client.get_symbol_ticker(symbol=symbol)
        price = float(ticker["price"])
        prices[symbol] = price
    return prices

# Função para obter os preços da Coinbase
def get_coinbase_prices():
    prices = {}
    for symbol in top_10_cryptos:
        coin_id = symbol.split("USDT")[0]  # Ex: 'BTC', 'ETH', etc.
        url = f'https://api.coinbase.com/v2/prices/{coin_id}-USD/spot'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'amount' in data['data']:
                price = float(data['data']['amount'])
                prices[symbol] = price
            else:
                prices[symbol] = None
        else:
            prices[symbol] = None
    return prices

# Função para obter os preços da KuCoin
def get_kucoin_prices():
    prices = {}
    for symbol in top_10_cryptos:
        coin_id = symbol.replace("USDT", "")
        url = f'https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={coin_id}-USDT'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'price' in data['data']:
                price = float(data['data']['price'])
                prices[symbol] = price
            else:
                prices[symbol] = None
        else:
            prices[symbol] = None
    return prices

# Função para obter os preços da Bitfinex
def get_bitfinex_prices():
    prices = {}
    for symbol in top_10_cryptos:
        coin_id = symbol.replace("USDT", "")
        url = f'https://api.bitfinex.com/v1/pubticker/{coin_id}usd'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'last_price' in data:
                price = float(data['last_price'])
                prices[symbol] = price
            else:
                prices[symbol] = None
        else:
            prices[symbol] = None
    return prices

# Função para coletar os preços de todas as corretoras
async def get_all_prices():
    binance_prices = await asyncio.to_thread(get_binance_prices)
    coinbase_prices = await asyncio.to_thread(get_coinbase_prices)
    kucoin_prices = await asyncio.to_thread(get_kucoin_prices)
    bitfinex_prices = await asyncio.to_thread(get_bitfinex_prices)
    
    return binance_prices, coinbase_prices, kucoin_prices, bitfinex_prices

# Função para calcular os valores de compra, venda e a diferença
def calculate_buy_sell_difference(binance_prices, coinbase_prices, kucoin_prices, bitfinex_prices):
    result = {}
    
    for crypto in top_10_cryptos:
        prices = {
            'binance': binance_prices.get(crypto),
            'coinbase': coinbase_prices.get(crypto),
            'kucoin': kucoin_prices.get(crypto),
            'bitfinex': bitfinex_prices.get(crypto)
        }
        
        # Filtrar preços não nulos
        valid_prices = {k: v for k, v in prices.items() if v is not None}
        
        if valid_prices:
            buy_price = min(valid_prices.values())  # Menor preço = Compra
            sell_price = max(valid_prices.values())  # Maior preço = Venda
            price_difference = sell_price - buy_price  # Diferença entre venda e compra
            
            # Simulações de lucro
            simulations = {
                "2000 unidades": price_difference * 2000,
                "5000 unidades": price_difference * 5000,
                "10000 unidades": price_difference * 10000
            }
            
            result[crypto] = {
                'buy_price': buy_price,
                'sell_price': sell_price,
                'price_difference': price_difference,
                'simulations': simulations
            }
    
    return result


# Função para comparar as cotações e enviar para o Telegram
async def send_prices_to_telegram():
    """Envia as cotações para o Telegram após compará-las"""
    while True:
        try:
            # Coleta os preços de todas as corretoras
            binance_prices, coinbase_prices, kucoin_prices, bitfinex_prices = await get_all_prices()

            # Formata a mensagem para o Telegram
            message = "📊 *Cotações Criptomoedas - Denis Valim:*\n\n"
            for crypto in top_10_cryptos:
                # Obtém os preços de cada corretora
                binance_price = binance_prices[crypto]
                coinbase_price = coinbase_prices[crypto]
                kucoin_price = kucoin_prices[crypto]
                bitfinex_price = bitfinex_prices[crypto]

                # Cria um dicionário para associar os preços às corretoras
                prices = {
                    'Binance': binance_price,
                    'Coinbase': coinbase_price,
                    'KuCoin': kucoin_price,
                    'Bitfinex': bitfinex_price
                }

                # Encontra o menor preço (compra) e o maior preço (venda)
                min_price = min(prices, key=prices.get)
                max_price = max(prices, key=prices.get)

                min_price_value = prices[min_price]
                max_price_value = prices[max_price]

                # Calcula a diferença entre os preços de venda e compra
                price_difference = max_price_value - min_price_value

                # Simulações com base na diferença de preço
                sim_500 = price_difference * 500
                sim_1000 = price_difference * 1000
                sim_10000 = price_difference * 10000

                # Formata a mensagem com as cotações e simulações
                message += f"📈 {crypto}:\n"
                for exchange, price in prices.items():
                    message += f"  - {exchange}:   ${price:.2f}\n"

                message += f"\n💸 Compra ({min_price}):   ${min_price_value:.2f}\n"
                message += f"💰 Venda ({max_price}):   ${max_price_value:.2f}\n"
                message += f"📉 Diferença:   ${price_difference:.2f}\n\n"
                
                message += f"💡 Simulações:\n"
                message += f"     500 Dif.:   ${sim_500:.2f}\n"
                message += f"     1000 Dif.:   ${sim_1000:.2f}\n"
                #message += f"   10000 Dif.:   ${sim_10000:.2f}\n"

                message += f"------------------------------------------------------\n\n"

            # Envia a mensagem para o Telegram
            await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
            print("Mensagem enviada com sucesso!")

        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")

        # Aguarda 1 minuto antes de enviar novamente
        Time_of_interval = 3 * 60 # 5 minutos
        await asyncio.sleep(Time_of_interval)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_prices_to_telegram())
