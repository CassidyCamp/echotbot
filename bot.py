import os
import json
import requests
from flask import Flask, request
from dotenv import load_dotenv

# .env fayldan o'zgaruvchilarni yuklash
load_dotenv()

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
DB_NAME = "users.json"
URL = f"https://api.telegram.org/bot{TOKEN}"

# =================== Asosiy sahifa ===================
@app.route('/')
def home():
    return "Bot is running!"

# =================== Webhook qabul qilish ===================
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = request.get_json()

    if not update or "message" not in update:
        return {"ok": True}

    chat_id = update["message"]["chat"]["id"]
    text = update["message"].get("text", "")
    first_name = update["message"]["from"]["first_name"]
    username = update["message"]["from"].get("username", "")

    check_user(chat_id, first_name, username)

    if text == "/start":
        reply = "Salom! Mening botimga xush kelibsiz 😊"
    else:
        reply = f"Siz yubordingiz: {text}"

    requests.get(f"{URL}/sendMessage", params={
        "chat_id": chat_id,
        "text": reply
    })

    return {"ok": True}

# =================== Foydalanuvchini saqlash ===================
def save_db(chat_id, first_name, username):
    user = {"chat_id": chat_id, "first_name": first_name, "username": username}
    try:
        with open(DB_NAME) as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = []

    if not any(u["chat_id"] == chat_id for u in data):
        data.append(user)
        with open(DB_NAME, "w") as f:
            json.dump(data, f, indent=4)

def check_user(chat_id, first_name, username):
    save_db(chat_id, first_name, username)

# =================== Flask ishga tushishi ===================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
