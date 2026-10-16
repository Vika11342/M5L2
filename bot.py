import telebot
from config import *
from logic import *
manager = DB_Map(DATABASE)
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:  ...")
    # Допиши команды бота


@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    try:
        city_name = message.text.split()[-1]
        img_path = 'city_map.png'
        
        if manager.get_coordinates(city_name):
            manager.create_grapf(img_path, [city_name]) # Обрати внимание: create_grapf с буквой f, как у тебя в logic.py
            with open(img_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.send_message(message.chat.id, "Такого города нет в базе данных.")
    except IndexError:
        bot.send_message(message.chat.id, "Пожалуйста, укажи название города после команды, например: /show_city London")
    # Реализуй отрисовку города по запросу


@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    if cities:
        img_path = 'my_cities_map.png'
        manager.create_grapf(img_path, cities)
        with open(img_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, "Ты еще не добавил ни одного города. Используй команду /remember_city!")
    # Реализуй отрисовку всех городов


if __name__=="__main__":
    manager.create_user_table()
    bot.polling()
