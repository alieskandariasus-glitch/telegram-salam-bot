from bale import Bot, Message
from flask import Flask
from threading import Thread
import os

# توکن ربات بله (از متغیر محیطی می‌خواند)
TOKEN = os.getenv("BALE_TOKEN", "1222383463:xE0V0qtz-K7mp45a4AStuUn8aINKvD6NUkM")

# راه‌اندازی ربات و فلاسک (برای نگهداشتن پورت روی Render)
client = Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "ربات بله در حال اجراست!"

# --- رویدادهای ربات ---

# رویداد آماده‌شدن ربات
@client.event
async def on_ready():
    print(f"✅ ربات {client.user} با موفقیت روشن شد!")

# رویداد دریافت هر پیام جدید
@client.event
async def on_message(message: Message):
    # اگر متن پیام دقیقاً "سلام" بود
    if message.content and message.content.strip() == "سلام":
        await message.reply("سلام!")
    # اگر پیام حاوی متن بود و "سلام" نبود (به جز دستور start)
    elif message.content and message.content.strip() != "/start":
        await message.reply("فقط به «سلام» پاسخ می‌دم. لطفاً «سلام» رو تایپ کن.")

# --- اجرای ربات در یک ترد جداگانه برای Render ---
def run_bot():
    client.run()

if __name__ == "__main__":
    # اجرای ربات در پس‌زمینه
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    
    # اجرای سرور فلاسک برای نگهداشتن پورت Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
