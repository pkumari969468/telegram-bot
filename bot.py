from flask import Flask, request
import telebot
from pymongo import MongoClient
import os

TOKEN = "8702770051:AAGt1WgLNqYKprabfI7hEDA14qzQnThvpQQ"

MONGO_URL = "YOUR_MONGODB_URL"

client = MongoClient(MONGO_URL)

db = client["telegram_bot"]

users_collection = db["users"]

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):

    user_id = message.chat.id

    existing_user = users_collection.find_one(
        {"user_id": user_id}
    )

    if not existing_user:

        users_collection.insert_one(
            {"user_id": user_id}
        )

    bot.reply_to(
        message,
        "Bot + MongoDB Working ✅"
    )

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():

    json_str = request.get_data().decode('UTF-8')

    update = telebot.types.Update.de_json(json_str)

    bot.process_new_updates([update])

    return "OK", 200

@app.route('/')
def home():

    return "Bot Running ✅"

bot.remove_webhook()

bot.set_webhook(
    url=f"https://mybot-cnv1.onrender.com/{TOKEN}"
)

app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 10000))
)
