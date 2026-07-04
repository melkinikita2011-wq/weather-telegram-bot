import os
import telebot
import requests
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

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

        return (f"🌤 Погода в {city.capitalize()}:"
                f"\n🌡 Температура: {temp}°C (ощущается как {feels_like}°C)"
                f"\n📝 {description.capitalize()}"
                f"\n💧 Влажность: {humidity}%"
                f"\n💨 Ветер: {wind} м/с")

    except Exception as e:
        return f"⚠ Ошибка при получении погоды: {e}"


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет! Я бот-погода. ☀️\n"
                 "Напиши /weather [город], чтобы узнать погоду.\n"
                 "Например: /weather Moscow"
                 )


@bot.message_handler(commands=['weather'])
def weather_command(message):
    city = message.text.replace('/weather', '').strip()

    if not city:
        bot.reply_to(message, "Укажи город! Например: /weather Minsk")
        return

    weather_text = get_weather(city)
    bot.reply_to(message, weather_text)


if __name__ == '__main__':
    print("Бот запущен... 🚀")
    bot.infinity_polling()