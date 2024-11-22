import discord
from discord.ext import commands
from discord.ext.commands import CommandInvokeError
import ollama
import time

def getApiKey(filename):
    with open(filename) as f:
        apiKey = f.read()
        print(apiKey)
    return apiKey

def split_long_response(response_to_process):
    split_response = []
    response_to_process_length = len(response_to_process)
    print(response_to_process)
    response = str(response_to_process)
    while len(response_to_process) > 2000:
        split_response.append(response_to_process[0:2000])
        response_to_process = response_to_process[2001:response_to_process_length]
    split_response.append(response_to_process)
    return split_response

async def get_response(messages, modelToUse):
    """Passes command content to ollama
       To implement models"""
    print(modelToUse)
    response = ollama.chat(model=modelToUse, messages=messages)
    return response['message']['content']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

# Define the model variable
model = 'llama3.2'  

# Dictionary to store conversation history for each user
conversation_history = {}

@bot.command(description="tests bot is getting commands")
async def ping(ctx):
    await ctx.send('pong')

@bot.command(description="prompts llm")
async def prompt(ctx, *, msg):
    user_id = ctx.author.id
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    # Add the new message to the conversation history
    conversation_history[user_id].append({
        'role': 'user',
        'content': msg,
    })

    try:
        response = await get_response(conversation_history[user_id], model)
        conversation_history[user_id].append({
            'role': 'assistant',
            'content': response,
        })
        await ctx.send(response)
    except CommandInvokeError:
        await ctx.send('Model not pulled, pulling now. Prompt will be unavailable during this time.')
        await ollama.pull(model)
        await ctx.send(f"{model} pull complete")

# Add bot.run with your token
bot.run(getApiKey('config.txt'))
