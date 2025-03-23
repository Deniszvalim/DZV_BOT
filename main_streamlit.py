import streamlit as st
import asyncio
import time
import requests
from binance.client import Client
from telegram import Bot

api_key = st.secrets["api_key"]
api_secret = st.secrets["api_secret"]
telegram_token = st.secrets["telegram_token"]
chat_id = st.secrets["chat_id"]

# Conectar à API da Binance
binance_client = Client(api_key, api_secret)

# Conectar ao Telegram
bot = Bot(token=telegram_token)

# Lista das 10 principais criptomoedas
top_10_cryptos = ["BTCUSDT","XRPUSDT", "SOLUSDT"]

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
        coin_id = symbol.split("USDT")[0]
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

# Interface no Streamlit
st.title("📊 Cotações Criptomoedas")
st.write("Atualização a cada 10 minutos.")

async def main():
    while True:
        binance_prices, coinbase_prices, kucoin_prices, bitfinex_prices = await get_all_prices()
        message = ""
        
        for crypto in top_10_cryptos:
            binance_price = binance_prices.get(crypto, "N/A")
            coinbase_price = coinbase_prices.get(crypto, "N/A")
            kucoin_price = kucoin_prices.get(crypto, "N/A")
            bitfinex_price = bitfinex_prices.get(crypto, "N/A")
            
            prices = {
                'Binance': binance_price,
                'Coinbase': coinbase_price,
                'KuCoin': kucoin_price,
                'Bitfinex': bitfinex_price
            }
            
            min_price = min(prices, key=prices.get)
            max_price = max(prices, key=prices.get)
            
            min_price_value = prices[min_price]
            max_price_value = prices[max_price]
            price_difference = max_price_value - min_price_value
            
            sim_500 = price_difference * 500
            sim_1000 = price_difference * 1000
            
            message += f"\n📈 {crypto}:\n"
            for exchange, price in prices.items():
                message += f"  - {exchange}: ${price:.2f}\n"
            
            message += f"\n💸 Compra ({min_price}): ${min_price_value:.2f}\n"
            message += f"💰 Venda ({max_price}): ${max_price_value:.2f}\n"
            message += f"📉 Diferença: ${price_difference:.2f}\n\n"
            message += f"💡 Simulações:\n"
            message += f"  500 Dif.: ${sim_500:.2f}\n"
            message += f"  1000 Dif.: ${sim_1000:.2f}\n"
            message += f"------------------------------------------------------\n\n"
        
        st.text_area("Cotações Atualizadas:", message, height=400)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
        await asyncio.sleep(600)

if __name__ == "__main__":
    asyncio.run(main())
