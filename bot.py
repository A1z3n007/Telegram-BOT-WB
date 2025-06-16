from telebot import TeleBot, types
from config import TOKEN, whitelist
from core import analyze_article
from database import init_db

bot = TeleBot(TOKEN)
init_db()

def is_whitelisted(message):
    return str(message.chat.id) in whitelist

@bot.message_handler(commands=['start'])
def start(message):
    if is_whitelisted(message):
        bot.send_message(message.chat.id, "✅ Добро пожаловать!")
    else:
        bot.send_message(message.chat.id, "❌ У вас нет доступа к боту.")

@bot.message_handler(content_types=['text'])
def on_text(message):
    if is_whitelisted(message):
        analyze_article(bot, message)
    else:
        bot.send_message(message.chat.id, "⛔ Доступ запрещён")

if __name__ == '__main__':
    bot.infinity_polling()