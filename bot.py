from bale import Bot, Message
from flask import Flask
from threading import Thread
import os

TOKEN = os.getenv("BALE_TOKEN", "1222383463:xE0V0qtz-K7mp45a4AStuUn8aINKvD6NUkM")

client = Bot(token=TOKEN)
app = Flask(__name__)

# دیکشنری برای ذخیره وضعیت کاربران (کی قبلاً جواب گرفته)
replied_users = set()

@app.route('/')
def home():
    return "ربات بله در حال اجراست!"

@client.event
async def on_ready():
    print(f"✅ ربات {client.user} روشن شد!")

@client.event
async def on_message(message: Message):
    user_id = message.author.id  # آیدی یکتای کاربر
    
    # فقط اگه پیام "سلام" باشه و کاربر قبلاً جواب نگرفته باشه
    if message.content and message.content.strip() == "سلام":
        if user_id not in replied_users:
            await message.reply("سلام!")
            replied_users.add(user_id)  # علامت بزن که این کاربر جواب گرفته
    # اگه دستور start بود، حافظه رو پاک کن (اختیاری)
    elif message.content and message.content.strip() == "/start":
        replied_users.discard(user_id)  # حذف کاربر از حافظه
        await message.reply("سلام! حافظه پاک شد. دوباره میتونی به من سلام کنی.")
    elif message.content and message.content.strip() != "/start":
        await message.reply("فقط به «سلام» پاسخ می‌دم. لطفاً «سلام» رو تایپ کن.")

def run_bot():
    client.run()

if __name__ == "__main__":
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
