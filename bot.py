# TODO: ZARUR ISHLAR CHIQAN SABAB BOT VAQTIDA QILIN MAD. 02/11/2025. 17:00 DA BOT TOLIQ TUGAYDI 
import requests
import time

from config import TOKEN

# =============Telegram API======================
TG_BOT_URL = f'https://api.telegram.org/bot{TOKEN}'
GetUpdates = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
SendMessange = f'https://api.telegram.org/bot{TOKEN}/sendMessage'




def get_updates(offset: int | None, limit: int = 100):
    return requests.get(GetUpdates, params={'offset': offset, 'limit': limit}).json()['result']


def send_messange(chat_id: int | str, text: str):
    requests.get(SendMessange, params={'chat_id': chat_id, 'text': text})

offset = None

while True:
    for update in get_updates(offset):    
        get_chat_id = update['message']['chat']['id']
        update_id = update['update_id']
        first_name = update['message']['from']['first_name']
        username = update['message']['from']['username']
        
        if 'text' in update['message']:
            user_text = update['message']['text']
            text = user_text
            if user_text == '/start':
                text = 'salom meni botimga xosh kelib siz'
            send_messange(get_chat_id, text)
        elif 'photo' in update['message']:
            print(update)
        
        
        
        
        
        
        
        
        
        
        
        offset = update_id + 1
