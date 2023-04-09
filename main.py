from keepalive import keep_alive
import os
import openai
import discord
from discord.ext import commands
from discord.errors import Forbidden

keep_alive()
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
OPENAI_API_KEY = os.environ['OPEN_AI_KEY']
openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def chat(ctx, *, message: str):
    prompt = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{message}",
        max_tokens=2048,
        temperature=0.5,
        )
    response_text = prompt.choices[0].text.strip()
    await ctx.send(response_text[:2000])
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    try:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"{amount} Nachrichten wurden erfolgreich gelöscht.", delete_after=3)
    except Forbidden:
        await ctx.send("Ich habe keine Berechtigung, Nachrichten in diesem Kanal zu löschen.")
bot.run(DISCORD_TOKEN)
