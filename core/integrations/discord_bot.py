from os import getenv
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

bot = commands.Bot(command_prefix='>')


@bot.event
async def on_ready():
    await bot.get_channel(int(getenv('STONKS_CHANNEL_ID'))).send('Sup dorks!')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(getenv('DISCORD_TOKEN'))
