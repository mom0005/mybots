import sqlite3
import time
from telethon import TelegramClient
from telethon import sync, events
import re
import json
import multiprocessing
from multiprocessing import Manager

db = sqlite3.connect('Account.db')
cur = db.cursor()
accounts = cur.execute(f"SELECT * FROM Account").fetchall()
numberBots = len(accounts)
time.sleep(0.2)

def checker(summ, flag):
    while True:
        time.sleep(5)
        print(f'flag -> {flag.value}, bots -> {numberBots}')
        if flag.value == numberBots:
            print(f'Сумма --> {summ.value}')
            break

def balance(x, summ, flag):
    Phone = accounts[x][1]
    print(f"Входим в аккаунт -> {x+1}: {Phone}")
    api_id = accounts[x][3]
    api_hash = accounts[x][4]
    session = str("anon" + str(x+1))
    client = TelegramClient(session, api_id, api_hash)
    client.start()

    dlgs = client.get_dialogs()
    for dlg in dlgs:
        if dlg.title == 'LTC Click Bot':
            tegmo = dlg

    client.send_message('LTC Click Bot', "/balance")
    time.sleep(10)
    msgs = client.get_messages(tegmo, limit=1)

    for mes in msgs:
        str_a = str(mes.message)
        zz = str_a.replace('Available balance: ', '')
        qq = zz.replace(' LTC', '')
        print(qq)
        waitin = float(qq)
    summ.value += waitin
    flag.value += 1
    time.sleep(1)

if __name__ == "__main__":
    manager = Manager()
    summ = manager.Value(int, 0)
    flag = manager.Value(int, 0)
    for num in range(numberBots):
        p = multiprocessing.Process(target=balance, args=(num, summ, flag, ))
        p.start()
    p = multiprocessing.Process(target=checker, args=(summ, flag, ))
    p.start()
    time.sleep(100)
