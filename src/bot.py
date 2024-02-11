import asyncio
import logging
from aiogram import Bot, Dispatcher, types, html
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from datetime import datetime
from config_reader import config
import io
import qrcode


# Создаём переменнную с именем и местоположением qr
name = './data/qr.png'  

def qr_ascii(data):
    qr = qrcode.QRCode()
    qr.add_data(data)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    ascii_link = f.read()
    print('\nQR => \n' + ascii_link + '<=')
    
# Включаем логгирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота с SecretStr type 
bot = Bot(token=config.bot_token.get_secret_value())
# Создание диспетчера
dp = Dispatcher()
dp['started_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")

# Создание хэндлера на комманду '/start'
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Hello, {html.bold(html.quote(message.from_user.full_name))}\nДля запуска "
            "генератора используйте /generator",
        parse_mode=ParseMode.HTML,
        reply_markup=types.ReplyKeyboardRemove()
    )

# Хэндлер на комманду '/generator'
@dp.message(Command("generator"))
async def cmd_gen(message: types.Message):
    await message.answer("Отправьте ссылку")
    @dp.message()
    async def send_qr(message: types.Message):
        username = message.from_user.full_name
        print(f'\nfrom user >{username}< link => {message.text} <=\n')
        # Сюда будем помещать file_id отправленных файлов, чтобы потом ими воспользоваться
        file_ids = []
        data = message.text
        img = qrcode.make(data)
        type(img)
        filename = img.save(name)
        # Отправка файла из файловой системы
        image_from_pc = FSInputFile(name)
        result = await message.answer_photo(
            image_from_pc,
            caption=message.text + '\nОтправьте ссылку'
        )
        file_ids.append(result.photo[-1].file_id)

        qr_ascii(data)

# Хэндлер на комманду '/help'
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer('support: {0}')

# Хэндлер на комманду '/info'
@dp.message(Command("info"))
async def cmd_info(message: types.Message, started_at: str):
    await message.answer(f'Время запуска: {started_at}\nСкоро будут доступны svg и custom форматы')

# Запуск процесса полинга новый апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())