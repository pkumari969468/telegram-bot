from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
import os

TOKEN = "8702770051:AAGt1WgLNqYKprabfI7hEDA14qzQnThvpQQ"

MONGO_URL = "mongodb+srv://pkumari969468_db_user:8WfLlHMlDH7syb4G@teligrambot.ec5liii.mongodb.net/?retryWrites=true&w=majority&appName=Teligrambot"

# ================= SAFE MONGODB =================

client = MongoClient(
    MONGO_URL,
    serverSelectionTimeoutMS=5000
)

db = client["telegram_bot"]

users_collection = db["users"]

# ================= BOT =================

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):

    try:

        user_id = message.chat.id

        existing_user = users_collection.find_one(
            {"user_id": user_id}
        )

        if not existing_user:

            users_collection.insert_one(
                {"user_id": user_id}
            )

    except Exception as e:

        print("MongoDB Error:", e)

    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton(
        "🇮🇳 Indian",
        callback_data="indian"
    )

    btn2 = InlineKeyboardButton(
        "🇵🇰 Pakistani",
        callback_data="pakistani"
    )

    btn3 = InlineKeyboardButton(
        "🇷🇺 Russian",
        callback_data="russian"
    )

    btn4 = InlineKeyboardButton(
        "🔥 Latest",
        callback_data="latest"
    )

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)

    bot.send_message(
        message.chat.id,
        "🔥 Welcome ❤️\n\nChoose Option Below 👇",
        reply_markup=markup
    )

# ================= BUTTONS =================

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    links = {

        "indian": "https://t.me/+-FNft_vu2bVlMjA1",

        "pakistani": "https://t.me/+Kv6gjLUO31Q3Yzg1",

        "russian": "https://t.me/+Os2eJeUY4S5kZTRl",

        "latest": "https://t.me/+UPBBtW3bii8xZDdl"

    }

    if call.data in links:

        bot.send_message(
            call.message.chat.id,
            links[call.data]
        )

# ================= WEBHOOK =================

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():

    try:

        json_str = request.get_data().decode('UTF-8')

        update = telebot.types.Update.de_json(json_str)

        bot.process_new_updates([update])

        return "OK", 200

    except Exception as e:

        print("Webhook Error:", e)

        return "ERROR", 500

# ================= HOME =================

@app.route('/')
def home():

    return "Bot Running ✅"

# ================= START =================

print("Bot Started ✅")

bot.remove_webhook()

bot.set_webhook(
    url=f"https://mybot-cnv1.onrender.com/{TOKEN}"
)

app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 10000))
        )
