from dis import disco
import discord
from discord.ext import commands
import logging
from pathlib import Path
import json
import DiscordUtils
import os

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"-----\n{cwd}\n-----")

secret_file = json.load(open(cwd+'/secrets.json'))

bot = commands.Bot(
    command_prefix='~', 
    case_insensitive=True, 
    intents=discord.Intents.all())
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)
tracker = DiscordUtils.InviteTracker(bot)

bot.version = "0.5"

@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is -\n-----")
    await bot.change_presence(activity=discord.Game(name="Use ~ to interact with me"))
    await tracker.cache_invites()

    for filename in os.listdir(cwd+'/cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command
async def load(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')

@bot.command
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')

bot.run(bot.config_token) # Runs our bot()