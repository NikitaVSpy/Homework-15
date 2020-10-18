import telebot
import config
import datetime
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


# Стартовая панель
@bot.message_handler(commands=["start"])
def start_handler(message):
    stick = open("welcome.webp", "rb")
    bot.send_sticker(message.chat.id, stick)
    # Клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Сделать заметку на сегодня")
    item2 = types.KeyboardButton("Показать заметки на сегодня")
    item3 = types.KeyboardButton("Сделать заметку на завтра")
    item4 = types.KeyboardButton("Показать заметки на завтра")
    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b> бот, созданный чтобы организовать рабочее время и запланировать задачи\nСкажите, что бы вы хотели сделать?".format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


# Анализ выбора
@bot.message_handler(content_types=["text"])
def main_handler(message):
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)

    if message.chat.type == "private":
        if message.text == "Сделать заметку на сегодня":
            note = bot.send_message(message.chat.id, 'Сделайте заметку')
            bot.register_next_step_handler(note, note_today)

        elif message.text == "Показать заметки на сегодня":
            try:
                file = open(f'today/{now.strftime("%d.%m.%Y")}.txt', "r", encoding='utf-8')
                bot.send_message(message.chat.id, f'Заметки на сегодня:\n{file.read()}')
                file.close()
            except IOError:
                bot.send_message(message.chat.id, 'Заметок на сегодня нет')


        elif message.text == "Сделать заметку на завтра":
            note = bot.send_message(message.chat.id, 'Сделайте заметку')
            bot.register_next_step_handler(note, note_tomorrow)

        elif message.text == "Показать заметки на завтра":
            try:
                file = open(f'tomorrow/{tomorrow.strftime("%d.%m.%Y")}.txt', "r", encoding='utf-8')
                bot.send_message(message.chat.id, f'Заметки на завтра:\n{file.read()}')
                file.close()
            except IOError:
                bot.send_message(message.chat.id, 'Заметок на завтра нет')


# Запись заметки на сегодня
def note_today(message):
    now = datetime.datetime.now()
    with open(f'today/{now.strftime("%d.%m.%Y")}.txt', "a", encoding="utf-8") as file:
        file.write(message.text)
    bot.send_message(message.chat.id, f'Сделал заметку на {now.strftime("%d.%m.%Y")}')


# Запись заметки на завтра
def note_tomorrow(message):
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)
    with open(f'tomorrow/{tomorrow.strftime("%d.%m.%Y")}.txt', "a", encoding="utf-8") as file:
        file.write(message.text)
    bot.send_message(message.chat.id, f'Сделал заметку на {tomorrow.strftime("%d.%m.%Y")}')


# Запуск
bot.polling(none_stop=True)
