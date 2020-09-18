from telethon import TelegramClient
import sqlite3
import time
from os.path import exists

db = sqlite3.connect('Account.db')
cur = db.cursor()
accounts = cur.execute(f"SELECT * FROM Account").fetchall()
numberBots = len(accounts)
time.sleep(0.2)

x = 0

while(True):
    if exists("anon"+str(x+1)+".session") == False:
        print("Очередь аккаунта № " + str(x + 1))
        Phone = accounts[x][1]
        print("Входим в аккаунт: " + Phone)
        Password = accounts[x][2]
        print("Пароль: " + Password)
        api_id = accounts[x][3]
        api_hash = accounts[x][4]
        x += 1
        session = str("anon" + str(x))
        client = TelegramClient(session, api_id, api_hash)
        print("На ваш аккаунт был отправлен код")
        client.start(phone=Phone, password=Password)
        time.sleep(0.2)
    else:
        x+=1
    if x == numberBots:
        print("Aккаунты активированы!")
        break
