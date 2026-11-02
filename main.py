import os
import threading
from flask import Flask
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Merhaba! Mesajını yaz.")

@bot.message_handler(func=lambda m: True)
def forward_to_admin(message):
    if message.from_user.id == ADMIN_ID:
        return
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, f"ID: {message.from_user.id}")
    bot.reply_to(message, "İletildi!")

@bot.message_handler(func=lambda message: message.reply_to_message is not None)
def reply_to_user(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        if message.reply_to_message.forward_from:
            user_id = message.reply_to_message.forward_from.id
            bot.send_message(user_id, f"Destek: {message.text}")
            bot.reply_to(message, "Gönderildi!")
    except Exception as e:
        bot.reply_to(message, f"Hata: {e}")

@app.route('/')
def home():
    return "Bot Canlı!"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
