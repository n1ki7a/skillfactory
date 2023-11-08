import requests
import telebot


from config import *


bot = telebot.TeleBot(TOKEN)

keys = {
    'доллар': 'USD',
    'рубль': 'RUB'
}


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
    queue, base, amount = message.text.split(' ')
    r = requests.get('https://www.cbr-xml-daily.ru/latest.js')


bot.polling()
