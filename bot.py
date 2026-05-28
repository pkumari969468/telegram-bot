from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
import os

# ================= TOKEN =================

TOKEN = "8702770051:AAGt1WgLNqYKprabfI7hEDA14qzQnThvpQQ"

# ================= MONGODB =================

MONGO_URL = "mongodb+srv://pkumari969468_db_user:8WfLlHMlDH7syb4G@teligrambot.ec5liii.mongodb.net/?retryWrites=true&w=majority&appName=Teligrambot"

client = MongoClient(MONGO_URL)

db = client["telegram_bot"]

users_collection = db["users"]

# ================= ADMIN =================

ADMIN_ID = 123456789

# ================= BOT =================

bot = telebot.TeleBot(TOKEN)

# ================= FLASK =================

app = Flask(__name__)

# ================= START =================

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

    if call.data == "indian":

        bot.send_message(
            call.message.chat.id,
            "https://t.me/+-FNft_vu2bVlMjA1"
        )

    elif call.data == "pakistani":

        bot.send_message(
            call.message.chat.id,
            "https://t.me/+Kv6gjLUO31Q3Yzg1"
        )

    elif call.data == "russian":

        bot.send_message(
            call.message.chat.id,
            "https://t.me/+Os2eJeUY4S5kZTRl"
        )

    elif call.data == "latest":

        bot.send_message(
            call.message.chat.id,
            "https://t.me/+UPBBtW3bii8xZDdl"
        )

# ================= USERS =================

@bot.message_handler(commands=['users'])
def users(message):

    if message.chat.id != ADMIN_ID:

        return

    total = users_collection.count_documents({})

    bot.reply_to(
        message,
        f"Total Users: {total}"
    )

# ================= BROADCAST =================

@bot.message_handler(commands=['broadcast'])
def broadcast(message):

    if message.chat.id != ADMIN_ID:

        return

    if not message.reply_to_message:

        bot.reply_to(
            message,
            "Reply to a message with /broadcast"
        )

        return

    msg = message.reply_to_message

    sent = 0

    users = users_collection.find()

    for user in users:

        user_id = user["user_id"]

        try:

            if msg.text:

                bot.send_message(
                    user_id,
                    msg.text
                )

            elif msg.photo:

                bot.send_photo(
                    user_id,
                    msg.photo[-1].file_id,
                    caption=msg.caption
                )

            elif msg.video:

                bot.send_video(
                    user_id,
                    msg.video.file_id,
                    caption=msg.caption
                )

            elif msg.document:

                bot.send_document(
                    user_id,
                    msg.document.file_id,
                    caption=msg.caption
                )

            sent += 1

        except Exception as e:

            print(e)

    bot.reply_to(
        message,
        f"Broadcast Sent To {sent} Users ✅"
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

        print(e)

        return "ERROR", 500

# ================= HOME =================

@app.route('/')
def home():

    return "Bot Running ✅"

# ================= START BOT =================

print("Bot Started ✅")

bot.remove_webhook()

bot.set_webhook(
    url=f"https://mybot-cnv1.onrender.com/{TOKEN}"
)

app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 10000))
            )
