from bale import Bot, Message
from flask import Flask
from threading import Thread
import os
import time

TOKEN = os.getenv("BALE_TOKEN", "1222383463:xE0V0qtz-K7mp45a4AStuUn8aINKvD6NUkM")

client = Bot(token=TOKEN)
app = Flask(__name__)

# دیکشنری برای ذخیره زمان آخرین پاسخ به هر کاربر
last_reply_time = {}

@app.route('/')
def home():
    return "ربات بله در حال اجراست!"

@client.event
async def on_ready():
    print(f"✅ ربات {client.user} روشن شد!")

@client.event
async def on_message(message: Message):
    # روش اول: استفاده از chat_id (معمولاً پایدارتر است)
    user_id = str(message.chat.id)  # تبدیل به رشته برای دیکشنری
    
    current_time = time.time()
    last_time = last_reply_time.get(user_id, 0)
    
    # فقط اگر پیام "سلام" باشد و آخرین پاسخ بیش از 10 ثانیه پیش بوده
    if message.content and message.content.strip() == "سلام":
        if current_time - last_time > 10:  # هر 10 ثانیه فقط یک بار پاسخ بده
            await message.reply("سلام!")
            last_reply_time[user_id] = current_time
            print(f"به کاربر {user_id} پاسخ داده شد")
        else:
            print(f"کاربر {user_id} در زمان کوتاه دوباره سلام کرد - پاسخ داده نشد")
    
    elif message.content and message.content.strip() == "/start":
        # ریست کردن زمان آخرین پاسخ برای این کاربر
        last_reply_time[user_id] = 0
        await message.reply("سلام! حافظه پاک شد. می‌توانی دوباره سلام کنی.")
    
    elif message.content and message.content.strip() != "/start":
        await message.reply("فقط به «سلام» پاسخ می‌دم. لطفاً «سلام» رو تایپ کن.")

def run_bot():
    client.run()

if __name__ == "__main__":
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
