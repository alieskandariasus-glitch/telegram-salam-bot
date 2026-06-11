from balebot.models.messages import TextMessage
from balebot.updater import Updater
from balebot.handlers import MessageHandler, CommandHandler
import os

# توکن ربات بله (از متغیر محیطی یا مستقیم)
TOKEN = os.getenv("BALE_TOKEN", "1222383463:xE0V0qtz-K7mp45a4AStuUn8aINKvD6NUkM")

# راه‌اندازی ربات
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# دستور start
def start_handler(bot, update):
    bot.reply(update, "سلام! به ربات بله خوش اومدی. به من «سلام» بگو تا جواب بدم.")

start_command = CommandHandler("start", start_handler)
dispatcher.register_handler(start_command)

# پاسخ به "سلام"
def say_hello(bot, update):
    message = update.get_effective_message()
    if message.text and message.text.strip() == "سلام":
        bot.reply(update, "سلام!")
    else:
        bot.reply(update, "فقط به «سلام» پاسخ می‌دم. لطفاً «سلام» رو تایپ کن.")

message_handler = MessageHandler(TextMessage, say_hello)
dispatcher.register_handler(message_handler)

# راه‌اندازی وب‌هوک برای Render (نیاز به Flask)
from flask import Flask, request
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    update = request.get_json()
    updater.dispatcher.process_update(update)
    return "OK"

@app.route('/')
def home():
    return "ربات بله در حال اجراست!"

if __name__ == "__main__":
    # ثبت وب‌هوک
    updater.start_webhook(listen="0.0.0.0", port=int(os.environ.get("PORT", 5000)), url_path=TOKEN)
    updater.bot.set_webhook(f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
