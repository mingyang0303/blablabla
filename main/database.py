import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
global conn, cur

def init(name):
  return psycopg2.connect(DATABASE_URL, sslmode='require')



def setup(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS User
            (
                  user_id int,
                  is_admin bit,
                  diamonds int,
                  bagslot int,
                  maxbagslot int,
                  gold int,
                  exp int,
                  level int

            )
    """)
    conn.commit()
    conn.execute("""CREATE TABLE IF NOT EXISTS Card
                (
                      user_id int,
                      card_name TEXT,
                      eng TEXT

                )
        """)
    conn.commit()
    conn.execute("""CREATE TABLE IF NOT EXISTS Chat
                    (
                          Chat_id int

                    )
            """)
    conn.commit()

def add_user(conn, user_id):
  stmt = """INSERT INTO User (user_id, is_admin, diamonds, bagslot , maxbagslot , gold, exp , level)
VALUES (
  ?,
  0,
  10,
  0,
  50,
  100000,
  0,
  1
)"""
  conn.execute(stmt, (user_id,))
  conn.commit()
  return conn

def add_user_card(conn, user_id , card_name , eng):
  stmt = """INSERT INTO Card (user_id , card_name, eng)
VALUES (
  ?,
  ?,
  ?

)"""
  conn.execute(stmt, (user_id, card_name, eng))
  conn.commit()
  return conn

def get_user_value(conn, user_id: int, items: str):
    stmt = f"SELECT {items} FROM User WHERE user_id={user_id}"
    try:
     r= conn.execute(stmt).fetchone()[0]
    except TypeError:
     r = None
    finally:
     return r

def get_user_card(conn, user_id: int, items: str):
    stmt = f"SELECT card_name FROM Card WHERE user_id={user_id}"
    try:
     r= conn.execute(stmt).fetchall()
    except TypeError:
     r = None
    finally:
     return r

def get_user_card_eng(conn, user_id: int, items: str):
    stmt = f"SELECT eng FROM Card WHERE user_id={user_id}"
    try:
     r= conn.execute(stmt).fetchall()
    except TypeError:
     r = None
    finally:
     return r

def approved_list(conn):
    stmt = f"SELECT Chat_id FROM Chat"
    try:
     r= conn.execute(stmt).fetchall()
    except TypeError:
     r = None
    finally:
     return r

def add_card(conn , user_id : int , card_name : str):
    stmt = f"UPDATE Card card_name = card_name + ? WHERE user_id =?"
    conn.execute(stmt, (card_name,user_id))
    conn.commit()

def add_exp(conn , user_id : int , exp : int):
    stmt = f"UPDATE User SET exp = exp + ? WHERE user_id =?"
    conn.execute(stmt, (exp,user_id))
    conn.commit()

def add_level(conn , user_id : int):
    stmt = f"UPDATE User SET level = level + 1 WHERE user_id =?"
    conn.execute(stmt, (user_id,))
    conn.commit()

def add_diamonds(conn , user_id : int , diamonds : int):
    stmt = f"UPDATE User SET diamonds = diamonds + ? WHERE user_id =?"
    conn.execute(stmt, (diamonds,user_id))
    conn.commit()

def add_slot(conn , user_id : int):
    stmt = f"UPDATE User SET bagslot = bagslot + 1 WHERE user_id =?"
    conn.execute(stmt, (user_id,))
    conn.commit()

def add_gold(conn , user_id : int , gold : int):
    stmt = f"UPDATE User SET gold = gold + ? WHERE user_id =?"
    conn.execute(stmt, (gold,user_id))
    conn.commit()

def minus_gold(conn , user_id : int , gold : int):
    stmt = f"UPDATE User SET gold = gold - ? WHERE user_id =?"
    conn.execute(stmt, (gold,user_id))
    conn.commit()

def buy_slot(conn , user_id : int):
    stmt = f"UPDATE User SET maxbagslot = maxbagslot + 5 WHERE user_id =?"
    conn.execute(stmt, (user_id,))
    conn.commit()

