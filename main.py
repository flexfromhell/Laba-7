import telebot
import psycopg2

from telebot import types
from config import token, days
from statusDTO import getStatus, setStatus, status
from telegrambot_db import cursor, getResponseDay, getResponseWeek

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Расписание на текущую неделю",
                 "Расписание на следующую неделю")
    bot.send_message(message.chat.id, 'Здравствуйте! Хотите узнать расписание? Рад помочь!', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def info_about_bot(message):
    bot.send_message(message.chat.id, '/start - Узнать рассписание\n' +
                     '/mtuci - Официальный сайт МТУСИ\n' +
                     '/getweek - Показать текущую неделю\n' +
                     '/setweek - Выбор недели\n')


@bot.message_handler(commands=['mtuci'])
def info_mtuci(message):
    bot.send_message(message.chat.id, 'Официальный сайт МТУСИ – https://mtuci.ru/')


@bot.message_handler(commands=['getweek'])
def currentWeek(message):
    if getStatus() == "U":
        bot.send_message(message.chat.id, "Верхняя неделя")
    else:
        bot.send_message(message.chat.id, "Нижняя неделя")


@bot.message_handler(commands=['setweek'])
def setWeek(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Верхняя", "Нижняя")
    bot.send_message(message.chat.id, "Выберите неделю:", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def day_of_the_week(message):
    if message.text in days:
        response = getResponseDay(message.text, getStatus())

        bot.send_message(message.chat.id, response)

    elif message.text == "Расписание на текущую неделю":
        response = getResponseWeek(getStatus())

        bot.send_message(message.chat.id, response)


    elif message.text == "Расписание на следующую неделю":

        clone_status = ""

        if getStatus() == "U":
            clone_status = "L"
        else:
            clone_status = "U"

        response = getResponseWeek(clone_status)

        bot.send_message(message.chat.id, response)

    elif message.text == "Верхняя":
        status = setStatus("U")
        bot.send_message(message.chat.id, "Неделя изменена на " + message.text)
    elif message.text == "Нижняя":
        status = setStatus("L")
        bot.send_message(message.chat.id, "Неделя изменена на " + message.text)

    else:
        bot.send_message(message.chat.id, "Извините, я Вас не понял")


bot.infinity_polling()