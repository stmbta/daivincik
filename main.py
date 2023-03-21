from config import bot_token
import telebot 
from requests import get
import sqlite3
from telebot import types
from db.db import Users, get_users, generate_tokens, check_inspection, check_dislike, dislike, get_name, stop_dialogue, check_register, check_islike, find_friend, get_user_invites, is_matching, like, user_registration, user_arr, start_dial, cur_dial_find, new_message_add, check_invite, UsersAndDialogs, Messages, Inspections, Invites
import os

last_like = {}
global_dict = {}
url_number = 1
bot = telebot.TeleBot(bot_token)
register_dict = {}
admin_list = [785704774, 197942998]


@bot.message_handler(commands=['sendmessage'])
def send_message(message):
    if message.chat.id in admin_list:
        mesg = bot.send_message(message.chat.id, 'Отправьте фотографию с текстом или просто текст для рассылки')
        bot.register_next_step_handler(mesg, send_message_1)
    else:
        bot.send_message(message.chat.id, 'У вас нет прав для выполнения данной команды')


def send_message_1(message):
    try:
        if message.photo:
            raw = message.photo[2].file_id
            name = raw+".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            
            with open(name,'wb') as new_file:
                new_file.write(downloaded_file)
            with open (name, 'rb') as file: 
                for user_id in get_users():
                    bot.send_photo(user_id, photo=types.InputMediaPhoto(file), caption=message.caption)
            os.remove(name)
        else:
            for user_id in get_users():
                bot.send_message(user_id, text=message.text)
        bot.send_message(message.chat.id, 'Сообщения успешно отправлены')
    except: 
        bot.send_message(message.chat.id, 'Отправленное вами сообщение некорректно, оно не может быть переслано пользователям')

@bot.message_handler(commands=['getinvite'])
def getinvite(message):
    if check_register(message.chat.id):
        arr = get_user_invites(message.chat.id)
        if len(arr) != 0:
            bot.send_message(message.chat.id, 'Ваши инвайты:')
            for elem in arr:
                bot.send_message(message.chat.id, f'{elem}')
        else:
            bot.send_message(message.chat.id, 'Ваши инвайты закончились.')
        # joinarr = "\n".join(arr)
        # bot.send_message(message.chat.id, f'Ваши инвайты \n{joinarr}')
    else:
        bot.send_message(message.chat.id, "Вы не зарегистрированы")


@bot.message_handler(commands=['start'])
def check_token(message):
    if check_register(message.chat.id):
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы')
    else:
        mesg = bot.send_message(message.chat.id, 'Введите ваш инвайт-код:', )
        bot.register_next_step_handler(mesg, start)
        
@bot.message_handler(commands=['continue'])
def contin(message):
    if check_register(message.chat.id):
        keyb = types.InlineKeyboardMarkup(row_width=1)
        butt = types.InlineKeyboardButton(text='Продолжить знакомиться', callback_data='startwatching')
        keyb.add(butt)
        bot.send_message(message.chat.id, 'Продолжим знакомиться?', reply_markup=keyb)
    else:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы')

@bot.message_handler(commands=['ismatchs'])
def ismatchhing(message):
    if check_register(message.chat.id):
        if not cur_dial_find(message.chat.id):
            kob = types.InlineKeyboardMarkup(row_width=2)
            arr = is_matching(message.chat.id)
            txt = ''
            print(0)
            if arr:     
                for elem in arr:
                    kob = types.InlineKeyboardMarkup(row_width=2)
                    kob.add(types.InlineKeyboardButton(text=f'{elem[1]}', callback_data=f'suggdial/{message.chat.id}/{elem[0]}'))
                    txt = elem[1] 
                    bot.send_message(message.chat.id, txt, reply_markup=kob, parse_mode='Markdown')

            else:
                bot.send_message(message.chat.id, 'Возможных диалогов не найдено')
        else:
            bot.send_message(message.chat.id, 'Вы уже ведете диалог')
    else:
        bot.send_message(message.chat.id, "Вы не зарегистрированы")


