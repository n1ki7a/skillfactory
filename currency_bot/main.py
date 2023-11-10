import telebot

from extensions import Converter, APIException
from config import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def command_help(message: telebot.types.Message):
    text = '''Чтобы начать работу введите команду боту в следующем формате:
<имя валюты> <в какую валюту перевести> <количество>'''
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def command_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров.')

        quote, base, amount = values
        result = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{amount} {quote} = {result["total"]:.2f} {base}\nЦБ РФ - {result["date"]}'
        bot.reply_to(message, text)


bot.polling()
