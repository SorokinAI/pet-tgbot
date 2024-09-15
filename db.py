"""Файл для работы с базой данных"""
import sqlite3

connect = sqlite3.connect('database.sql')
cursor = connect.cursor()

# Таблица с учениками и учителями
cursor.execute('CREATE TABLE IF NOT EXISTS classmates (id int auto_increment primary key, first_name varchar(50), surname varchar(50), seat_column varchar(2), seat_row varchar(2))')
cursor.execute('CREATE TABLE IF NOT EXISTS teachers (id int auto_increment primary key, first_name varchar(50), surname varchar(50), patronymic varchar(50), class varchar(30))')

connect.commit()
cursor.close()
connect.close()


# Список всех учеников
def classmates():
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM classmates')
    classmates_db = cur.fetchall()

    classmates_return = ''
    n = 0
    for el in classmates_db:
        n += 1
        classmates_return += f'{n}. {el[2]} {el[1]}, ряд: {el[3]}, парта: {el[4]}\n'
    cur.close()
    conn.close()

    return classmates_return


# Список всех учителей
def teachers():
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM teachers')
    teachers_db = cur.fetchall()

    teachers_return = ''
    n = 0
    for el in teachers_db:
        n += 1
        teachers_return += f'{n}. {el[2]} {el[1]} {el[3]}, урок: {el[4]}\n'
    cur.close()
    conn.close()

    return teachers_return


def add_classmate(surname, name, column, row):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO classmates (first_name, surname, seat_column, seat_row) VALUES ('%s', '%s', '%s', '%s')"
                % (name, surname, column, row))
    conn.commit()
    cur.close()
    conn.close()


def add_teacher(surname, name, patronymic, lession):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO teachers (first_name, surname, patronymic, class) VALUES ('%s', '%s', '%s', '%s')"
                % (name, surname, patronymic, lession))
    conn.commit()
    cur.close()
    conn.close()


def delete_classmate(name, surname):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute("DELETE FROM classmates WHERE first_name=('%s') AND surname=('%s')"
                % (name, surname))
    conn.commit()
    cur.close()
    conn.close()


def delete_teacher(name, surname, patronymic):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute("DELETE FROM teachers WHERE first_name=('%s') AND surname=('%s') AND patronymic=('%s')"
                % (name, surname, patronymic))
    conn.commit()
    cur.close()
    conn.close()
