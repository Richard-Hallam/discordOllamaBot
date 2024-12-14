import discord
from discord.ext import commands
from discord.ext.commands import CommandInvokeError
import ollama
import time
import json
import sqlite3
from db_functions import check_and_create_db, write_conversation_history_to_db

def getApiKey(filename):
    with open(filename) as f:
        apiKey = f.read()
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
    try:
        response = ollama.chat(model=modelToUse, messages=messages)
        #print (response)
    except Exception as e:
        print("model not found. Contact admin to add it. selecting default model")
        global model 
        model = 'llama3.2'
        print(e)
        response = {'model': model, 'message': {'role': 'assistant', 'content': 'model not found. Contact admin to add it. selecting default model'}}
        return response['message']['content']
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


@bot.command(description="changes the model")
async def changemodel(ctx, *, model_name):
    global model
    model = model_name
    try:
         get_response("test", model)
         await ctx.send(f"Model changed to {model}")
    except:
        ctx.send(f"Model {model} not found")
    

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
    print(conversation_history)


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


@bot.command(description="clears the conversation history")
async def clearhistory(ctx):
    user_id = ctx.author.id
    if user_id in conversation_history:
        conversation_history[user_id].clear()
        await ctx.send("Conversation history cleared")


@bot.command(description="saves the conversation history to the database")
async def savehistory(ctx):
    write_conversation_history_to_db(conversation_history, 'ollamaDCBot.db')
    await ctx.send("Conversation history saved to the database")


# Add bot.run with your token
bot.run(getApiKey('config.txt'))