def start(message):
    i = check_invite(message.text, message.chat.id)
    if i == 1:
        bot.send_message(message.chat.id, 'Видео-инструкция по пользованию бота: https://youtu.be/py3y6-Nw6yc')
        keyb = types.InlineKeyboardMarkup()
        reg_button = types.InlineKeyboardButton(text='Я согласен с политикой обработки персональных данных', callback_data='reg')
        keyb.add(reg_button)
        with open('rules.docx', 'rb') as file:
            bot.send_document(message.chat.id, file)
            
        
        with open('politics.docx', 'rb') as file:
            bot.send_document(message.chat.id, file)

        bot.send_message(message.chat.id, 'Для использования бота необходимо согласится с политикой обработки персональных данных', reply_markup=keyb)
    elif i == -1:
        mesg = bot.send_message(message.chat.id, 'Неправильный инвайт-код')
        bot.register_next_step_handler(mesg, start)
    else:
        mesg = bot.send_message(message.chat.id, 'Код уже использован')
        bot.register_next_step_handler(mesg, start)




        
 

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "reg":
            global global_dict
            global register_dict
            
            if call.message.chat.id in global_dict:
                bot.send_message(call.message.chat.id, 'Вы уже начали регистрацию')
                bot.answer_callback_query(callback_query_id=call.id)
            elif call.message.chat.id in register_dict:
                bot.send_message(call.message.chat.id, 'Вы уже начали регистрацию')
                bot.answer_callback_query(callback_query_id=call.id)

            else:
                
                mesg = bot.send_message(call.message.chat.id, 'Введите свое имя и фамилию:')
                register_dict.update({call.message.chat.id: 1})
                bot.register_next_step_handler(mesg, reg)
                bot.answer_callback_query(callback_query_id=call.id)

        elif call.data == "startwatching":
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
            u2 = find_friend(call.message.chat.id)
            print(call.message.chat.id)

            if u2:
                filepath = u2[2]

                kb = types.InlineKeyboardMarkup(row_width=2)
                like_button = types.InlineKeyboardButton(text='🤝', callback_data=f'like/{str(u2[0])}')

                dislike_button = types.InlineKeyboardButton(text='⛔️', callback_data=f'dislike/{str(u2[0])}')
                kb.add(like_button, dislike_button)
                # see_matchs = types.InlineKeyboardButton(text='Возможные диалоги', callback_data='ismatchs')
                # kb.add(see_matchs)
                last_like.update({call.message.chat.id: u2[0]})
                print(u2)
                bot.send_photo(call.message.chat.id, open(f'{filepath}', 'rb'), caption=f'_{u2[1]}, {u2[4]}_ \n{u2[3]}', reply_markup=kb, parse_mode='Markdown')
            else:
                bot.send_message(call.message.chat.id, 'собеседники кончились')
        elif call.data.split('/')[0] == 'like':

            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
            if not check_islike(call.message.chat.id, int(call.data.split('/')[-1])):
                like(call.message.chat.id, int(call.data.split('/')[-1]))

            else:
                bot.send_message(call.message.chat.id, 'Вы уже лайкали этого пользователя')
                bot.answer_callback_query(callback_query_id=call.id)
            u2 = find_friend(call.message.chat.id)
            if u2:
                filepath = u2[2]
                kb = types.InlineKeyboardMarkup(row_width=2)
                like_button = types.InlineKeyboardButton(text='🤝', callback_data=f'like/{str(u2[0])}')

                dislike_button = types.InlineKeyboardButton(text='⛔️', callback_data=f'dislike/{str(u2[0])}')
                kb.add(like_button, dislike_button)
                # see_matchs = types.InlineKeyboardButton(text='Возможные диалоги', callback_data='ismatchs')
                # kb.add(see_matchs)
            


                print(u2)
                bot.send_photo(call.message.chat.id, open(f'{filepath}', 'rb'), caption=f'{u2[1]}, {u2[4]} \n{u2[3]}', reply_markup=kb)
                bot.answer_callback_query(callback_query_id=call.id)
            else:
                bot.send_message(call.message.chat.id, 'собеседники кончились')
                bot.answer_callback_query(callback_query_id=call.id)
        elif call.data.split('/')[0] == 'dislike':
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
            if not check_dislike(call.message.chat.id, int(call.data.split('/')[-1])):
                dislike(call.message.chat.id, int(call.data.split('/')[-1]))
            
            u2 = find_friend(call.message.chat.id)
            if u2:
                filepath = u2[2]
                kb = types.InlineKeyboardMarkup(row_width=2)
                like_button = types.InlineKeyboardButton(text='🤝', callback_data=f'like/{str(u2[0])}')

                
                dislike_button = types.InlineKeyboardButton(text='⛔️', callback_data=f'dislike/{str(u2[0])}')
                kb.add(like_button, dislike_button)
                # see_matchs = types.InlineKeyboardButton(text='Возможные диалоги', callback_data='ismatchs')
                # kb.add(see_matchs)
                

                last_like.update({call.message.chat.id: u2[0]})
                print(u2)
                bot.send_photo(call.message.chat.id, open(f'{filepath}', 'rb'), caption=f'{u2[1]}, {u2[4]} \n{u2[3]}', reply_markup=kb)
                bot.answer_callback_query(callback_query_id=call.id)
            else:
                bot.send_message(call.message.chat.id, 'собеседники кончились')
                bot.answer_callback_query(callback_query_id=call.id)
        # elif call.data == 'ismatchs':
        #     bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        #     kob = types.InlineKeyboardMarkup(row_width=1)
        #     arr = is_matching(call.message.chat.id)
        #     txt = ''
        #     print(0)
        #     if arr:
        #         for elem in arr:
        #             kob.add(types.InlineKeyboardButton(text=f'{elem[1]}', callback_data=f'suggdial/{call.message.chat.id}/{elem[0]}'))
        #             txt = txt + elem[1] + '\n'
        #         bot.send_message(call.message.chat.id, f'Список возможных диалогов: {txt}', reply_markup=kob)
        #         bot.answer_callback_query(callback_query_id=call.id)
        #     else:
        #         bot.send_message(call.message.chat.id, 'Возможных диалогов не найдено')
        #         bot.answer_callback_query(callback_query_id=call.id)
        elif call.data.split('/')[0] == 'suggdial':
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
            arr = call.data.split('/')
            kb = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text='Начать', callback_data=f'{arr[1]}')
            kb.add(button)
            bot.send_message(int(call.data.split('/')[2]), f'С вами хочет начать диалог пользователь {get_name(int(arr[1]))}', reply_markup=kb)
            bot.send_message(call.message.chat.id, 'Заявка отправлена')
            bot.answer_callback_query(callback_query_id=call.id)
        
        elif call.data.split('/')[0] == 'ismatchs':
            if not cur_dial_find(call.message.chat.id):
                kob = types.InlineKeyboardMarkup()
                arr = is_matching(call.message.chat.id)
                txt = ''
                
                print(0)
                num = int(call.data.split("/")[1]) 
                if arr:
                    if len(arr) > (num+1) * 5:
                        kob.add(types.InlineKeyboardButton(text=f'->', callback_data=f'ismatchs/{int(call.data.split("/")[1]) + 1}'))
                    if num > 0:
                        kob.add(types.InlineKeyboardButton(text=f'<-', callback_data=f'ismatchs/{int(call.data.split("/")[1]) - 1}'))
                    
                    
                    arr = arr[num*5:(num+1)*5]
                    

                    for elem in arr:
                        kob.add(types.InlineKeyboardButton(text=f'{elem[1]}', callback_data=f'suggdial/{call.message.chat.id}/{elem[0]}'))
                        txt = txt + elem[1] + '\n'
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=kob)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'_Список возможных диалогов_:\n{txt}', parse_mode='Markdown')
                    bot.answer_callback_query(callback_query_id=call.id)
    

        


        if call.data.isdigit():
            if call.data in user_arr():
                if not cur_dial_find(call.message.chat.id):
                    start_dial(call.message.chat.id, int(call.data))
                    bot.send_message(call.message.chat.id, f'Вы начали диалог с {get_name(int(call.data))}')
                    bot.send_message(int(call.data), f'С вами начал диалог пользователь {get_name(call.message.chat.id)}')
                    bot.answer_callback_query(callback_query_id=call.id)
                else:
                    bot.send_message(call.message.chat.id, 'Одновременно можно вести только один диалог')
                    bot.answer_callback_query(callback_query_id=call.id)
                    




