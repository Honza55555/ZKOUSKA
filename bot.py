import os
import telebot
from flask import Flask, request

# Získání tokenu z environment variable
TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# Reakce na /start a /help příkaz
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Ahoj! Jsem jednoduchý Telegram bot.")

# Webhook endpoint pro Telegram
@server.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'OK', 200

# Hlavní stránka, která potvrzuje, že bot běží
@server.route("/")
def index():
    return "Bot běží!", 200

if __name__ == "__main__":
    # Nastavení webhooku
    bot.remove_webhook()
    bot.set_webhook(url=f"{os.environ.get('RENDER_URL')}/{TOKEN}")
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
