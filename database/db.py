import sqlite3
import random
from datetime import datetime
from services.service import compare

#Функции для работы с базой данных.

#Поиск пользователя по его ID
def find_user(id):
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    info = cursor.execute('SELECT * FROM Users WHERE id_user = (?)', (id, ))
    z = info.fetchall()
    conn.close()
    if z:
        return True
    else:
        return False

#Добавление пользователя     
def add_user(id, name):
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Users (id_user,name,access,status,points) VALUES (?,?,?,?,?)', (id, name, "User", 0, 0,))
    conn.commit()
    conn.close()

#Проверка админского доступа
def getAccess(id):
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('SELECT access FROM Users WHERE id_user = (?)', (id, ))
    name = cursor.fetchone()
    conn.close()
    return True if name[0] == 'admin' else False

#Добавление нового кадра в базу
def newShot(token,answer,id_user):
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Shots (Shot_token,answer,status,id_user) VALUES (?,?,?,?)', (token, answer, "new",id_user,))
    conn.commit()
    conn.close()

#Получение кадра для проверки
def check_shot():
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('SELECT id_shot, Shot_token, answer FROM Shots WHERE status = "new"')
    shot = cursor.fetchone()
    conn.close()
    return shot

#Смена статуса кадра на "ок"
def shot_ok(id_user,id_shot):
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('UPDATE Shots SET status = "ok" WHERE id_shot = (?)', (id_shot,))
    conn.commit()
    cursor.execute('INSERT INTO passed_shots (id_user, id_shot) VALUES (?,?)', (id_user, id_shot,))
    conn.commit()
    cursor.execute('SELECT id_user FROM Shots WHERE id_shot = (?)', (id_shot,))
    id = cursor.fetchone()
    if id[0] != id_user:
        cursor.execute('INSERT INTO passed_shots (id_user, id_shot) VALUES (?,?)', (id[0], id_shot,))
        conn.commit()
    cursor.execute('UPDATE Users SET points = points+1 WHERE id_user = (?)', (id[0],))
    conn.commit()
    conn.close()

#Удаление кадра
def shot_del(id_shot):
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Shots WHERE id_shot = (?)', (id_shot,))
    conn.commit()
    conn.close()

#Получение кадра для игры
def get_shot(id_user):
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute("""SELECT id_shot, Shot_token 
                   FROM Shots WHERE status = "ok" 
                   AND id_shot NOT IN
                   (SELECT id_shot FROM passed_shots WHERE id_user = (?))""", (id_user,))
    shot = cursor.fetchall()
    if shot:
        shot = random.choice(shot)
        cursor.execute('UPDATE Users SET status = (?) WHERE id_user = (?)', (shot[0], id_user,))
        conn.commit()
    else:
        cursor.execute('UPDATE Users SET status = (?) WHERE id_user = (?)', (0, id_user,))
        conn.commit()
    conn.close()
    return shot

#Получение загаданного фильма пользователю
def get_answer(id_user):
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM Users WHERE id_user = (?)', (id_user, ))
    answer = cursor.fetchone()
    if answer[0] != 0:
        cursor.execute('SELECT answer FROM Shots WHERE id_shot = (?)', (answer[0], ))
        answer = cursor.fetchone()
    conn.close()
    return answer[0]

#-1 балл при пропуске кадра
def skip_shot(id_user):
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('SELECT status, points FROM Users WHERE id_user = (?)', (id_user, ))
    point = cursor.fetchone()
    cursor.execute('UPDATE Users SET status = (?) WHERE id_user = (?)', (0, id_user,))
    conn.commit()
    cursor.execute('INSERT INTO passed_shots (id_user, id_shot) VALUES (?,?)', (id_user, point[0]))
    conn.commit()
    conn.close()
    

#Дан правильный ответ
def win_shot(id_user):
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('SELECT status, points FROM Users WHERE id_user = (?)', (id_user, ))
    point = cursor.fetchone()
    cursor.execute('UPDATE Users SET status = (?) WHERE id_user = (?)', (0, id_user,))
    conn.commit()
    cursor.execute('UPDATE Users SET points = (?) WHERE id_user = (?)', (point[1] + 1, id_user,))
    conn.commit()
    cursor.execute('INSERT INTO passed_shots (id_user, id_shot) VALUES (?,?)', (id_user, point[0]))
    conn.commit()
    conn.close()

#Запись в лог при любом ответе
def add_passed(id_user, answer_user):
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (id_user, answer_user, answer, datetime, ans_check ) VALUES (?,?,?,?,?)', 
                   (id_user, answer_user, get_answer(id_user), datetime.now(), compare(get_answer(id_user),answer_user) ))
    conn.commit()
    conn.close()

#Взять количество баллов
def get_points(id_user):
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('SELECT points FROM Users WHERE id_user = (?)', (id_user, ))
    point = cursor.fetchone()
    conn.close()
    return point[0]

#Получить список ID пользователей не в игре
def get_users_notgame():
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('SELECT id_user FROM Users WHERE status = 0')
    users = cursor.fetchall()
    conn.close()
    return users

#Получить 10 лучших игроков
def get_top10():
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('SELECT name, points FROM Users ORDER BY points DESC LIMIT 10')
    users = cursor.fetchall()
    conn.close()
    return users


#Дан не правильный ответ
# def not_win_shot(id_user):
#     conn = sqlite3.connect('database\WhatShot_database.db') 
#     cursor = conn.cursor()
#     cursor.execute('SELECT points FROM Users WHERE id_user = (?)', (id_user, ))
#     point = cursor.fetchone()
#     if point[0] != 0:
#         cursor.execute('UPDATE Users SET points = (?) WHERE id_user = (?)', (point[0] - 1, id_user,))
#         conn.commit()
#     conn.close()