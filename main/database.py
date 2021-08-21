import os
import psycopg2

def init(url):
    global conn, cur
    conn = psycopg2.connect(url, sslmode='require')
    cur = conn.cursor()
    print(url)



def setup():
    conn.autocommit = True
    cur.execute("SELECT VERSION();")
    print("Connected to", cur.fetchone())
    cur.execute("""CREATE TABLE IF NOT EXISTS User
            (
                  user_id serial primary key,
                  is_admin bool,
                  diamonds integer,
                  bagslot integer,
                  maxbagslot integer,
                  gold integer,
                  exp integer,
                  level integer
            );
    """)
    conn.commit()
    cur.execute("""CREATE TABLE Card
                (
                      user_id integer,
                      card_name text,
                      eng text

                );
        """)
    conn.commit()
    cur.execute("""CREATE TABLE Chat
                    (
                          chat_id integer

                    );
            """)
    conn.commit()

def add_user(user_id):
  stmt = """INSERT INTO User (user_id, is_admin, diamonds, bagslot , maxbagslot , gold, exp , level)
VALUES (
  %s,
  0,
  10,
  0,
  50,
  100000,
  0,
  1
);"""
  cur.execute(stmt, (user_id,))
  conn.commit()
  return conn

def add_user_card(user_id , card_name , eng):
  stmt = """INSERT INTO Card (user_id , card_name, eng)
VALUES (
  %s,
  %s,
  %s
);"""
  cur.execute(stmt, (user_id, card_name, eng))
  conn.commit()

def get_user_value(user_id: int, items: str):
    stmt = f"SELECT {items} FROM User WHERE user_id={user_id};"
    try:
     cur.execute(stmt)
     r = cur.fetchone()[0]
    except TypeError:
     r = None
    finally:
     return r

def get_user_card(user_id: int, items: str):
    stmt = f"SELECT card_name FROM Card WHERE user_id={user_id};"
    try:
     cur.execute(stmt)
     r = cur.fetchall()
    except TypeError:
     r = None
    finally:
     return r

def get_user_card_eng(user_id: int, items: str):
    stmt = f"SELECT eng FROM Card WHERE user_id={user_id};"
    try:
     cur.execute(stmt)
     r = cur.fetchall()
    except TypeError:
     r = None
    finally:
     return r

def approved_list():
    stmt = f"SELECT chat_id FROM Chat;"
    try:
     cur.execute(stmt)
     r = cur.fetchall()
    except TypeError:
     r = None
    finally:
     return r

def add_card(user_id : int , card_name : str):
    stmt = f"UPDATE Card card_name = card_name + %s WHERE user_id =%s;"
    cur.execute(stmt, (card_name,user_id))
    conn.commit()

def add_exp(user_id : int , exp : int):
    stmt = f"UPDATE User SET exp = exp + %s WHERE user_id = %s;"
    cur.execute(stmt, (exp,user_id))
    conn.commit()

def add_level(user_id : int):
    stmt = f"UPDATE User SET level = level + 1 WHERE user_id = %s;"
    cur.execute(stmt, (user_id,))
    conn.commit()

def add_diamonds(user_id : int , diamonds : int):
    stmt = f"UPDATE User SET diamonds = diamonds + ? WHERE user_id = %s;"
    cur.execute(stmt, (diamonds,user_id))
    conn.commit()

def add_slot(user_id : int):
    stmt = f"UPDATE User SET bagslot = bagslot + 1 WHERE user_id = %s;"
    cur.execute(stmt, (user_id,))
    conn.commit()

def add_gold(user_id : int , gold : int):
    stmt = f"UPDATE User SET gold = gold + %s WHERE user_id =%s;"
    cur.execute(stmt, (gold,user_id))
    conn.commit()

def minus_gold(user_id : int , gold : int):
    stmt = f"UPDATE User SET gold = gold - %s WHERE user_id = %s;"
    cur.execute(stmt, (gold,user_id))
    conn.commit()

def buy_slot(user_id : int):
    stmt = f"UPDATE User SET maxbagslot = maxbagslot + 5 WHERE user_id =%s;"
    cur.execute(stmt, (user_id,))
    conn.commit()

