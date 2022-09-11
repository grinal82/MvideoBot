from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
import os
import time
from dotenv import load_dotenv
from main_pagination import get_data, get_result
import json

load_dotenv()

token = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Ноутбуки', 'Планшеты']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберете категорию', reply_markup=keyboard)


@dp.message_handler(Text(equals='Ноутбуки'))
async def get_discount_laptops(message: types.Message):
    await message.answer('Please wait ....')

    get_data(category='118')
    get_result()

    with open('data/4_result.json') as file:
        data = json.load(file)

    for item in data.values():
        products = item.get('body').get('products')
        for product in products:
            product_name = product.get('name')
            url = product.get('item_link')
            full_price = product.get('item_basePrice')
            discount_price = product.get('item_salePrice')
            discount = int(100 - round((discount_price / full_price), 2) * 100)
            card = f'{hlink(product_name, url)}\n'\
            f'{hbold("Скидка: ")}{discount}%\n'\
                f'Цена со скидкой: {discount_price}!'

            await message.answer(card)


@dp.message_handler(Text(equals='Планшеты'))
async def get_discount_laptops(message: types.Message):
    await message.answer('Please wait ....')

    get_data(category='195')
    get_result()

    with open('data/4_result.json') as file:
        data = json.load(file)

    for item in data.values():
        products = item.get('body').get('products')
        for product in products:
            product_name = product.get('name')
            url = product.get('item_link')
            full_price = product.get('item_basePrice')
            discount_price = product.get('item_salePrice')
            discount = int(100 - round((discount_price / full_price), 2) * 100)
            card = f'{hlink(product_name, url)}\n'\
            f'{hbold("Скидка: ")}{discount}%\n'\
                f'Цена со скидкой: {discount_price}!'

            await message.answer(card)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
