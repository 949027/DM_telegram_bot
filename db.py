import sqlite3


conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

#Создание таблицы "Вещи"
def create_table_things():
    cursor.execute("""CREATE TABLE things
                      (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                       name TEXT, 
                       image TEXT,
                       owner TEXT)
                   """)

#получить рандомную вещь
def get_random_thing(id_user):
    print(id_user)
    sql = "SELECT * FROM things WHERE owner IS NOT ?" \
          "ORDER BY RANDOM()" \
          "LIMIT 1"
    cursor.execute(sql, [(id_user)])
    return cursor.fetchone()

#print(get_random_thing(20046788))



def create_table_wishes():
#Создание таблицы "Желания"
    cursor.execute("""CREATE TABLE wishes
                          (user TEXT,
                           id TEXT)
                       """)

#Внесение вещи в таблицу
def add_thing(name, image, owner):
    cursor.execute("""INSERT INTO things VALUES (NULL, ?, ?, ?)""", [(name), (image), (owner)])
    conn.commit()

#Внесение вещи в список желаний
def add_wish(user, id_wish):
    cursor.execute("""INSERT INTO wishes VALUES (?, ?)""", [(user), (id_wish)])
    conn.commit()

#Получить вещь по id
def get_thing(id):
    sql = "SELECT * FROM things WHERE id = ?"
    cursor.execute(sql, [(id)])
    return cursor.fetchall()[0]

#Получить все вещи одного хозяина
def get_all_things(owner):
    sql = "SELECT * FROM things WHERE owner = ?"
    cursor.execute(sql, [(owner)])
    return cursor.fetchall()

#Показать таблицу Вещи
def show_things():
    sql = "SELECT * FROM things "
    cursor.execute(sql)
    return cursor.fetchall()

#Получить любую вещь юзера
def get_one_thing(user):
    sql = "SELECT * FROM things WHERE owner = ?"
    cursor.execute(sql, [(user)])
    return cursor.fetchone()

#ТАБЛИЦА ПРИОРИТЕТНЫХ ВЕЩЕЙ

#Создание таблицы Приоритет
def create_table_priority_things():
    cursor.execute("""CREATE TABLE priority_things
                          (id_target_user TEXT,
                           id_thing TEXT,
                           id_owner TEXT)
                       """)
#Добавить запись в таблицу приоритет "SELECT * FROM things WHERE owner = ?" [(id_user), (id_owner)]
def add_priority_things(id_user, id_target_user):
    sql = """INSERT INTO priority_things SELECT ?, id, owner FROM things WHERE owner=? """
    cursor.execute(sql, [(id_user), (id_target_user)])
    conn.commit()
#print(show_things())

#add_priority_things(200466788, 89088)

#удалить таблицу приоритетных вещей
def delete_priority_things():
    sql = "DELETE FROM priority_things"

    cursor.execute(sql)
    conn.commit()
#delete_priority_things()






#Проверка совпадения id юзера и хозяина вещи
def check_for_matches(id_user, id_owner):
    #print(show_priority_things())
    sql = "SELECT * FROM priority_things WHERE id_owner = ? AND id_user = ?"
    cursor.execute(sql, [(id_owner), (id_user)])
    conn.commit()
    #print('check=', cursor.fetchone())
    #print(show_priority_things())
    return cursor.fetchone()

#print(check_exchange(115225, 4585211))

#Удалить запись из таблицы приоритета
def delete_priority_thing(id_user, id_thing):
    sql = "DELETE FROM priority_things WHERE id_user=? AND id_thing=?"
    cursor.execute(sql, [(id_user), (id_thing)])
    conn.commit()

#Показать таблицу приоритета
def show_priority_things():
    sql = "SELECT * FROM priority_things "
    cursor.execute(sql)
    return cursor.fetchall()

#Достать первую вещь из таблицы приоритета (с удалением)
def cut_priority_thing(id_user):
    #print(id_user)
    sql = "SELECT id_thing FROM priority_things WHERE id_user=?"
    cursor.execute(sql, [(id_user)])
    try:
        id_thing = cursor.fetchone()[0]
    except:
        id_thing = None
    #print('id_thing=', id_thing)

    #print(id_thing)
    sql = "DELETE FROM priority_things WHERE id_user=? AND id_thing=?"
    cursor.execute(sql, [(id_user), (id_thing)])
    conn.commit()
    return id_thing




#print(cut_priority_thing(200466788))
#create_table_priority_things()
#add_priority_thing(200466788, 1, 1064554654)
#print(cut_priority_thing(200466788))
#print(show_priority_things())


#create_table_things()
#add_thing(325475, 'Vitaly_1041573069\\3.jpg', '4534556546')
#add_thing('Самокат', '200466788/AgACAgIAAxkBAAIExGFNi7HOtbALQhHveRr0zPt7tWOdAAJItjEbt65oSmG4xlSdXhQLAQADAgADbQADIQQ.jpg', '346446541')
# add_thing('Кепка', 'http://.....', '@username')
# print(get_thing(3))
# print(get_all_things('@Ivan'))
#print(get_one_thing(2458))

#print(show_things())
