from discord.ext import commands
import discord
import os
import time
import requests
import random
import string
import re
import ctypes
from bs4 import BeautifulSoup
import string
import argparse as parser
import os

ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )

bot = commands.Bot(command_prefix="scraper$$$")
embed_color = 0x404040

max_session_requests = 10000

headers = {
    'authority': 'prnt.sc',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

def get_img_url(code):
    html = requests.get(f"http://prnt.sc/{code}", headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    img_url = soup.find_all('img', {'class': 'no-click screenshot-image'})
    return img_url[0]['src']


@bot.event
async def on_ready():
    amount = 0
    
    try:
        open(".mt")
    except:
        pass
    else:
        os.remove(".mt")
        __stime__ =  time.strftime("%H:%M:%S", time.localtime())
        print(f"> {__stime__}  [MAINTENANCE] Announcing...")
        for file in os.listdir("servers"):
            if file.endswith(".txt"):
                try:
                    __stime__ =  time.strftime("%H:%M:%S", time.localtime())
                    channel = bot.get_channel(int(open(f"servers/{file}", "r").read()))
                    await channel.send(embed=discord.Embed(description=f"Maintenance mode is deactivated!", color=embed_color))
                    print(f"> {__stime__}  [MAINTENANCE] Notified {channel}")
                except:
                    pass

        await bot.get_channel(957995450735161404).send(embed=discord.Embed(description=f"Maintenance mode is deactivated!", color=embed_color))

    rpc = random.randint(1,3)
    if rpc == 1:
        await bot.change_presence(activity=discord.Streaming(name="https://discord.gg/UHwQFNktvU", url="https://xello.blue/i/"))
    elif rpc == 2:
        await bot.change_presence(activity=discord.Streaming(name="scraping images from ctrlv.cz...", url="https://xello.blue/i/"))
    else:
        await bot.change_presence(activity=discord.Streaming(name="$help :^)", url="https://xello.blue/i/"))

    mode = "ctrlv"
    while True:

        try: #maintenance mode
            open(".mt")
        except:
                pass
        else:
            os._exit(0)

        try:
            __ctime__ =  time.strftime("%H:%M:%S", time.localtime())
            if mode == "ctrlv":
                #generating & requesting url
                img = "".join(random.choice(string.ascii_letters) for i in range(4))
                link = f"https://ctrlv.cz/{img}"
                #link = "https://ctrlv.cz/ODfx"

                r = requests.get(f"{link}")
                if "/images/notexists.png" in r.text: #invalid url
                    pass
                else: #valid url
                    open("dump/link.txt", "w").write(r.text)
                    with open("dump/link.txt") as f:
                        urls = f.read()
                        links = re.findall('"((http)s?://ctrlv.cz/shots.*?)"', urls)

                    for url in links:
                        print(f"[CTRLV.CZ] VALID: {url[0]}")

                        download = requests.get(url[0])
                        open(f'dump/image.png', 'wb').write(download.content)

                        chat_append = random.randint(0,500)

                        for file in os.listdir("servers"):
                            if file.endswith(".txt"):
                                try:
                                    c_id = open(f"servers/{file}", "r").read()
                                    channel = bot.get_channel(int(c_id))

                                    if chat_append < 10:
                                        await channel.send(f"<{url[0]}>\n**Do you also want this on your server? see guide on how to add me here:** https://discord.gg/UHwQFNktvU", file=discord.File("dump/image.png"))
                                    else:
                                        await channel.send(f"<{url[0]}>", file=discord.File("dump/image.png"))
                                    __stime__ =  time.strftime("%H:%M:%S", time.localtime())
                                    print(f"> {__stime__}  [POST] Sending the link to {channel}")
                                except Exception as err:
                                    __stime__ =  time.strftime("%H:%M:%S", time.localtime())
                                    print(f"> {__stime__}  [ERROR] '{err}'")
                                    if f"{err}" == "'NoneType' object has no attribute 'send'":
                                        print(f"> {__stime__}  [ERROR] Removing {file}...")
                                        os.remove(f"servers/{file}")
                    mode = "prntsc"
            else:
                
                code = "".join(random.choice(string.digits + string.ascii_lowercase) for i in range(6))
                url = get_img_url(code)
                chat_append = random.randint(0,500)
                response = requests.get(url)
                if response.status_code == 200:
                    with open("dump/image.png", 'wb') as f:
                        f.write(response.content)
                    image = open("dump/image.png", "rb").read()
                    image_error = open("dump/image-error.png", "rb").read()
                    if image != image_error:
                        print(f"[PRNT.SC] VALID: {url}")
                        for file in os.listdir("servers"):
                                if file.endswith(".txt"):
                                    try:
                                        c_id = open(f"servers/{file}", "r").read()
                                        channel = bot.get_channel(int(c_id))

                                        if chat_append < 10:
                                            await channel.send(f"<{url}>\n**Do you also want this on your server? see guide on how to add me here:** https://discord.gg/UHwQFNktvU", file=discord.File("dump/image.png"))
                                        else:
                                            await channel.send(f"<{url}>", file=discord.File("dump/image.png"))
                                        __stime__ =  time.strftime("%H:%M:%S", time.localtime())
                                        print(f"> {__stime__}  [POST] Sending the link to {channel}")
                                    except Exception as err:
                                        __stime__ =  time.strftime("%H:%M:%S", time.localtime())
                                        print(f"> {__stime__}  [ERROR] '{err}'")
                                        if f"{err}" == "'NoneType' object has no attribute 'send'":
                                            print(f"> {__stime__}  [ERROR] Removing {file}...")
                                            os.remove(f"servers/{file}")
                    mode = "ctrlv"
                    

            amount += 1
            os.system(f"title ctrlvscrape [{amount}] [{__ctime__}]")

            if amount > max_session_requests:
                os.system("start scrape.py")
                os._exit(0)

        except Exception as error:
            print(f"[ERROR] {error}")

bot.run("token") #replace with bot token