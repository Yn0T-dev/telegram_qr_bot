import asyncio
import aiogram
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BufferedInputFile, InputFile
import qrcode.image.pil
import qrcode.image.svg
from config_reader import config
from io import BytesIO

dp = aiogram.Dispatcher()
bot = aiogram.Bot(token=config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        "👋 <b>Привет!</b>\nДоступные форматы: png, svg\nИспользование: <code>/qr https://google.com png</code>"
        )
    

@dp.message(Command('qr'))
async def command_qr_handler(message: Message):
    cmd: str = message.text
    args = cmd.split(" ")
    if len(args) != 3:
        await message.reply("Неправильное использование команды")

    bio = BytesIO()

    if args[2] == "png":
        img: qrcode.image.pil.PilImage = qrcode.make(args[1]) # type:ignor
        bio.name = "image.png"
        img.save(bio, "png")
    if args[2] == "svg":
        factory = qrcode.image.svg.SvgPathImage
        img: qrcode.image.svg.SvgPathImage = qrcode.make(args[1], image_factory=factory) 
        bio.name = "image.svg"
        img.save(bio)

    bio.seek(0)

    await bot.send_document(
        message.chat.id, document=BufferedInputFile(bio.read(), filename=bio.name)
    )


async def main() -> None:
    print("Starting")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
