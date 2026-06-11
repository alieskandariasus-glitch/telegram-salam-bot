from bale import Bot, Message
from flask import Flask
from threading import Thread
import os
import time

TOKEN = os.getenv("BALE_TOKEN", "1222383463:xE0V0qtz-K7mp45a4AStuUn8aINKvD6NUkM")

client = Bot(token=TOKEN)
app = Flask(__name__)

# حافظه برای جلوگیری از پردازش تکراری
processed_messages = {}  # {message_id: time}
replied_users = []       # کاربرانی که جواب گرفتن

@app.route('/')
def home():
    return "ربات بله در حال اجراست!"

@client.event
async def on_ready():
    print(f"✅ ربات {client.user} روشن شد!")

@client.event
async def on_message(message: Message):
    # === روش جلوگیری از پردازش تکراری ===
    msg_id = str(message.id)  # آیدی یکتای پیام
    
    # اگه این پیام قبلاً پردازش شده، بیخیال شو
    if msg_id in processed_messages:
        return
    processed_messages[msg_id] = time.time()
    
    # پاک کردن خودکار حافظه هر 5 دقیقه
    if len(processed_messages) > 100:
        current_time = time.time()
        to_delete = [mid for mid, t in processed_messages.items() if current_time - t > 300]
        for mid in to_delete:
            del processed_messages[mid]
    
    # === منطق اصلی ربات ===
    user_id = message.chat.id
    text = message.text
    
    # دستور start - فقط یک بار پیام بده
    if text == "/start":
        # اگه قبلاً این کاربر توی replied_users هست، پاکش کن
        if user_id in replied_users:
            replied_users.remove(user_id)
        # فقط یک بار پیام بده
        await message.reply("سلام! حافظه پاک شد. میتونی یه بار به من سلام کنی.")
        return
    
    # پیام سلام - فقط اگه قبلاً جواب نداده باشیم
    if text == "سلام" and user_id not in replied_users:
        await message.reply("سلام!")
        replied_users.append(user_id)
        return
    
    # اگه پیام دیگه‌ای بود (نه start و نه سلام)
    if text != "/start" and text != "سلام":
        await message.reply("فقط به «سلام» پاسخ میدم. «سلام» رو تایپ کن.")

def run_bot():
    client.run()

if __name__ == "__main__":
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
