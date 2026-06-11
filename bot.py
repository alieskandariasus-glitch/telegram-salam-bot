from bale import Bot, Message
from flask import Flask
from threading import Thread
import os

TOKEN = os.getenv("BALE_TOKEN", "1222383463:xE0V0qtz-K7mp45a4AStuUn8aINKvD6NUkM")

client = Bot(token=TOKEN)
app = Flask(__name__)

# اینجا یادمون میاد به کیا جواب دادیم
already_replied = []

@app.route('/')
def home():
    return "ربات بله در حال اجراست!"

@client.event
async def on_ready():
    print(f"✅ ربات {client.user} روشن شد!")

@client.event
async def on_message(message: Message):
    # ایدی کاربر رو میگیریم
    user_id = message.chat.id
    
    # اگه پیام "سلام" بود و قبلاً به این کاربر جواب نداده بودیم
    if message.text == "سلام" and user_id not in already_replied:
        await message.reply("سلام!")
        already_replied.append(user_id)  # یادمون میاد به این کاربر جواب دادیم
    
    # اگه کاربر start زد، اجازه میدیم دوباره بتونه سلام کنه
    elif message.text == "/start":
        if user_id in already_replied:
            already_replied.remove(user_id)
        await message.reply("سلام! حافظه پاک شد. میتونی یه بار دیگه به من سلام کنی.")
    
    # اگه چیز دیگه ای فرستاد (به جز سلام و start)
    elif message.text != "/start" and message.text != "سلام":
        await message.reply("فقط به «سلام» پاسخ میدم. «سلام» رو تایپ کن.")

def run_bot():
    client.run()

if __name__ == "__main__":
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