def reg(message):
    global global_dict
    username = message.text

    global_dict.update({message.chat.id: [username]})
    mesg = bot.send_message(message.chat.id, 'Сколько вам лет?')
    bot.register_next_step_handler(mesg, reg1)

def reg1(message):
    global global_dict
    try:
        age = int(message.text)
        global_dict[message.chat.id].append(age)
        mesg = bot.send_message(message.chat.id, 'Теперь отправьте свою фотографию:')
        bot.register_next_step_handler(mesg, reg2)
    except:
        mesg = bot.send_message(message.chat.id, 'Возраст введен некорректно, введите еще раз, используя только цифры')
        bot.register_next_step_handler(mesg, reg1)



def reg2(message):
    global global_dict
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f'{file_info.file_path}'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        global_dict[message.chat.id].append(src)
        mesg = bot.send_message(message.chat.id, "А сейчас давайте добавим описание:")
        bot.register_next_step_handler(mesg, reg3)
    except:
        mesg = bot.send_message(message.chat.id, 'Фотография некорректна, отправьте еще раз')
        bot.register_next_step_handler(mesg, reg2)

def reg3(message):
    global global_dict
    about = message.text
    global_dict[message.chat.id].append(about)

    with open(f'{message.chat.id}.txt', 'w') as f:
        f.write(f'Файл с переписками {global_dict[message.chat.id][0]}')


    
    global_dict[message.chat.id].append(f'{message.chat.id}.txt')
    
    mesg = bot.send_message(message.chat.id, 'Теперь укажите номер инспекции (строго 4 цифры):')

    bot.register_next_step_handler(mesg, reg4)
    # bot.send_photo(message.chat.id, photo_link, caption=f'{username} \n{about}', reply_markup=kb)


