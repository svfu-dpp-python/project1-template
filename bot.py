import sys

from telebot import TeleBot, types
from telebot.util import quick_markup

if __name__ != "__main__":
    print("Этот модуль нельзя импортировать!")
    sys.exit(-1)

# Читаем токен
with open("token.txt") as f:
    token = f.read().strip()

if not token:
    print("Не удалось прочитать токен!")
    sys.exit(-2)

bot = TeleBot(token)


# Команда /start
@bot.message_handler(commands=["start"])
def start_cmd(message: types.Message) -> None:
    user = message.from_user
    bot.send_message(user.id, f"Привет, {user.first_name}!")


# Команда /image
@bot.message_handler(commands=["image"])
def image_cmd(message: types.Message) -> None:
    with open("telegram_logo.png", mode="rb") as f:
        photo = f.read()
    bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=["cat_or_dog"])
def cat_or_dog_cmd(message: types.Message):
    msg = "Кто лучше: кошки или собаки?"
    kbd = quick_markup({
        "Кошки": {"callback_data": "Кошка"},
        "Собаки": {"callback_data": "Собака"},
    })
    bot.send_message(message.chat.id, msg, reply_markup=kbd)


# Обработка нажатия на кнопку
@bot.callback_query_handler(func=lambda call: True)
def cat_or_dog_ans(query: types.CallbackQuery):
    msg = query.message
    bot.answer_callback_query(query.id)
    bot.edit_message_reply_markup(msg.chat.id, msg.id, reply_markup=[])
    bot.send_message(query.message.chat.id, f"{query.data} — это очень мило!")


# Вычисление арифметических выражений в тексте
@bot.message_handler(func=lambda message: True)
def evaluate_msg(message: types.Message):
    try:
        answer = eval(message.text)
        bot.reply_to(message, answer)
    except NameError as e:
        bot.reply_to(message, f"Что такое {e.name}?")
    except ArithmeticError:
        bot.reply_to(message, "В моих вычислениях произошла ошибка.. ☹️")


# Запускаем бота в работу
bot.set_my_commands(commands=[
    types.BotCommand("start", "Начало работы с ботом"),
    types.BotCommand("image", "Отправка картинки"),
    types.BotCommand("cat_or_dog", "Кто лучше: кошки или собаки?"),
])
bot.infinity_polling()
