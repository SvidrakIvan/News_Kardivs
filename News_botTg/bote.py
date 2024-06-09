import os
import json
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, JobQueue

from os import environ
import logging

FORMAT = '%(asctime)-15s %(name)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logging.basicConfig(level=logging.ERROR, format=FORMAT)
logger = logging.getLogger()

# Шлях до файлу для збереження підписок
SUBSCRIPTIONS_FILE = 'subscriptions.json'
# Введіть свій токен, отриманий від BotFather
TOKEN = environ.get("NEWS_BOT_TOKEN","define me")

# Завантаження підписок з файлу
def load_subscriptions():
    if os.path.exists(SUBSCRIPTIONS_FILE):
        with open(SUBSCRIPTIONS_FILE, 'r') as file:
            try:
                return set(json.load(file))
            except json.JSONDecodeError:
                return set()
    return set()

# Збереження підписок у файл
def save_subscriptions():
    with open(SUBSCRIPTIONS_FILE, 'w') as file:
        json.dump(list(subscribed_users), file)

# Завантаження підписок при старті
subscribed_users = load_subscriptions()

# Функція для парсингу новинного сайту
def get_news():
    url = "http://feeds.bbci.co.uk/news/rss.xml"  # RSS-канал BBC News
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml-xml')  # Використовуємо lxml для парсингу XML

    news_items = soup.find_all('item')[:5]  # Отримуємо перші 5 новин
    news_list = []

    for item in news_items:
        title = item.title.text
        link = item.link.text
        news_list.append(f"{title}\n{link}")

    return news_list

# Функція для обробки команди /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привіт! Я новинний бот. Використовуй команду /news для отримання останніх новин.\n"
                                    "Команди:\n"
                                    "/subscribe - підписатися на автоматичні новини кожні 6 годин\n"
                                    "/unsubscribe - відписатися від автоматичних новин")

# Функція для обробки команди /news
async def news(update: Update, context: CallbackContext) -> None:
    news_list = get_news()
    for news_item in news_list:
        await update.message.reply_text(news_item)

# Функція для обробки команди /subscribe
async def subscribe(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    subscribed_users.add(user_id)
    save_subscriptions()
    await update.message.reply_text("Ви підписалися на автоматичні новини кожні 6 годин.")

# Функція для обробки команди /unsubscribe
async def unsubscribe(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if user_id in subscribed_users:
        subscribed_users.remove(user_id)
        save_subscriptions()
        await update.message.reply_text("Ви відписалися від автоматичних новин.")
    else:
        await update.message.reply_text("Ви не були підписані на автоматичні новини.")

# Функція для відправки новин підписаним користувачам
async def send_news_to_subscribers(context: CallbackContext):
    news_list = get_news()
    for user_id in subscribed_users:
        for news_item in news_list:
            await context.bot.send_message(chat_id=user_id, text=news_item)

def main():
    
    application = Application.builder().token(TOKEN).build()

    logger.info("News bot Started")

    # Обробники команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", news))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))

    # Планування автоматичної розсилки новин кожні 6 годин
    job_queue = application.job_queue
    job_queue.run_repeating(send_news_to_subscribers, interval=6*60*60)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
