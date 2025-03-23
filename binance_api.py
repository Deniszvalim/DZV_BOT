import asyncio
import time
from binance.client import Client
from telegram import Bot
from secrets import api_key, api_secret, telegram_token, chat_id

# Conectar à API da Binance
client = Client(api_key, api_secret)

# Conectar ao Telegram
bot = Bot(token=telegram_token)

# Lista das 10 principais criptomoedas
top_10_cryptos = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", 
                   "DOGEUSDT", "SOLUSDT", "DOTUSDT", "MATICUSDT", "LTCUSDT"]

def get_crypto_prices():
    """Obtém os preços das 10 principais criptomoedas na Binance"""
    prices = []
    for symbol in top_10_cryptos:
        ticker = client.get_symbol_ticker(symbol=symbol)
        price = float(ticker["price"])
        prices.append(f"{symbol}: ${price:.2f}")
    return "\n".join(prices)

async def send_prices_to_telegram():
    """Envia as cotações para o Telegram"""
    while True:
        try:
            prices = get_crypto_prices()
            message = f"📊 *Cotações das Top 10 Criptomoedas:*\n\n{prices}"
            await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
            print("Mensagem enviada com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")

        await asyncio.sleep(60)  # Aguarda 1 minuto antes de enviar novamente

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_prices_to_telegram())
