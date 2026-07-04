import os
import telebot
import requests
import time
from datetime import datetime
from dotenv import load_dotenv
import threading

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(BOT_TOKEN)


def get_weather(city='Moscow'):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('cod') != 200:
            return f"❌ Город '{city}' не найден. Проверь название."
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        return (f"🌤 Погода в {city.capitalize()}:\n"
                f"🌡 Температура: {temp}°C (ощущается как {feels_like}°C)\n"
                f"📝 {description.capitalize()}\n"
                f"💧 Влажность: {humidity}%\n"
                f"💨 Ветер: {wind} м/с")
    except Exception as e:
        return f"⚠ Ошибка при получении погоды: {e}"


def send_daily_weather():
    if CHAT_ID:
        try:
            weather = get_weather('Minsk')
            bot.send_message(CHAT_ID, f"☀️ Доброе утро! Прогноз на сегодня:\n\n{weather}")
            print("✅ Рассылка отправлена")
        except Exception as e:
            print(f"⚠ Ошибка рассылки: {e}")
    else:
        print("⚠ CHAT_ID не указан в .env, рассылка отключена")


def schedule_checker():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == "08:00":
            send_daily_weather()
            time.sleep(60)
        time.sleep(30)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет! Я бот-погода. ☀️\n"
                 "Напиши /weather [город], например: /weather Minsk"
                 )


@bot.message_handler(commands=['weather'])
def weather_command(message):
    city = message.text.replace('/weather', '').strip()
    if not city:
        bot.reply_to(message, "Укажи город! Например: /weather Minsk")
        return
    bot.reply_to(message, get_weather(city))


if __name__ == '__main__':
    print("Бот запущен... 🚀")

    thread = threading.Thread(target=schedule_checker)
    thread.daemon = True
    thread.start()

    bot.infinity_polling()
    
