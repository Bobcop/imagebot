from http import server
from discord.ext import commands
import discord
import os
import time
import requests
import random
import string
import re
from discord.ext.commands import Bot, has_permissions, CheckFailure
import pyfiglet
import ctypes

bot = commands.Bot(command_prefix="$")
bot.remove_command("help")

admin_id = 0 #your id (integer)
whitelist_id = "friends id" #your friends id (string)

ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )

command_list = """[>] Commands:
$help - this page
$add <#channel> - starts sending random images from ctrlv.cz
$remove - stops sending the images
"""

embed_color = 0x404040

def ctime():
    c = time.strftime("%H:%M:%S", time.localtime())
    return c

#admin checks

def acheck(id):
    if f"{id}" in whitelist_id:
        return "wl"
    elif id == admin_id:
        return "admin"
    else:
        return "bl"

#events--------------------------------------------------------

@bot.event #on ready
async def on_ready():
    os.system("title ctrlv.cz scrape - bot")
    print(pyfiglet.figlet_format("Ctrlv Scrape"))
    __ctime__ =  time.strftime("%H:%M:%S", time.localtime())
    print(f"> {ctime()}  [TASK] Bot launched")

@bot.event #command error
async def on_command_error(ctx, error):
    embed = discord.Embed(title=error, description=command_list, color=embed_color)
    await ctx.reply(embed=embed)

@bot.event #command
async def on_command(ctx):
    if ctx.command.name != "add" or ctx.command.name != "remove": 
        print(f"> {ctime()}  [COMMAND] {ctx.command.name}")

#commands---------------------------------------------------------

#admin only--------------------------------------------------

admin_commands = """[Admin commands]:
$servers #shows all the servers the bot is in
$announce <text> #send a message to the system channel
$say <text> #broadcasts the message
"""

@bot.command() #ahelp----------------------------------
async def ahelp(ctx):
    if acheck(ctx.message.author.id) == "wl" or "admin":
        user = ctx.message.author
        embed = discord.Embed(description=f"```ini\n{admin_commands}```")
        await user.send(embed=embed)
    else:
        embed = discord.Embed(title=f"Command \"{ctx.command.name}\" is not found", description=command_list, color=embed_color)
        await ctx.reply(embed=embed)

@bot.command() #servers------------------------
async def servers(ctx):
    if acheck(ctx.message.author.id) == "wl" or "admin":
        activeservers = bot.guilds
        __servers__ = ""
        for guild in activeservers:
            #active check
            try:
                open(f"servers/{guild.id}.txt")
            except:
                __servers__ += f"[{guild.name}]: {guild.id}\n"
            else:
                __servers__ += f"[{guild.name}]: {guild.id} [ACTIVE]\n"

        await ctx.reply(embed=discord.Embed(title="Server list:", description=f"```{__servers__}```", color=embed_color))
    else:
        embed = discord.Embed(title=f"Command \"{ctx.command.name}\" is not found", description=command_list, color=embed_color)
        await ctx.reply(embed=embed)

@bot.command() #announce--------
async def announce(ctx, *, message=None):
    if acheck(ctx.message.author.id) == "wl" or "admin":
        if message != None:
            embed = discord.Embed(title=f"[!] Announcement:", description=message, color=embed_color)
            for guild in bot.guilds:
                try:
                    if guild.id != 957994760801509406:
                        await guild.system_channel.send(embed=embed)
                except:
                    pass
            await bot.get_channel(957995450735161404).send(embed=embed)
    else:
        embed = discord.Embed(title=f"Command \"{ctx.command.name}\" is not found", description=command_list, color=embed_color)
        await ctx.reply(embed=embed)

@bot.command() #say--------------
async def say(ctx, *, message=None):
    if acheck(ctx.message.author.id) == "wl" or "admin":
        if message != None:
            for file in os.listdir("servers"):
                if file.endswith(".txt"):
                    c_id = open(f"servers/{file}", "r").read()
                    channel = bot.get_channel(int(c_id))
                    try:
                        await channel.send(embed=discord.Embed(title=f"[Broadcast] {ctx.author.name}#{ctx.author.discriminator}:" ,description=message, color=0xf673ff))
                    except:
                        pass
            await ctx.reply(embed=discord.Embed(description="Broadcasted the message to everyone", color=embed_color))
    else:
        embed = discord.Embed(title=f"Command \"{ctx.command.name}\" is not found", description=command_list, color=embed_color)
        await ctx.reply(embed=embed)

