# import ollama
# import discord
# from discord.ext import commands

# def getApiKey(filename):
#   with open(filename) as f:
#     apiKey = f.read()
#     print(apiKey)
#   return apiKey


# async def prompt(message):
#   response = ollama.chat(model='llama3.1', messages=[
#     {
#       'role': 'user',
#       'content': message,
#     },
#   ])
#   return(response['message']['content'])

 

# intents = discord.Intents.default()
# intents.message_content = True
# bot = commands.Bot(command_prefix='>', intents=intents)

# @bot.command(description="tests bot is getting commands")
# async def ping(ctx):
#     await ctx.send('pong')

# @bot.command(description="prompts llm")
# async def prompt(ctx, *, msg):
#   response = await prompt(msg)
#   await ctx.send(response)

# bot.run(getApiKey("config.txt"))


# print(1) 

import ollama
import discord
from discord.ext import commands

def getApiKey(filename):
  with open(filename) as f:
    apiKey = f.read()
    print(apiKey)
  return apiKey

async def get_response(message):
  response = ollama.chat(model='llama3.1', messages=[
    {
      'role': 'user',
      'content': message,
    },
  ])
  return response['message']['content']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command(description="tests bot is getting commands")
async def ping(ctx):
    await ctx.send('pong')

@bot.command(description="prompts llm")
async def prompt(ctx, *, msg):
  response = await get_response(msg)
  await ctx.send(response)

bot.run(getApiKey("config.txt"))
