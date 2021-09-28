import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()


def create_table_things():
    cursor.execute("""CREATE TABLE things
                      (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                       name TEXT, 
                       image TEXT,
                       owner TEXT,
                       category TEXT,
                       chat_id TEXT,
                       username TEXT)
                   """)


def get_random_thing(id_user, category):
    print(id_user)
    sql = "SELECT * FROM things WHERE category=? AND owner IS NOT ?" \
          "ORDER BY RANDOM()" \
          "LIMIT 1"
    cursor.execute(sql, [(category), (id_user)])
    return cursor.fetchone()


def add_thing(name, image, owner, category, chat_id, username):
    cursor.execute(
        """INSERT INTO things VALUES (NULL, ?, ?, ?, ?, ?, ?)""",
        [(name), (image), (owner), (category), (chat_id), (username)]
    )
    conn.commit()


def add_wish(user, id_wish):
    cursor.execute("""INSERT INTO wishes VALUES (?, ?)""", [(user), (id_wish)])
    conn.commit()


def get_thing(id):
    sql = "SELECT * FROM things WHERE id = ?"
    cursor.execute(sql, [(id)])
    return cursor.fetchall()[0]


def get_all_things(owner):
    sql = "SELECT * FROM things WHERE owner = ?"
    cursor.execute(sql, [(owner)])
    return cursor.fetchall()


def show_things():
    sql = "SELECT * FROM things "
    cursor.execute(sql)
    return cursor.fetchall()


def get_one_thing(user):
    sql = "SELECT * FROM things WHERE owner = ?"
    cursor.execute(sql, [(user)])
    return cursor.fetchone()


def create_table_priority_things():
    cursor.execute("""CREATE TABLE priority_things
                          (id_user TEXT,
                           id_thing TEXT,
                           id_owner TEXT)
                       """)


def add_priority_things(id_user, id_target_user):
    sql = """INSERT INTO priority_things SELECT ?, id, owner FROM things WHERE owner=? """
    cursor.execute(sql, [(id_user), (id_target_user)])
    conn.commit()


def delete_priority_things():
    sql = "DELETE FROM priority_things"

    cursor.execute(sql)
    conn.commit()


def check_for_matches(id_user, id_owner):
    sql = "SELECT * FROM liked_things WHERE id_owner = ? AND id_user = ?"
    cursor.execute(sql, [(id_user), (id_owner)])
    conn.commit()
    return cursor.fetchone()


def delete_priority_thing(id_user, id_thing):
    sql = "DELETE FROM priority_things WHERE id_user=? AND id_thing=?"
    cursor.execute(sql, [(id_user), (id_thing)])
    conn.commit()


def show_priority_things():
    sql = "SELECT * FROM priority_things "
    cursor.execute(sql)
    return cursor.fetchall()


def cut_priority_thing(id_user):
    sql = "SELECT id_thing FROM priority_things WHERE id_user=?"
    cursor.execute(sql, [(id_user)])
    try:
        id_thing = cursor.fetchone()[0]
    except:
        id_thing = None
    sql = "DELETE FROM priority_things WHERE id_user=? AND id_thing=?"
    cursor.execute(sql, [(id_user), (id_thing)])
    conn.commit()
    return id_thing


def create_table_liked_things():
    cursor.execute("""CREATE TABLE liked_things
                          (id_user TEXT,
                           id_thing TEXT,
                           id_owner TEXT)
                       """)


def add_thing_like(id_user, id_thing, id_owner):
    cursor.execute(
        """INSERT INTO liked_things VALUES (?, ?, ?)""",
        [(id_user), (id_thing), (id_owner)]
    )
    conn.commit()


def add_thing_priority(id_user, id_thing, id_owner):
    cursor.execute(
        """INSERT INTO priority_things VALUES (?, ?, ?)""",
        [(id_user), (id_thing), (id_owner)]
    )
    conn.commit()


def add_liked_things(id_user, id_target_user):
    sql = """INSERT INTO liked_things SELECT ?, id, owner FROM things WHERE owner=? """
    cursor.execute(sql, [(id_user), (id_target_user)])
    conn.commit()


def show_liked_things():
    sql = "SELECT * FROM liked_things "
    cursor.execute(sql)
    return cursor.fetchall()


def show_things_like():
    sql = "SELECT * FROM things "
    cursor.execute(sql)
    return cursor.fetchall()


def delete_user(id_user):
    cursor.execute('''DELETE FROM priority_things''')
    conn.commit()
    conn.close()

