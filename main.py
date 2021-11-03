from config import bot_token
import telebot 
from requests import get
import sqlite3
from telebot import types
from db.db import Users, user_registration, UsersAndDialogs, Messages, Inspections, Invites


url_number = 1
bot = telebot.TeleBot(bot_token)
@bot.message_handler(commands=['start'])
def start(message):
    keyb = types.InlineKeyboardMarkup()
    reg_button = types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg')
    keyb.add(reg_button)
    
    bot.send_message(message.chat.id, 'Приветствую тебя в боте! Нажми "зарегистрироваться" чтобы начать общение', reply_markup=keyb)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "reg":
            mesg = bot.send_message(call.message.chat.id, 'Введи свое имя:')
            bot.register_next_step_handler(mesg, reg)

def reg(message):
    username = message.text
    mesg = bot.send_message(message.chat.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(mesg, reg1)

def reg1(message):

    mesg = bot.send_message(message.chat.id, 'Теперь отправь свою фотографию:')
    bot.register_next_step_handler(mesg, reg2)

def reg2(message):
    global file_id
    file_id = message.photo[-1].file_id
    mesg = bot.send_message(message.chat.id, "А сейчас давай добавим описание:")
    bot.register_next_step_handler(mesg, reg3)

def reg3(message):
    about = message.text
    kb = types.InlineKeyboardMarkup(row_width=2)
    like_button = types.InlineKeyboardButton(text='❤️', callback_data='like')
    
    dislike_button = types.InlineKeyboardButton(text='⛔️', callback_data='dislike')
    kb.add(like_button, dislike_button)
    see_matchs = types.InlineKeyboardButton(text='Возможные диалоги', callback_data='ismatchs')
    kb.add(see_matchs)
    # photo_link = 'https://web.archive.org/web/20200305072250if_/https://2ch.hk/b/src/214946077/15833836674910.jpg'
    # bot.send_photo(message.chat.id, photo_link, caption=f'{username} \n{about}', reply_markup=kb)




bot.polling(none_stop=True)