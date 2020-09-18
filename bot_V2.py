from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telethon import sync, events
import requests
import json
import hashlib
import time
import re
from telethon import TelegramClient
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
import webbrowser
import urllib.request
import os
import sqlite3
import multiprocessing
import time

db = sqlite3.connect('Account.db')
cur = db.cursor()
accounts = cur.execute(f"SELECT * FROM Account").fetchall()
numberBots = len(accounts)
time.sleep(0.2)

def checker(tasks, taskMode, botMode):
    while True:
        time.sleep(3)
        string = ''
        for task in tasks:
            string += f'  {str(task)}  '
        print(string)
        string = ''
        for mode in taskMode:
            string += f'  {mode}  '
        print(string)
        string = ''
        for mode in botMode:
            string += f'  {mode}  '
        print(f'{string}\n')

class RunChromeTests():
    def testMethod(self, url_rec, waitin):
        selenium_url = "http://localhost:4444/wd/hub" 
        caps = {'browserName': 'chrome'}
        driver = webdriver.Remote(command_executor=selenium_url, desired_capabilities=caps)
        driver.set_page_load_timeout(30)
        driver.maximize_window()
        driver.get(url_rec)
        time.sleep(waitin + 5)
        driver.close()
        driver.quit()

def bot(x, tasks, taskMode, botMode):
    n = 0
    u = 0

    Phone = accounts[x][1]
    print(f"\nВходим в аккаунт: {x+1} --> {Phone}\n")

    api_id = accounts[x][3]
    api_hash = accounts[x][4]
    session = str("anon" + str(x+1))
    client = TelegramClient(session, api_id, api_hash)
    try:
        client.start()
    except:
        print("Connection Error!!!")

    dlgs = client.get_dialogs()
    for dlg in dlgs:
        if dlg.title == 'LTC Click Bot':
            tegmo = dlg
    client.send_message('LTC Click Bot', "🖥 Visit sites")
    time.sleep(15)
    while True:
        time.sleep(6)
        if u == 2:
            botMode[x] = 'W'
            n = 0
            taskMode[x] = '-'
            time.sleep(3600*5)
        tasks[x] = n
        botMode[x] = 'G'
        msgs = client.get_messages(tegmo, limit=1)
        for mes in msgs:
            if re.search(r'\bseconds to get your reward\b', mes.message):
                str_a = str(mes.message)
                zz = str_a.replace('You must stay on the site for', '')
                qq = zz.replace('seconds to get your reward.', '')
                waitin = int(qq)
                taskMode[x] = f'r({waitin})'
                client.send_message('LTC Click Bot', "/visit")
                time.sleep(3)
                msgs2 = client.get_messages(tegmo, limit=1)
                for mes2 in msgs2:
                    button_data = mes2.reply_markup.rows[1].buttons[1].data
                    message_id = mes2.id
                    taskMode[x] = f'r --> {waitin}'
                    time.sleep(2)
                    try:
                        url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                    except:
                        print(messages[0].reply_markup)
                        break
                    ch = RunChromeTests()
                    
                    ch.testMethod(url_rec, waitin)
                    fp = urllib.request.urlopen(urllib.request.Request(url_rec, headers={'User-Agent': 'Mozilla/5.0'}))
                    bytes = fp.read()
                    mystr = bytes.decode("utf8")
                    fp.close()
                    if re.search(r'\bSwitch to reCAPTCHA\b', mystr):
                        resp = client(GetBotCallbackAnswerRequest(
                            'LTC Click Bot',
                            message_id,
                            data=button_data
                        ))
                        time.sleep(2)
                        print("КАПЧА!")

            elif re.search(r'\bSorry\b', mes.message):
                u = u + 1

            else:
                taskMode[x] = 'S'
                messages = client.get_messages('Litecoin_click_bot')
                try:
                    url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                except:
                    print(messages[0].reply_markup)
                    break
                try:
                    f = open(f"per{x}.txt")
                except:
                    f = open(f"per{x}.txt", 'w')
                fd = f.read()
                if fd == url_rec:
                    #print("Найдено повторение переменной")
                    msgs2 = client.get_messages(tegmo, limit=1)
                    for mes2 in msgs2:
                        button_data = mes2.reply_markup.rows[1].buttons[1].data
                        message_id = mes2.id
                        resp = client(GetBotCallbackAnswerRequest(
                            tegmo,
                            message_id,
                            data=button_data
                        ))
                        time.sleep(2)
                else:
                    waitin = 15
                    try:
                        data1 = requests.get(url_rec).json
                    except:
                        print("Request Error!!!")
                        break

                    my_file = open(f'per{x}.txt', 'w')
                    my_file.write(url_rec)
                    #print("Новая запись в файле сделана")
                    time.sleep(12)
                    n += 1

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    t = [0 for i in range(numberBots)]
    tasks = manager.list(t)
    tM = ['S' for i in range(numberBots)]
    taskMode = manager.list(tM)
    bM = ['G' for i in range(numberBots)]
    botMode = manager.list(bM)
    for num in range(numberBots):
        p = multiprocessing.Process(target=bot, args=(num, tasks, taskMode, botMode, ))
        p.start()
    
    p = multiprocessing.Process(target=checker, args=(tasks, taskMode, botMode, ))
    p.start()
    p.join()