def reg4(message):
    global global_dict

    inspection_number = message.text
    if check_inspection(inspection_number):


        global_dict[message.chat.id].append(inspection_number)
        user_registration(message.chat.id, global_dict[message.chat.id])
        keyb = types.InlineKeyboardMarkup(row_width=1)
        butt = types.InlineKeyboardButton(text='Начать знакомиться', callback_data='startwatching')
        # keyb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        # butt = types.KeyboardButton(text='Начать знакомиться')
        keyb.add(butt)
        bot.send_message(message.chat.id, 'Начнем?', reply_markup=keyb)
    else:
        mesg = bot.send_message(message.chat.id, 'Некорректный номер инспекции')
        bot.register_next_step_handler(mesg, reg4)


# @bot.callback_query_handler(func=lambda call: True)
# def callback_inlin(call):
#     if call.message:
#         if call.data == "startwatching":
#             kb = types.InlineKeyboardMarkup(row_width=2)
#             like_button = types.InlineKeyboardButton(text='❤️', callback_data='like')
#             print(0)
#             dislike_button = types.InlineKeyboardButton(text='⛔️', callback_data='dislike')
#             kb.add(like_button, dislike_button)
#             see_matchs = types.InlineKeyboardButton(text='Возможные диалоги', callback_data='ismatchs')
#             kb.add(see_matchs)
#             u2 = find_friend(call.message.chat.id)
#             print(1)
#             file_info = bot.get_file(u2.photo)
#             filepath = file_info.file_path
#             last_like.update({call.message.chat.id: u2.id})
#             bot.send_photo(call.message.chat.id, get(f'http://api.telegram.org/file/bot{bot_token}/{filepath}').content, caption=f'{u2.name}, {u2.age} \n{u2.about}', reply_markup=kb)

# @bot.callback_query_handler(func=lambda call: True)
# def callback_inli(call):
#     if call.message:
#         if call.data == 'like':
#             like(call.message.chat.id, last_like[call.message.chat.id])
#             kb = types.InlineKeyboardMarkup(row_width=2)
#             like_button = types.InlineKeyboardButton(text='❤️', callback_data='like')
            
#             dislike_button = types.InlineKeyboardButton(text='⛔️', callback_data='dislike')
#             kb.add(like_button, dislike_button)
#             see_matchs = types.InlineKeyboardButton(text='Возможные диалоги', callback_data='ismatchs')
#             kb.add(see_matchs)
#             u2 = find_friend(call.message.chat.id)
#             file_info = bot.get_file(u2.photo)
#             filepath = file_info.file_path
#             last_like.update({call.message.chat.id: u2.id})
#             bot.send_photo(call.message.chat.id, get(f'http://api.telegram.org/file/bot{bot_token}/{filepath}').content, caption=f'{u2.name}, {u2.age} \n{u2.about}', reply_markup=kb)
#         elif call.data == 'dislike':
#             kb = types.InlineKeyboardMarkup(row_width=2)
#             like_button = types.InlineKeyboardButton(text='❤️', callback_data='like')
            
#             dislike_button = types.InlineKeyboardButton(text='⛔️', callback_data='dislike')
#             kb.add(like_button, dislike_button)
#             see_matchs = types.InlineKeyboardButton(text='Возможные диалоги', callback_data='ismatchs')
#             kb.add(see_matchs)
#             u2 = find_friend(call.message.chat.id)
#             file_info = bot.get_file(u2.photo)
#             filepath = file_info.file_path
#             last_like.update({call.message.chat.id: u2.id})
#             bot.send_photo(call.message.chat.id, get(f'http://api.telegram.org/file/bot{bot_token}/{filepath}').content, caption=f'{u2.name}, {u2.age} \n{u2.about}', reply_markup=kb)
    
