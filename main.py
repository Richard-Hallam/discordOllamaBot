import ollama
import discord
from discord.ext import commands

def getApiKey(filename):
  with open(filename) as f:
    apiKey = f.read()
  return apiKey


def prompt():
  response = ollama.chat(model='llama3.1', messages=[
    {
      'role': 'user',
      'content': 'Why is the sky blue?',
    },
  ])
  print(response['message']['content'])



intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run('token')