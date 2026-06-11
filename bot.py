import telebot
import os
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "ربات در حال اجراست!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! به ربات خوش اومدی. به من «سلام» بگو تا جواب بدم.")

@bot.message_handler(func=lambda message: message.text and message.text.strip() == "سلام")
def say_hello(message):
    bot.reply_to(message, "سلام!")

@bot.message_handler(func=lambda message: True)
def other_messages(message):
    bot.reply_to(message, "فقط به «سلام» پاسخ می‌دم. لطفاً «سلام» رو تایپ کن.")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
