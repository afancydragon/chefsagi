#################################################################################################
#                   Discord ----- RoboChef
#   
#################################################################################################

# import packages
import os
import discord
from discord.ext import commands
import json

#           Bot/Status/Token/Prefix
TOKEN =

cmdpre = ['chef ', 'Chef ', 'RoboChef ', 'robochef', 'CHEF ', 'chef', 'CHEF', 'Chef']
description = 'Makes a menu for the week'
extpath = "./Desktop/RoboSousChef/ext" #path to ext folder

botstatus = discord.Game("chef [help]")
bot = commands.Bot(command_prefix=cmdpre, description=description)

################################################################################################
#                      Bot on_ready Events, remove help, and Settings for Game
################################################################################################
@bot.event
async def on_ready():

    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(status=discord.Status.online, activity=botstatus)

bot.load_extension('ext.menu')

@bot.command(hidden = True)
async def l(ctx, extension):
    """Load Extensions"""
    bot.load_extension('ext.'+extension)
    print('Loaded '+extension)

@bot.command(hidden = True)
async def u(ctx,extension):
    """Unload Extensions"""
    bot.unload_extension('ext.'+extension)
    print('Unloaded '+extension)

@bot.command(hidden = True)
async def r(ctx,extension):
    """Reloads Extension"""
    bot.reload_extension('ext.'+extension)
    print('Reloaded '+extension)

@bot.command(hidden = True)
async def el(ctx):
    """Lists extentions"""
    extlist = os.listdir(extpath)
    txt = '\n'
    for x in extlist:
        if (x != "__pycache__"):
            txt = txt+f"{x.strip('.py')} \n"
    await ctx.send(f"```Current Extensions availible: {txt}```")

#                                                   THE CHEF LIVES
bot.run(TOKEN)
