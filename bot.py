import json
import sys
from urllib import request

from telebot import TeleBot, types
from telebot.util import quick_markup

if __name__ != "__main__":
    # Если модуль запускается при импортировании
    print("Этот модуль нельзя импортировать!")
    # Выход с ошибкой
    sys.exit(-1)

# Читаем токен из файла
with open("token.txt") as f:
    token = f.read().strip()

if not token:
    # Если токен не удалось прочитать
    print("Не удалось прочитать токен!")
    # Выход с ошибкой
    sys.exit(-2)

# Создаем бота с токеном
bot = TeleBot(token)


# Команда /start
@bot.message_handler(commands=["start"])
def start_cmd(message: types.Message) -> None:
    # Извлекаем отправителя сообщения
    user = message.from_user
    # Отправляем ему сообщение
    bot.send_message(user.id, f"Привет, {user.first_name}!")


# Команда /image
@bot.message_handler(commands=["image"])
def image_cmd(message: types.Message) -> None:
    # Читаем картинку из файла
    with open("telegram_logo.png", mode="rb") as f:
        photo = f.read()
    # Отправляем картинку в чат
    bot.send_photo(message.chat.id, photo)


# Команда /cat_or_dog
@bot.message_handler(commands=["cat_or_dog"])
def cat_or_dog_cmd(message: types.Message):
    # Готовим сообщение
    msg = "Кто лучше: кошки или собаки?"
    # Готовим кнопки
    kbd = quick_markup({
        "Кошки": {"callback_data": "cat"},
        "Собаки": {"callback_data": "dog"},
    })
    # Отправляем в чат сообщение с кнопками
    bot.send_message(message.chat.id, msg, reply_markup=kbd)


# Обработка нажатия на кнопку
@bot.callback_query_handler(func=lambda call: True)
def cat_or_dog_ans(query: types.CallbackQuery):
    # Находим исходное сообщение с кнопками из запроса
    msg = query.message
    # Отвечаем на запрос (на каждый запрос нужно ответить)
    bot.answer_callback_query(query.id)
    # Убираем кнопки в исходном сообщении
    bot.edit_message_reply_markup(msg.chat.id, msg.id, reply_markup=[])
    if query.data == "cat":
        # Отправляем в чат случайную картинку с котом
        bot.send_photo(msg.chat.id, "https://cataas.com/cat")
    elif query.data == "dog":
        # Отправляем в чат случайную картинку с собакой
        response = request.urlopen("https://random.dog/woof.json")
        url = json.loads(response.read())["url"]
        ext = url.lower().rsplit(".", maxsplit=1)[1]
        if ext == "gif":
            bot.send_animation(msg.chat.id, url)
        elif ext == "mp4":
            bot.send_video(msg.chat.id, url)
        else:
            bot.send_photo(msg.chat.id, url)
    else:
        bot.send_message(msg.chat.id, "Ээ.. это очень мило!")


# Вычисление арифметических выражений в тексте
@bot.message_handler(func=lambda message: True)
def evaluate_msg(message: types.Message):
    try:
        # Пытаемся вычислить значение выражения
        result = eval(message.text)
        # В ответ на сообщение отправляем результат
        bot.reply_to(message, result)
    except NameError as e:
        # Пользователь упомянул текст как будто это переменная
        bot.reply_to(message, f"Что такое {e.name}?")
    except ArithmeticError:
        # Возникла арифметическая ошибка
        bot.reply_to(message, "В моих вычислениях произошла ошибка.. ☹️")


# Задаем команды, доступные через кнопку меню
bot.set_my_commands(commands=[
    types.BotCommand("start", "Начало работы с ботом"),
    types.BotCommand("image", "Отправка картинки"),
    types.BotCommand("cat_or_dog", "Кто лучше: кошки или собаки?"),
])
# Запускаем бота в работу
bot.infinity_polling()
