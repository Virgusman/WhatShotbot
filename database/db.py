import sqlite3

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
    cursor.execute('INSERT INTO Users (id_user,name,access,status,points) VALUES (?,?,?,?,?)', (id, name, "User", "not game", 0,))
    conn.commit()
    conn.close()

#Проверка статуса на
def getAccess(id):
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('SELECT access FROM Users WHERE id_user = (?)', (id, ))
    name = cursor.fetchone()
    conn.close()
    return True if name[0] == 'admin' else False

#Добавление нового кадра в базу
def newShot(token,answer):
    conn = sqlite3.connect('database\WhatShot_database.db') 
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Shots (Shot_token,answer,status) VALUES (?,?,?)', (token, answer, "new",))
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
