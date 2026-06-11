from bale import Bot, Message, Update
from bale.handlers import CommandHandler
import os
from flask import Flask
from threading import Thread

# توکن ربات بله
TOKEN = os.getenv("BALE_TOKEN", "1222383463:xE0V0qtz-K7mp45a4AStuUn8aINKvD6NUkM")

# راه‌اندازی ربات
client = Bot(token=TOKEN)

# فلاسک برای نگه داشتن پورت (نیاز Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "ربات بله در حال اجراست!"

# دستور start
@client.handle(CommandHandler('start'))
async def start_command(message: Message):
    await message.reply("سلام! به ربات بله خوش اومدی. به من «سلام» بگو تا جواب بدم.")

# رویداد دریافت پیام
@client.event
async def on_message(message: Message):
    # اگه متن پیام دقیقاً "سلام" بود
    if message.content and message.content.strip() == "سلام":
        await message.reply("سلام!")
    elif message.content and message.content.strip() != "/start":
        await message.reply("فقط به «سلام» پاسخ می‌دم. لطفاً «سلام» رو تایپ کن.")

# رویداد آماده شدن ربات
@client.event
async def on_ready():
    print(f"ربات {client.user} آماده کار است!")

def run_bot():
    client.run()

if __name__ == "__main__":
    # اجرای ربات در ترد جداگانه
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    
    # اجرای فلاسک برای Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
