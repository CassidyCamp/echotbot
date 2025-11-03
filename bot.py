import os
import json
import time
import requests
from dotenv import load_dotenv

# .env fayldan o'zgaruvchilarni yuklash
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
DB_NAME = "users.json"

# Telegram API URL’lar
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
GET_UPDATES = f"{BASE_URL}/getUpdates"
SEND_MESSAGE = f"{BASE_URL}/sendMessage"
SEND_PHOTO = f"{BASE_URL}/sendPhoto"
SEND_STICKER = f"{BASE_URL}/sendSticker"
SEND_ANIMATION = f"{BASE_URL}/sendAnimation"
SEND_VOICE = f"{BASE_URL}/sendVoice"
SEND_VIDEO = f"{BASE_URL}/sendVideo"
SEND_LOCATION = f"{BASE_URL}/sendLocation"
SEND_DOCUMENT = f"{BASE_URL}/sendDocument"


# ==== Ma'lumotlar bazasi (JSON fayl) ====
def save_db(chat_id, first_name, username):
    user = {
        'chat_id': chat_id,
        'first_name': first_name,
        'username': username
    }
    try:
        with open(DB_NAME) as read_f:
            db_json = json.load(read_f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        db_json = []

    if not any(u['chat_id'] == chat_id for u in db_json):
        db_json.append(user)
        with open(DB_NAME, "w") as add_f:
            json.dump(db_json, add_f, indent=4)


def check_user(chat_id, first_name, username):
    save_db(chat_id, first_name, username)


# ==== Xabar yuborish funksiyalari ====
def send_message(chat_id, text):
    requests.get(SEND_MESSAGE, params={'chat_id': chat_id, 'text': text})


def send_photo(chat_id, file_id):
    requests.get(SEND_PHOTO, params={'chat_id': chat_id, 'photo': file_id})


def send_sticker(chat_id, file_id):
    requests.get(SEND_STICKER, params={'chat_id': chat_id, 'sticker': file_id})


def send_animation(chat_id, file_id):
    requests.get(SEND_ANIMATION, params={'chat_id': chat_id, 'animation': file_id})


def send_voice(chat_id, file_id):
    requests.get(SEND_VOICE, params={'chat_id': chat_id, 'voice': file_id})


def send_video(chat_id, file_id):
    requests.get(SEND_VIDEO, params={'chat_id': chat_id, 'video': file_id})


def send_location(chat_id, lat, lon):
    requests.get(SEND_LOCATION, params={'chat_id': chat_id, 'latitude': lat, 'longitude': lon})


def send_document(chat_id, file_id):
    requests.get(SEND_DOCUMENT, params={'chat_id': chat_id, 'document': file_id})


# ==== Polling orqali yangilanishlarni olish ====
def get_updates(offset=None, limit=100):
    response = requests.get(GET_UPDATES, params={'offset': offset, 'limit': limit})
    result = response.json()
    return result.get('result', [])


# ==== Asosiy loop ====
def main():
    offset = None
    print("Bot ishga tushdi ✅")

    while True:
        try:
            updates = get_updates(offset)
            for update in updates:
                update_id = update['update_id']
                offset = update_id + 1

                if 'message' not in update:
                    continue

                message = update['message']
                chat_id = message['chat']['id']
                first_name = message['from'].get('first_name', '')
                username = message['from'].get('username', '')

                check_user(chat_id, first_name, username)

                if 'text' in message:
                    text = message['text']
                    if text == '/start':
                        send_message(chat_id, f"Salom {first_name}! Bot ishga tushdi ✅")
                    else:
                        send_message(chat_id, f"Siz yubordingiz: {text}")

                elif 'photo' in message:
                    send_photo(chat_id, message['photo'][-1]['file_id'])
                elif 'sticker' in message:
                    send_sticker(chat_id, message['sticker']['file_id'])
                elif 'animation' in message:
                    send_animation(chat_id, message['animation']['file_id'])
                elif 'voice' in message:
                    send_voice(chat_id, message['voice']['file_id'])
                elif 'video' in message:
                    send_video(chat_id, message['video']['file_id'])
                elif 'location' in message:
                    send_location(chat_id, message['location']['latitude'], message['location']['longitude'])
                elif 'document' in message:
                    send_document(chat_id, message['document']['file_id'])

            time.sleep(1)

        except Exception as e:
            print(f"Xatolik: {e}")
            time.sleep(3)


if __name__ == "__main__":
    main()
