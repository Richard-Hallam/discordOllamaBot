import discord
from discord.ext import commands
from discord.ext.commands import CommandInvokeError
import ollama
import time
import json
import sqlite3


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
        split_response.append(response_to_process[0:1999])
        response_to_process = response_to_process[1999:response_to_process_length]
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
        print(response)
        if len(response) > 2000:
            split_response = split_long_response(response)
            for i in split_response:
                print(len(i))
                await ctx.send(i)
                time.sleep(10)
        if len(response) < 2000:
            await ctx.send(response)
    except CommandInvokeError:
        await ctx.send('Model not pulled, pulling now. Prompt will be unavailable during this time.')
        await ollama.pull(model)
        await ctx.send(f"{model} pull complete")


@bot.command(description="sets up the role for the LLM")
async def setrole(ctx, *, role):
    user_id = ctx.author.id
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    if user_id in conversation_history:
        conversation_history[user_id].clear()

    # Add the role to the conversation history
    conversation_history[user_id].insert(0, {
        'role': 'system',
        'content': role,
    })
    await ctx.send(f"Role set: {role}")


# Add bot.run with your token
bot.run(getApiKey('config.txt'))
