import telebot
import buttons
import db

# переменные для добавления учеников/учителей
name = ''
surname = ''
patronymic = ''
column = None
row = None
lession = ''

bot = telebot.TeleBot('6893380074:AAHaJa99d2DW8zgCI-8o7es-Qb3yHMbVI60')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Главное меню. Какой список тебе нужен?', reply_markup=buttons.main_markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global surname, name
    if callback.data == 'go_back':  # выход в меню
        bot.edit_message_text('Главное меню. Какой список тебе нужен?',
                              callback.message.chat.id, callback.message.message_id, reply_markup=buttons.main_markup)
    elif callback.data == 'get_classmates':  # список учеников
        bot.edit_message_text(f'Cписок учеников в классе:\n{db.classmates()}', callback.message.chat.id,
                              callback.message.message_id, reply_markup=buttons.markup_cmt)
    elif callback.data == 'get_teachers':  # список учителей
        bot.edit_message_text(f'Cписок учителей, ведущих уроки у класса:\n{db.teachers()}', callback.message.chat.id,
                              callback.message.message_id, reply_markup=buttons.markup_teacher)
    elif callback.data == 'add_classmate':  # добавление ученика в бд
        bot.edit_message_text(f'Фамилия и имя?', callback.message.chat.id,
                              callback.message.message_id, reply_markup=None)
        bot.register_next_step_handler(callback.message, classmate_column)
    elif callback.data == 'add_teacher':  # добавление учителя в бд
        bot.edit_message_text(f'ФИО?', callback.message.chat.id,
                              callback.message.message_id, reply_markup=None)
        bot.register_next_step_handler(callback.message, teacher_class)
    elif callback.data == 'remove_classmate':  # удаление ученика из бд
        bot.edit_message_text(f'Фамилия и имя?', callback.message.chat.id,
                              callback.message.message_id, reply_markup=None)
        bot.register_next_step_handler(callback.message, remove_classmate1)
    elif callback.data == 'remove_teacher':  # удаление учителя из бд
        bot.edit_message_text(f'ФИО?', callback.message.chat.id,
                              callback.message.message_id, reply_markup=None)
        bot.register_next_step_handler(callback.message, remove_teacher1)
    elif callback.data == 'delete_cmt_yes':  # согласие на удаление ученика из бд
        db.delete_classmate(name, surname)
        bot.edit_message_text(f'Готово✔\nГлавное меню. Какой список тебе нужен?', callback.message.chat.id,
                              callback.message.message_id, reply_markup=buttons.main_markup)
    elif callback.data == 'delete_teacher_yes':  # согласие на удаление учителя из бд
        db.delete_teacher(name, surname, patronymic)
        bot.edit_message_text(f'Готово✔\nГлавное меню. Какой список тебе нужен?', callback.message.chat.id,
                              callback.message.message_id, reply_markup=buttons.main_markup)


# Функции для добавления ученика
def classmate_column(message):
    global surname, name
    surname, name = message.text.split()
    bot.send_message(message.chat.id, 'Ряд, на котором сидит? (число)')
    bot.register_next_step_handler(message, classmate_row)


def classmate_row(message):
    global column
    column = message.text.strip()
    bot.send_message(message.chat.id, 'Парта, на которой сидит? (число)')
    bot.register_next_step_handler(message, classmate_end)


def classmate_end(message):
    global surname, name, column, row
    row = message.text.strip()
    bot.send_message(message.chat.id, 'Готово✔')

    # перевод в нужный регистр
    surname = surname.capitalize()
    name = name.capitalize()

    db.add_classmate(surname, name, column, row)
    bot.send_message(message.chat.id, 'Главное меню. Какой список тебе нужен?', reply_markup=buttons.main_markup)


# Функции для добавления учителя
def teacher_class(message):
    global surname, name, patronymic
    surname, name, patronymic = message.text.split()
    bot.send_message(message.chat.id, 'Какой урок ведёт этот учитель?')
    bot.register_next_step_handler(message, teacher_end)


def teacher_end(message):
    global surname, name, patronymic, lession
    lession = message.text.strip()
    bot.send_message(message.chat.id, 'Готово✔')
    # перевод в нужный регистр
    surname = surname.capitalize()
    name = name.capitalize()
    patronymic = patronymic.capitalize()
    lession = lession.capitalize()

    db.add_teacher(surname, name, patronymic, lession)
    bot.send_message(message.chat.id, 'Главное меню. Какой список тебе нужен?', reply_markup=buttons.main_markup)


# Функция для удаления ученика из бд
def remove_classmate1(message):
    global surname, name
    surname, name = message.text.split()
    # перевод в нужный регистр
    surname = surname.capitalize()
    name = name.capitalize()

    bot.send_message(message.chat.id, f'Вы точно хотите удалить {surname} {name}?',
                     reply_markup=buttons.markup_cmt_remove)


# Функция для удаления учителя из бд
def remove_teacher1(message):
    global surname, name, patronymic
    surname, name, patronymic = message.text.split()
    # перевод в нужный регистр
    surname = surname.capitalize()
    name = name.capitalize()
    patronymic = patronymic.capitalize()

    bot.send_message(message.chat.id, f'Вы точно хотите удалить {surname} {name}?',
                     reply_markup=buttons.markup_teacher_remove)


bot.polling(none_stop=True)
