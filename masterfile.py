import logging
from main import bot
from app import app
import sys
import time
logging.basicConfig(filename="sample.log", level=logging.INFO)
from threading import Thread




def second_func():
    print('print после app.run')
    while True:
        try:
            bot.polling(none_stop=True)
        except: 
            print('bolt')
            logging.error('error: {}'.format(sys.exc_info()[0]))
            time.sleep(5)


th1 = Thread(target=second_func)

th1.start()

# app.run(host='0.0.0.0', port=5000)




# host='0.0.0.0', port=4500
# 
