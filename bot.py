from flask import Flask
from threading import Thread
import telebot
import os

# ========= KEEP ALIVE =========

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ========= BOT TOKEN =========

TOKEN = "8702770051:AAFpiHtOkiltfZ1mxqyFUTMG7smDOlmiyLc"

bot = telebot.TeleBot(TOKEN)

# ========= USERS LOAD =========

if os.path.exists("users.txt"):
    with open("users.txt", "r") as f:
        users = f.read().splitlines()
else:
    users = []

# ========= START COMMAND =========

@bot.message_handler(commands=['start'])
def start(message):

    user_id = str(message.chat.id)

    if user_id not in users:

        users.append(user_id)

        with open("users.txt", "a") as f:
            f.write(user_id + "\n")

    bot.reply_to(message, """
🔥 Welcome ❤️

Aapka request receive ho gaya hai ✅

Bot active hai 🚀
""")

# ========= USERS COMMAND =========

@bot.message_handler(commands=['users'])
def total_users(message):

    bot.reply_to(
        message,
        f"Total Users: {len(users)}"
    )

# ========= UNIVERSAL BROADCAST =========

@bot.message_handler(commands=['broadcast'])
def broadcast(message):

    if not message.reply_to_message:

        bot.reply_to(
            message,
            "Kisi bhi message/photo/video pe reply karke /broadcast bhejo"
        )
        return

    msg = message.reply_to_message

    sent = 0

    for user in users:

        try:

            # TEXT
            if msg.text:

                bot.send_message(
                    user,
                    msg.text
                )

            # PHOTO
            elif msg.photo:

                photo_id = msg.photo[-1].file_id

                bot.send_photo(
                    user,
                    photo_id,
                    caption=msg.caption
                )

            # VIDEO
            elif msg.video:

                video_id = msg.video.file_id

                bot.send_video(
                    user,
                    video_id,
                    caption=msg.caption
                )

            # DOCUMENT
            elif msg.document:

                doc_id = msg.document.file_id

                bot.send_document(
                    user,
                    doc_id,
                    caption=msg.caption
                )

            sent += 1

        except Exception as e:
            print(e)

    bot.reply_to(
        message,
        f"Broadcast Sent To {sent} Users ✅"
    )

# ========= BOT START =========

print("Bot Started ✅")

keep_alive()

bot.infinity_polling(skip_pending=True)
