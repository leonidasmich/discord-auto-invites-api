import discord
from discord.ext import commands, tasks
import asyncio
from fastapi import HTTPException
import requests
from dotenv import load_dotenv
import os

load_dotenv()

GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.invites = True

bot = commands.Bot(command_prefix='!', intents=intents)

invite_url = None  

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    generate_invite.start()  

@tasks.loop(hours=24)
async def generate_invite():
    global invite_url
    guild_id = GUILD_ID  # Replace with your server's ID
    channel_id = CHANNEL_ID  # Replace with the channel ID where you want to post the invite
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id)
    invite = await channel.create_invite(max_uses=0, unique=True)
    invite_url = invite.url
    print(f"Generated new invite link: {invite_url}")
    
    
    with open('invite_url.txt', 'w') as file:
        file.write(invite_url)

@generate_invite.before_loop
async def before_generate_invite():
    await bot.wait_until_ready()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(TOKEN))  # Replace with your bot token

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
