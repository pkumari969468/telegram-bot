from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
import threading
import time
import schedule
import os

# ================= TOKEN =================

TOKEN = "8702770051:AAGt1WgLNqYKprabfI7hEDA14qzQnThvpQQ"

# ================= ADMIN ID =================

ADMIN_ID = 123456789

# ================= MONGODB =================

MONGO_URL = "mongodb+srv://pkumari969468_db_user:8WfLlHMlDH7syb4G@teligrambot.ec5liii.mongodb.net/telegram_bot?retryWrites=true&w=majority&appName=Teligrambot"

client = MongoClient(MONGO_URL)

db = client["telegram_bot"]

users_collection = db["users"]

# ================= BOT =================

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# ================= AUTO MESSAGE =================

def send_good_morning():

    users = users_collection.find()

    for user in users:

        try:

            bot.send_message(
                user["user_id"],
                "🌞 Good Morning ❤️"
            )

        except:
            pass

def send_good_night():

    users = users_collection.find()

    for user in users:

        try:

            bot.send_message(
                user["user_id"],
                "🌙 Good Night ❤️"
            )

        except:
            pass

schedule.every().day.at("07:00").do(send_good_morning)

schedule.every().day.at("22:00").do(send_good_night)

def run_schedule():

    while True:

        schedule.run_pending()

        time.sleep(1)

threading.Thread(target=run_schedule).start()

# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):

    user_id = message.chat.id

    existing = users_collection.find_one(
        {"user_id": user_id}
    )

    if not existing:

        users_collection.insert_one(
            {"user_id": user_id}
        )

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
        "🔥 Welcome ❤️\n\nChoose Option 👇",
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

# ================= USERS =================

@bot.message_handler(commands=['users'])
def users(message):

    if message.chat.id != ADMIN_ID:
        return

    total = users_collection.count_documents({})

    bot.reply_to(
        message,
        f"👥 Total Users: {total}"
    )

# ================= BROADCAST =================

@bot.message_handler(
    commands=['broadcast'],
    content_types=['text', 'photo', 'video', 'document']
)
def broadcast(message):

    if message.chat.id != ADMIN_ID:
        return

    users = users_collection.find()

    sent = 0

    # TEXT

    if message.text and message.text.startswith("/broadcast"):

        text = message.text.replace("/broadcast ", "")

        for user in users:

            try:

                bot.send_message(
                    user["user_id"],
                    text
                )

                sent += 1

            except:
                pass

    # PHOTO

    elif message.photo:

        file_id = message.photo[-1].file_id

        caption = message.caption or ""

        for user in users:

            try:

                bot.send_photo(
                    user["user_id"],
                    file_id,
                    caption=caption
                )

                sent += 1

            except:
                pass

    # VIDEO

    elif message.video:

        file_id = message.video.file_id

        caption = message.caption or ""

        for user in users:

            try:

                bot.send_video(
                    user["user_id"],
                    file_id,
                    caption=caption
                )

                sent += 1

            except:
                pass

    # DOCUMENT

    elif message.document:

        file_id = message.document.file_id

        caption = message.caption or ""

        for user in users:

            try:

                bot.send_document(
                    user["user_id"],
                    file_id,
                    caption=caption
                )

                sent += 1

            except:
                pass

    bot.reply_to(
        message,
        f"✅ Broadcast Sent To {sent} Users"
    )

# ================= WEBHOOK =================

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():

    json_str = request.get_data().decode('UTF-8')

    update = telebot.types.Update.de_json(json_str)

    bot.process_new_updates([update])

    return "OK", 200

# ================= HOME =================

@app.route('/')
def home():

    return "Bot Running ✅"

# ================= START =================

bot.remove_webhook()

bot.set_webhook(
    url=f"https://mybot-cnv1.onrender.com/{TOKEN}"
)

print("Bot Started ✅")

app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 10000))
)
