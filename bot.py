import os
import requests
import time
import json

from config import TOKEN, DB_NAME
from dotenv import load_dotenv
from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}"

@app.route('/')
def home():
    return "Bot is running!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = request.get_json()
    chat_id = update["message"]["chat"]["id"]
    text = update["message"].get("text", "")

    if text == "/start":
        requests.get(f"{URL}/sendMessage", params={"chat_id": chat_id, "text": "Salom, bot ishga tushdi!"})
    return {"ok": True}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))


load_dotenv()

# Endi env o‘zgaruvchilarni olish
TOKEN = os.getenv("TELEGRAM_TOKEN")
PORT = int(os.getenv("PORT", 8080))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"


# =============Telegram API======================
TG_BOT_URL = f'https://api.telegram.org/bot{TOKEN}'
GetUpdates = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
SendMessange = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
SendPhoto = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
SendSticker = f'https://api.telegram.org/bot{TOKEN}/sendSticker'
SendAnimation = f'https://api.telegram.org/bot{TOKEN}/sendAnimation'
SendVoice = f'https://api.telegram.org/bot{TOKEN}/sendVoice'
SendVideo = f'https://api.telegram.org/bot{TOKEN}/sendVideo'
SendLocation = f'https://api.telegram.org/bot{TOKEN}/sendLocation'
SendDocument = f'https://api.telegram.org/bot{TOKEN}/sendDocument'



def get_updates(offset: int | None, limit: int = 100):
    return requests.get(GetUpdates, params={'offset': offset, 'limit': limit}).json()['result']


def send_messange(chat_id: int | str, text: str):
    requests.get(SendMessange, params={'chat_id': chat_id, 'text': text})
    

def send_photo(chat_id: str | int, file_id: str):
    requests.get(SendPhoto, params={'chat_id': chat_id, 'photo': file_id})


def send_sticker(chat_id: str | int, file_id: str):
    requests.get(SendSticker, params={'chat_id': chat_id, 'sticker': file_id})


def send_animation(chat_id: str | int, file_id: str):
    requests.get(SendAnimation, params={'chat_id': chat_id, 'animation': file_id})


def send_voice(chat_id: str | int, file_id: str):
    requests.get(SendVoice, params={'chat_id': chat_id, 'voice': file_id})


def send_video(chat_id: str | int, file_id: str):
    requests.get(SendVideo, params={'chat_id': chat_id, 'video': file_id})


def send_location(chat_id: str | int, latitude: float, longitude: float):
    requests.get(SendLocation, params={'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude})


def send_document(chat_id: str | int, file_id: str):
    requests.get(SendDocument, params={'chat_id': chat_id, 'document': file_id})


def save_db(chat_id: str|int, first_name: str, username: str):
    user = {
        'chat_id': chat_id,
        'first_name': first_name,
        'username': username
    }
    
    try:
        with open(DB_NAME) as read_f:
            db_json = json.load(read_f)
            
        with open(DB_NAME, "w") as add_f:
            db_json.append(user)
            json.dump(db_json, add_f, indent=4)
    except FileNotFoundError:
        with open(DB_NAME, "w") as add_f:
            l = [user]
            json.dump(l, add_f, indent=4)
    except json.decoder.JSONDecodeError:
        with open(DB_NAME, "w") as add_f:
            l = [user]
            json.dump(l, add_f, indent=4)
            
            
def check_user(chat_id: str|int, first_name: str, username: str):
    found = False
    try:
        
        with open(DB_NAME) as read_f:
            db_json = json.load(read_f)
            
        for user in db_json:
            if user['chat_id'] == chat_id:
                found= True
                break
        
        if not found:
            save_db(chat_id, first_name, username)
            
    except FileNotFoundError:
        save_db(chat_id, first_name, username)
    except json.decoder.JSONDecodeError:
        save_db(chat_id, first_name, username)


offset = None

while True:
    for update in get_updates(offset):    
        update_id = update['update_id']
        
        if 'message' in update:
            get_chat_id = update['message']['chat']['id']
            first_name = update['message']['from']['first_name']
            username = update['message']['from']['username']
            
            if 'text' in update['message']:
                user_text = update['message']['text']
                text = user_text
                if user_text == '/start':
                    text = 'salom meni botimga xosh kelib siz'
                    check_user(get_chat_id, first_name, username)
                
                send_messange(get_chat_id, text)
            elif 'photo' in update['message']:
                get_file_id = update['message']['photo'][-1]['file_id']
                send_photo(get_chat_id, get_file_id)
            elif 'sticker' in update['message']:
                get_sticker_id = update['message']['sticker']['file_id']
                send_sticker(get_chat_id, get_sticker_id)
            elif 'animation' in update['message']:
                get_animation_id = update['message']['animation']['file_id']
                send_animation(get_chat_id, get_animation_id)
            elif 'voice' in update['message']:
                get_voice_id = update['message']['voice']['file_id']
                send_voice(get_chat_id, get_voice_id)
            elif 'video' in update['message']:
                get_video_id = update['message']['video']['file_id']
                send_video(get_chat_id, get_video_id)
            elif 'location' in update['message']:
                get_latitude = update['message']['location']['latitude']
                get_longitude = update['message']['location']['longitude']
                send_location(get_chat_id, get_latitude, get_longitude)
            elif 'document' in update['message']:
                get_document_id = update['message']['document']['file_id']
                send_document(get_chat_id, get_document_id)
        
        offset = update_id + 1
        time.sleep(1)
