import requests
import time
import threading
import json
import random
import os
import platform

author = "m4k0exe"
join_for_more = "https://github.com/m4k0exe"

config = json.load(open('./config.json', 'r', encoding='utf-8'))
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
xtrack = "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InBsLVBMIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwNy4xNjQuNjIuMTAyIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIxMTQuMC41NzM1LjE5OSIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyMTk4MzksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
total, unlocked, locked = 0, 0, 0
time_start = None

class Log:
    def Success(text, highlighted):
        time_now = time.strftime('%H:%M:%S')
        if not highlighted:
            print(f"{time_now} ({author}) {text}")
        else:
            print(f"{time_now} ({author}) {text} {highlighted}")

    def Error(text, highlighted):
        time_now = time.strftime('%H:%M:%S')
        if not highlighted:
            print(f"{time_now} ({author}) ! {text}")
        else:
            print(f"{time_now} ({author}) ! {text} {highlighted}")

def finger():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://discord.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': useragent,
        'X-Track': xtrack,
    }
    proxies = {"http": f"http://{proxy()}"} if not config['proxyless'] else None
    fingerprint = requests.get('https://discord.com/api/v9/experiments', headers=headers, proxies=proxies).json()['fingerprint']
    return fingerprint

def proxy():
    with open('./data/proxies.txt') as f:
        random_line = random.choice(f.readlines()).strip()
        return random_line

def thread_worker(delay):
    while True:
        with open('./data/tokens.txt', 'r') as file:
            lines = file.readlines()

        if lines:
            first_line = lines[0].strip()
            time.sleep(delay)
            check_token(first_line)

            with open('./data/tokens.txt', 'w') as file:
                file.writelines(lines[1:])
        else:
            time.sleep(0.75)
            printresult()
            break

def init():
    global time_start
    time_start = time.time()
    config['delay'] = 0.1  

    delay = config.get('delay', 0.1) 



    thread = threading.Thread(target=thread_worker, args=(delay,))
    thread.start()

def check_token(token):
    global total, unlocked, locked, time_start

    newheaders = {
        'authority': 'discord.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': token,
        'origin': 'https://discord.com',
        'referer': 'https://discord.com/@me',
        'Content-Type': 'application/json',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': useragent,
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'en-US',
        'x-fingerprint': finger(),
        'x-super-properties': xtrack
    }

    proxies = {"http": f"http://{proxy()}"} if not config['proxyless'] else None
    r = requests.get("https://discord.com/api/v9/users/@me/affinities/users", headers=newheaders, proxies=proxies)

    if r.status_code == 200:
        Log.Success('Unlocked', token)
        total += 1
        unlocked += 1
        with open("./checked/unlocked.txt", "a") as f:
            f.write(f"{token}\n")
    else:
        Log.Error('Locked', token)
        total += 1
        locked += 1
        with open("./checked/locked.txt", "a") as f:
            f.write(f"{token}\n")

def printresult():
    print("\n\n\n")
    print(f"Total: {total} | Unlocked: {unlocked} | Locked: {locked} | Elapsed Time: {round(time.time() - time_start, 2)}s")

if __name__ == "__main__":
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

    logo = """
  __  __ _  _   _     ___  ________   ________ 
 |  \/  | || | | |   / _ \|  ____\ \ / /  ____|
 | \  / | || |_| | _| | | | |__   \ V /| |__   
 | |\/| |__   _| |/ / | | |  __|   > < |  __|  
 | |  | |  | | |   <| |_| | |____ / . \| |____ 
 |_|  |_|  |_| |_|\_\\___/|______/_/ \_\______|
                                               
                                               
                made by m4k0exe
    """

    print(logo)
    print("\n\n")
    time.sleep(1)
    init()
