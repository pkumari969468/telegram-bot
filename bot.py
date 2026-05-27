import telebot
import os

TOKEN = "8702770051:AAFpiHtOkiltfZ1mxqyFUTMG7smDOlmiyLc"

bot = telebot.TeleBot(TOKEN)

if os.path.exists("users.txt"):
    with open("users.txt", "r") as f:
        users = f.read().splitlines()
else:
    users = []

@bot.message_handler(commands=['start'])
def start(message):

    user_id = str(message.chat.id)

    if user_id not in users:

        users.append(user_id)

        with open("users.txt", "a") as f:
            f.write(user_id + "\n")

    bot.reply_to(message, """🔥 Welcome Bhai ❤️

Aapka request receive ho gaya hai ✅

Aapko thodi der me video mil jayegi 🎬

Kripya bot ko delete ya block mat kare 🙏

Updates aur videos yahi milengi 🔥
""")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):

    for user in users:
        try:
            bot.send_message(user, "Hello Everyone 🔥")
        except Exception as e:
            print(e)

    bot.reply_to(message, "Broadcast Sent ✅")

@bot.message_handler(commands=['users'])
def total_users(message):

    bot.reply_to(message, f"Total Users: {len(users)}")

print("Bot Started ✅")

bot.infinity_polling(skip_pending=True, none_stop=True)