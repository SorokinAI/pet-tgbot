"""Файл с клавиатурами и кнопками"""
from telebot import types

# кнопка "Вернуться в меню"
btn_menu = types.InlineKeyboardButton('Вернуться в меню', callback_data='go_back')

# клавиатура в главном меню
main_markup = types.InlineKeyboardMarkup()
main_markup.add(types.InlineKeyboardButton('Cписок класса', callback_data='get_classmates'))
main_markup.add(types.InlineKeyboardButton('Список учителей', callback_data='get_teachers'))

# клавиатура для списка класса
markup_cmt = types.InlineKeyboardMarkup()
btn_add_cmt = types.InlineKeyboardButton('Добавить ученика', callback_data='add_classmate')
btn_remove_cmt = types.InlineKeyboardButton('Удалить ученика', callback_data='remove_classmate')
markup_cmt.row(btn_add_cmt, btn_remove_cmt)
markup_cmt.row(btn_menu)

# клавиатура для списка учителей
markup_teacher = types.InlineKeyboardMarkup()
btn_add_teacher = types.InlineKeyboardButton('Добавить учителя', callback_data='add_teacher')
btn_remove_teacher = types.InlineKeyboardButton('Удалить учителя', callback_data='remove_teacher')
markup_teacher.row(btn_add_teacher, btn_remove_teacher)
markup_teacher.row(btn_menu)

# кнопка отмены у "Удалить ученика" и у "Удалить уичтеля" одна, потому что имеет один callback-data
cancel_delete = types.InlineKeyboardButton('Нет❌', callback_data='go_back')

# клавиатура при удалении ученика
markup_cmt_remove = types.InlineKeyboardMarkup()
markup_cmt_remove.row(types.InlineKeyboardButton('Да✔', callback_data='delete_cmt_yes'), cancel_delete)

# клавиатура при удалении учителя
markup_teacher_remove = types.InlineKeyboardMarkup()
markup_teacher_remove.row(types.InlineKeyboardButton('Да✔', callback_data='delete_teacher_yes'), cancel_delete)
