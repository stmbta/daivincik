# import random
import datetime
from re import S
import sqlite3


# chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
# for n in range(20):
#     password =''
#     for i in range(15):
#         password += random.choice(chars)
#     print(password)
# print(len(chars))

# date = str(datetime.datetime.now())
# print(type(date))
# print(date)

dictianory = {}

# def test():
#     global dictianory
#     dictianory.update({100: ['username']})

# def test2():
#     global dictianory
#     dictianory[100].append('age')

# test()
# print(dictianory)
# test2()
# print(dictianory)
# tupl = (85, 16, datetime.datetime.now(), 'лоах', 'photo.string', 'about', 'msfile', 3)
# con = sqlite3.connect('adb.db')
# cur = con.cursor()
# cur.execute("""INSERT INTO users (id, age, reg_time, name, photo, about, msfile, inspection) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", tupl)
# con.commit()
# con.close()
date_arr = [0 for _ in range(30)]
print(date_arr)