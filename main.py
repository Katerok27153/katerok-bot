import os
from dotenv import load_dotenv
import telebot
load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("В .env нет TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я твой первый бот! Напиши /help")
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message, "/start - начать\n/help - помощь\n/about - о боте")
@bot.message_handler(commands=['about'])
def about_cmd(message):
    bot.reply_to(message, "Это бот, созданный с целью приобретения практических навыков по созданию Telegram бота\nАвтор: Верниковская Екатерина Андреевна\nВерсия: 1.0.1")

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)