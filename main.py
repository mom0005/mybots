import os
import subprocess
import sys
from colorama import init, Fore, Back, Style
import time

init()

def console_picture():
    print(Style.BRIGHT + Fore.YELLOW)
    print("  _____          _                           _            ____            _   ")
    print(" |_   _|  _ __  (_)   __ _   _ __     __ _  | |   ___    | __ )    ___   | |_ ")
    print("   | |   | '__| | |  / _` | | '_ \   / _` | | |  / _ \   |  _ \   / _ \  | __|")
    print("   | |   | |    | | | (_| | | | | | | (_| | | | |  __/   | |_) | | (_) | | |_ ")
    print("   |_|   |_|    |_|  \__,_| |_| |_|  \__, | |_|  \___|   |____/   \___/   \__|")
    print("                                     |___/                                    ")
console_picture()
print("Нажми Enter чтобы запустить...")
input()

while (True):
    process = subprocess.Popen([sys.executable, "bot_V2.py"])
    process.wait()
