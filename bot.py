import asyncio
from aiobale import Bot, Dispatcher
from aiobale.types import Message
from aiobale.filters import Command

# توکن رباتت
API_TOKEN = "1222383463:xE0V0qtz-K7mp45a4AStuUn8aINKvD6NUkM"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# دستور start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.reply("سلام! به ربات بله خوش اومدی. به من «سلام» بگو تا جواب بدم.")

# پاسخ به "سلام"
@dp.message()
async def say_hello(message: Message):
    if message.text and message.text.strip() == "سلام":
        await message.reply("سلام!")
    else:
        await message.reply("فقط به «سلام» پاسخ می‌دم. لطفاً «سلام» رو تایپ کن.")

async def main():
    print("ربات بله در حال اجراست...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
