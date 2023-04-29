import telebot
import requests
from telebot import types
import random

# Создание объекта бота с указанием токена доступа
bot = telebot.TeleBot("6179385852:AAG4IZTN-bdb_BykjHI"
                      "-yT5ssOTP3qfa_sM")

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который может "
                          "многое. Вот мой список команд:"
                          "\n/rock_paper_scissors - "
                          "игра в камень ножницы бумага\n"
                          "/flip_coin - игра в орёл или "
                          "решка\n/guess_number - угадай "
                          "число от 1 до 10\n/weather "
                          "(введите город) - узнать погоду "
                          "в городе и что надеть.")

# Обработка /back
@bot.message_handler(commands=['back'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который может "
                          "многое. Вот мой список команд:"
                          "\n/rock_paper_scissors - "
                          "игра в камень ножницы бумага\n"
                          "/flip_coin - игра в орёл или "
                          "решка\n/guess_number - угадай "
                          "число от 1 до 10\n/weather "
                          "(введите город) - узнать погоду "
                          "в городе и что надеть.")




#___________________________________________________________
def get_weather(region):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={region}&appid=6d9e55b280794de32e84f65a3ae2edeb"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"Погода в регионе {region}:\n\n{weather_description}\nТемпература: {int((int(temperature) - 273.15))}°C"
    else:
        return "Не удалось получить данные о погоде."

# Обработка команды /weather
@bot.message_handler(commands=['weather'])
def send_weather(message):
    try:
        region = message.text.split()[1]
        weather = get_weather(region)
        bot.reply_to(message, weather)
    except:
        bot.reply_to(message, "Не удалось получить данные о погоде.")
#___________________________________________________________


# Игра "Камень, ножницы, бумага"
@bot.message_handler(commands=['rock_paper_scissors'])
def play_rock_paper_scissors(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Камень')
    itembtn2 = types.KeyboardButton('Ножницы')
    itembtn3 = types.KeyboardButton('Бумага')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.reply_to(message, "Выбери свой вариант:",
                 reply_markup=markup)
    bot.register_next_step_handler\
        (message, process_rock_paper_scissors_step)

def process_rock_paper_scissors_step(message):
    user_choice = message.text.lower()
    choices = ['камень', 'ножницы', 'бумага']
    bot_choice = random.choice(choices)
    result = determine_rock_paper_scissors_result\
        (user_choice, bot_choice)
    bot.reply_to(message, f"Твой выбор: {user_choice}"
                          f"\nВыбор бота: {bot_choice}\n"
                          f"Результат: {result}")

def determine_rock_paper_scissors_result(user_choice,
                                         bot_choice):
    if user_choice == bot_choice:
        return "Ничья!"
    elif (
        (user_choice == 'камень' and bot_choice
         == 'ножницы') or
        (user_choice == 'ножницы' and bot_choice
         == 'бумага') or
        (user_choice == 'бумага' and bot_choice
         == 'камень')
    ):
        return "Ты победил!"
    else:
        return "Ты проиграл!"

# Игра "Орёл или решка"




# Обработка команды /flip_coin
@bot.message_handler(commands=['flip_coin'])
def flip_coin(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('Орёл')
    button2 = types.KeyboardButton('Решка')
    markup.add(button1, button2)
    bot.reply_to(message, "Выбери орла или решку:",
                 reply_markup=markup)

# Обработка команды /guess_number
@bot.message_handler(commands=['guess_number'])
def guess_number(message):
    bot.reply_to(message, "Я загадал число от 1 до 10."
                          " Попробуй отгадать:")

# Обработка ответов пользователя
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Орёл' or message.text == 'Решка':
        result = random.choice(['Орёл', 'Решка'])
        if message.text == result:
            bot.reply_to(message, f"Ура! Ты угадал,"
                                  f" выпало {result}.")
        else:
            bot.reply_to(message, f"Упс! Ты не угадал,"
                                  f" выпало {result}.")
    elif message.text.isdigit():
        number = random.randint(1, 10)
        guess = int(message.text)
        if guess == number:
            bot.reply_to(message, f"Поздравляю!"
                                  f" Ты угадал"
                                  f" число {number}.")
        else:
            bot.reply_to(message,
                         f"Увы! Ты не угадал,"
                         f" я загадал число {number}.")
    else:
        bot.reply_to(message,
                     "Извини, я не понимаю команду.")


#_______________________________________________________________________




# Запуск бота
bot.polling()

