from flask import Flask, request
import telebot
from pymongo import MongoClient
import os

# ========= BOT TOKEN =========

TOKEN = "8702770051:AAGOZqOSi62PQmcYYdibmqVu3lwd-J4WmtU"

# ========= MONGODB =========

MONGO_URL = "mongodb+srv://pkumari969468_db_user:8WfLlHMlDH7syb4G@teligrambot.ec5liii.mongodb.net/?appName=Teligrambot"

client = MongoClient(MONGO_URL)

db = client["telegram_bot"]

users_collection = db["users"]

# ========= BOT =========

bot = telebot.TeleBot(TOKEN)

# ========= FLASK =========

app = Flask(__name__)

# ========= START COMMAND =========

@bot.message_handler(commands=['start'])
def start(message):

    user_id = str(message.chat.id)

    existing_user = users_collection.find_one(
        {"user_id": user_id}
    )

    if not existing_user:

        users_collection.insert_one(
            {"user_id": user_id}
        )

    markup = telebot.types.InlineKeyboardMarkup()

    btn1 = telebot.types.InlineKeyboardButton(
        "🇮🇳 Indian",
        callback_data="indian"
    )

    btn2 = telebot.types.InlineKeyboardButton(
        "🇵🇰 Pakistani",
        callback_data="pakistani"
    )

    btn3 = telebot.types.InlineKeyboardButton(
        "🇷🇺 Russian",
        callback_data="russian"
    )

    btn4 = telebot.types.InlineKeyboardButton(
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

# ========= BUTTON REPLY =========

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

# ========= USERS COMMAND =========

@bot.message_handler(commands=['users'])
def total_users(message):

    count = users_collection.count_documents({})

    bot.reply_to(
        message,
        f"Total Users: {count}"
    )

# ========= BROADCAST =========

@bot.message_handler(commands=['broadcast'])
def broadcast(message):

    if not message.reply_to_message:

        bot.reply_to(
            message,
            "Reply karke /broadcast bhejo"
        )
        return

    msg = message.reply_to_message

    sent = 0

    all_users = users_collection.find()

    for user in all_users:

        user_id = user["user_id"]

        try:

            # TEXT
            if msg.text:

                bot.send_message(
                    user_id,
                    msg.text
                )

            # PHOTO
            elif msg.photo:

                bot.send_photo(
                    user_id,
                    msg.photo[-1].file_id,
                    caption=msg.caption
                )

            # VIDEO
            elif msg.video:

                bot.send_video(
                    user_id,
                    msg.video.file_id,
                    caption=msg.caption
                )

            # DOCUMENT
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

# ========= WEBHOOK =========

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():

    json_str = request.get_data().decode('UTF-8')

    update = telebot.types.Update.de_json(json_str)

    bot.process_new_updates([update])

    return "OK", 200

# ========= HOME =========

@app.route('/')
def home():
    return "Bot Running ✅"

# ========= START =========

print("Bot Started ✅")

bot.remove_webhook()

RENDER_URL = "https://mybot-cnv1.onrender.com"

bot.set_webhook(
    url=f"{RENDER_URL}/{TOKEN}"
)

app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 10000))
)
