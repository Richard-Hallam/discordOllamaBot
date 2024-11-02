import ollama
import discord
import time
from discord.ext import commands

model = "llama3.2:3b"#default llm model


def getApiKey(filename):
  with open(filename) as f:
    apiKey = f.read()
    print(apiKey)
  return apiKey


def  split_long_response(response_to_process):
  split_response = []
  response_to_process_length = len(response_to_process)
  print(response_to_process)
  response = str(response_to_process)
  # if len(response_to_process) > 10000:
  #   return('responses over 10000 characters not currently supported')
  while len(response_to_process) > 2000:
    split_response.append(response_to_process[0:2000])
    response_to_process = response_to_process[2001:response_to_process_length]
  split_response.append(response_to_process)
  return split_response


async def get_response(message, modelToUse):
  """Passes command content to ollama
     To impliment models"""
  print(modelToUse)
  response = ollama.chat(model = modelToUse, messages=[
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
  try:
    response = await get_response(msg, model)
  except CommandInvokeError:
    await ctx.send('model not pulled, pulling now prompt will be unavailable during this time.')
    await ollama.pull('model')
    await ctx.send(f"{model} pull complete")
  else:
    if len(response) < 2000:
      await ctx.send(response)
    else:
      response_array = split_long_response(response)
      print(response_array)
      for item in response_array:
        await ctx.send(item)
        time.sleep(5)
        #print(item)
      await ctx.send('response end')


@bot.command(description="changes llm model")
async def selectModel(ctx, msg):
  """Changes llm model that is selected"""
  global model 
  model = msg
  await ctx.send(f"Model changed to {model}")

  

bot.run(getApiKey("config.txt"))
