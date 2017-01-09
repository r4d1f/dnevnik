# -*- coding: utf-8 -*-
import config
import telebot
import dnevnik
import requests
import time
dict ={}
dict1={}
bot = telebot.TeleBot(config.token)
@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, 'Для начала работы введите логин и пароль в следующем виде\nlogin:password\nА затем выберите день недели')

@bot.message_handler(commands = ['help'])
def helpcom(message):
    bot.send_message(message.chat.id, 'При получении ошибки проверьте правильность введенных данных. Для разделения логина и пароля используйте только двоеточие(:).Для связи используйте команду /contact')

@bot.message_handler(commands = ['contact'])
def contact(message):
    bot.send_message(message.chat.id, 'Почта: radif.47@gmail.com\nТелеграм: telegram.me/r4d1f')

def day(rasp, numday):
    trasp = rasp[numday]
    day_text = ''
    for x in trasp:
        day_text = day_text + x + ', '
    if day_text == '':
        day_text = 'Ничего'
    else:
        day_text = day_text[:-2]
    return day_text
    
@bot.message_handler(content_types = ['text'])
def logpass(message):
    if ':' in message.text:
        logp = message.text.split(':')
        login = logp[0]
        password = logp[1]
        dict[message.chat.id] = [login, password]
        dict1[message.chat.id] = dnevnik.main(dict, message.chat.id)
        if dict1[message.chat.id] == False:
            bot.send_message(message.chat.id, 'Ошибка, повторите попытку')
        else:
            user_markup = telebot.types.ReplyKeyboardMarkup(True)
            user_markup.row('Понедельник', 'Вторник')
            user_markup.row('Среда', 'Четверг')
            user_markup.row('Пятница', 'Суббота')
            bot.send_message(message.chat.id, 'Успешно', reply_markup = user_markup)
    else:
        try:
            if message.text == 'Понедельник':
                bot.send_message(message.chat.id, 'Понедельник: %s' % (day(dict1[message.chat.id], 0)) )
            elif message.text == 'Вторник':
                bot.send_message(message.chat.id, 'Вторник: %s' % (day(dict1[message.chat.id], 1)))
            elif message.text == 'Среда':
                bot.send_message(message.chat.id, 'Среда: %s' % (day(dict1[message.chat.id], 2)))
            elif message.text == 'Четверг':
                bot.send_message(message.chat.id, 'Четверг: %s' % (day(dict1[message.chat.id], 3)))
            elif message.text == 'Пятница':
                bot.send_message(message.chat.id, 'Пятница: %s' % (day(dict1[message.chat.id], 4)))
            elif message.text == 'Суббота':
                bot.send_message(message.chat.id, 'Суббота: %s' % (day(dict1[message.chat.id], 5)))
        except NameError and KeyError:
            bot.send_message(message.chat.id, 'Сначала авторизуйтесь')
    

        
if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except requests.exceptions.ReadTimeout:
        pass