# @bot.callback_query_handler(func=lambda call: True)
# def ismatch_callback(call):
#     if call.message:
#         if call.data == 'ismatchs':
#             kob = types.InlineKeyboardMarkup(row_width=1)
#             arr = is_matching(call.message.chat.id)
#             txt = ''
#             if arr:
#                 for elem in arr:
#                     kob.add(types.InlineKeyboardButton(text=f'{elem[1]}', callback_data=f'{elem[0]}'))
#                     txt = txt + elem[1] + '\n'
#             bot.send_message(call.message.chat.id, f'Список возможных диалогов: {txt}', reply_markup=kob)

@bot.message_handler(commands=['changeprofile'])
def change_profile(message):
    if check_register(message.chat.id):
    
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        butt = types.KeyboardButton(text='Изменить профиль')
        keyboard.add(butt)
        bot.send_message(message.chat.id, 'Хотите изменить свой профиль? Нажмите на кнопку для подтверждения.', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Вы не зарегистрированы")
        
       
@bot.message_handler(commands=['get_more_invites'])
def get_more_invites(message):
    mesg = bot.send_message(message.chat.id, 'Введите секретный токен:')
    bot.register_next_step_handler(mesg, get_more_invites2)

def get_more_invites2(message):
    if message.text == 'x29cv-39%32ka_!d':
        res = generate_tokens()
        bot.send_message(message.chat.id, '\n'.join(res))


@bot.callback_query_handler(func=lambda call: True)
def start_dialogue(call):
    if call.message:
        if call.data in user_arr():
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
            start_dial(call.message.chat.id, int(call.data))

@bot.message_handler(commands=['stopdialog'])
def stopdialog(message):
    fr_id = cur_dial_find(message.chat.id)
    if fr_id:
        stop_dialogue(message.chat.id, fr_id[0])
        bot.send_message(message.chat.id, 'Диалог закончен')
        bot.send_message(fr_id[0], 'Пользователь покинул диалог')
    else:
        bot.send_message(message.chat.id, 'Вы ни с кем не ведёте диалог')
    

@bot.message_handler(content_types=['text'])
def starttt(message):
    if message.text == "Зарегистрироваться":
        global global_dict
        global register_dict
            
        if message.chat.id in global_dict:
            bot.send_message(message.chat.id, 'Вы уже начали регистрацию')
        elif message.chat.id in register_dict:
            bot.send_message(message.chat.id, 'Вы уже начали регистрацию')

        else:
                
            mesg = bot.send_message(message.chat.id, 'Введите свое имя и фамилию:')
            register_dict.update({message.chat.id: 1})
            bot.register_next_step_handler(mesg, reg)
    elif message.text == 'Начать знакомиться':
        u2 = find_friend(message.chat.id)
        print(message.chat.id)
        if True:
            if u2:
                filepath = u2[2]

                kb = types.InlineKeyboardMarkup(row_width=2)
                like_button = types.InlineKeyboardButton(text='🤝', callback_data=f'like/{str(u2[0])}')

                dislike_button = types.InlineKeyboardButton(text='⛔️', callback_data=f'dislike/{str(u2[0])}')
                kb.add(like_button, dislike_button)
                # see_matchs = types.InlineKeyboardButton(text='Возможные диалоги', callback_data='ismatchs')
                # kb.add(see_matchs)
                last_like.update({message.chat.id: u2[0]})
                print(u2)
                bot.send_photo(message.chat.id, open(f'{filepath}', 'rb'), caption=f'_{u2[1]}, {u2[4]}_ \n{u2[3]}', reply_markup=kb, parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, 'собеседники кончились')
    elif message.text == "Изменить профиль":
        mesg = bot.send_message(message.chat.id, 'Введите свое имя и фамилию:')
        register_dict.update({message.chat.id: 1})
        bot.register_next_step_handler(mesg, reg)
    else:
        fr_id = cur_dial_find(message.chat.id)
        if fr_id:
            try:
                bot.send_message(fr_id[0], f'_{get_name(message.chat.id)}_:  {message.text}', parse_mode='Markdown')
                new_message_add(message.message_id, message.chat.id, fr_id[0], message.text)
            except:
                stop_dialogue(message.chat.id, fr_id[0])
                bot.send_message(message.chat.id, 'Диалог закончен')

        else:
            bot.send_message(message.chat.id, 'Вы ни с кем не ведёте диалог')


# @bot.message_handler(content_types=['text'])
# def dialogg(message):
#     fr_id = cur_dial_find(message.chat.id)
#     if fr_id:
#         bot.send_message(fr_id[0], f'{get_name(message.chat.id)}:\n{message.text}')
#         # new_message_add(message.id, message.chat.id, fr_id[0], message.text)
#     else:
#         bot.send_message(message.chat.id, 'Вы ни с кем не ведёте диалог')
    
        







# bot.polling(none_stop=True)