@bot.command() #maintenance---------------------
async def maintenance(ctx, *, message=None):
    if ctx.message.author.id == admin_id:
        open(".mt", "w")
        for file in os.listdir("servers"):
            if file.endswith(".txt"):
                c_id = open(f"servers/{file}", "r").read()
                channel = bot.get_channel(int(c_id))
                try:
                    if message == None:
                        await channel.send(embed=discord.Embed(title="[!] Maintenance", description="```Please wait... the bot won't work for a while, you'll be notified when we're online!```", color=0xff7d7d))
                    else:
                        await channel.send(embed=discord.Embed(title="[!] Maintenance", description=f"```Please wait... the bot won't work for a while, you'll be notified when we're online!\n> {message}```", color=0xff7d7d))
                except:
                    pass
        if message == None:
            await bot.get_channel(957995450735161404).send(embed=discord.Embed(title="[!] Maintenance", description="```Please wait... the bot won't work for a while, you'll be notified when we're online!```", color=0xff7d7d))
        else:
            await bot.get_channel(957995450735161404).send(embed=discord.Embed(title="[!] Maintenance", description=f"```Please wait... the bot won't work for a while, you'll be notified when we're online!\n> {message}```", color=0xff7d7d))
        await ctx.reply(embed=discord.Embed(description="Maintenance mode activated", color=embed_color))
        os._exit(0)
    else:
        embed = discord.Embed(title=f"Command \"{ctx.command.name}\" is not found", description=command_list, color=embed_color)
        await ctx.reply(embed=embed)

#force commands------------------------------------------------------------

@bot.command() #forceadd
async def forceadd(ctx, channel: discord.TextChannel=None):
    if acheck(ctx.message.author.id) == "admin" or "wl" or channel != None:
        open(f"servers/{ctx.guild.id}.txt", "w").write(f"{channel.id}")

        embed = discord.Embed(description="Channel whitelisted", color=embed_color)
        print(f"> {ctime()}  [COMMAND] {ctx.command.name}: Whitelisted channel '#{channel.name}' {ctx.guild.name}")
        await channel.send(embed=embed)
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title=f"Command \"{ctx.command.name}\" is not found", description=command_list, color=embed_color)
        await ctx.reply(embed=embed)

@bot.command() #forcedel
async def forcedel(ctx):
    if acheck(ctx.message.author.id) == "admin" or "wl":
        try:
            open(f"servers/{ctx.guild.id}.txt")
        except:
            embed = discord.Embed(description="This server hasn't got any channel on the whitelist", color=embed_color)
            await ctx.reply(embed=embed)
        else:
            try:
                channel = open(f"servers/{ctx.guild.id}.txt", "r").read()
                os.remove(f"servers/{ctx.guild.id}.txt")
            except Exception as err:
                embed = discord.Embed(description=f"Something went wrong... {err}", color=embed_color)
                await ctx.send(embed=embed)
            else:
                print(f"> {ctime()}  [COMMAND] {ctx.command.name}: Unwhitelisted channel '#{bot.get_channel(int(channel)).name}' in {ctx.guild.name}")
                embed = discord.Embed(description=f"Whitelist removed from this server (<#{channel}>)", color=embed_color)
                await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title=f"Command \"{ctx.command.name}\" is not found", description=command_list, color=embed_color)
        await ctx.reply(embed=embed)

#public--------------------------------------------------------------

@bot.command() #help---------------------------
async def help(ctx, command="$"): #```
    command = command.lower()
    if command == None:
        await ctx.send(f"```{command_list}```") 
    elif command == "add":
        await ctx.send(f"```[>] $add <channel>\nadds the server (channel) on the whitelist\n\n*admin permissions required```")
    elif command == "remove":
        await ctx.send(f"```[>] $remove\nremoves whitelist for the server\n\n*admin permissions required```")
    elif command == "help":
        await ctx.send(f"```[>] $help [command]\nThis page```")
    else:
        await ctx.send(f"```{command_list}```")

@bot.command() #add-------------------------------
@has_permissions(administrator=True)
async def add(ctx, channel: discord.TextChannel):
    open(f"servers/{ctx.guild.id}.txt", "w").write(f"{channel.id}")

    embed = discord.Embed(description="Channel whitelisted", color=embed_color)
    print(f"> {ctime()}  [COMMAND] {ctx.command.name}: Whitelisted channel '#{channel.name}' {ctx.guild.name}")
    await channel.send(embed=embed)
    await ctx.reply(embed=embed)

@bot.command() #remove----------------------------
@has_permissions(administrator=True)
async def remove(ctx):
    try:
        open(f"servers/{ctx.guild.id}.txt")
    except:
        embed = discord.Embed(description="This server hasn't got any channel on the whitelist", color=embed_color)
        await ctx.reply(embed=embed)
    else:
        try:
            channel = open(f"servers/{ctx.guild.id}.txt", "r").read()
            os.remove(f"servers/{ctx.guild.id}.txt")
        except Exception as err:
            embed = discord.Embed(description=f"Something went wrong... {err}", color=embed_color)
            await ctx.send(embed=embed)
        else:
            print(f"> {ctime()}  [COMMAND] {ctx.command.name}: Unwhitelisted channel '#{bot.get_channel(int(channel)).name}' in {ctx.guild.name}")
            embed = discord.Embed(description=f"Whitelist removed from this server (<#{channel}>)", color=embed_color)
            await ctx.reply(embed=embed)
    
bot.run("token") #replace with bot token