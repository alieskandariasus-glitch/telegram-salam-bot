from bale import Bot, Message
from flask import Flask
from threading import Thread
import os

TOKEN = os.getenv("BALE_TOKEN", "1222383463:xE0V0qtz-K7mp45a4AStuUn8aINKvD6NUkM")

client = Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "ربات بله در حال اجراست!"

@client.event
async def on_ready():
    print(f"✅ ربات {client.user} روشن شد!")

@client.event
async def on_message(message: Message):
    # فقط اگه متن پیام برابر با "سلام" بود، جواب بده
    if message.text == "سلام":
        await message.reply("سلام!")
    # اگه دستور start بود خوش‌آمدگویی کن
    elif message.text == "/start":
        await message.reply("سلام! به ربات خوش اومدی. «سلام» بگو تا جواب بدم.")

def run_bot():
    client.run()

if __name__ == "__main__":
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
