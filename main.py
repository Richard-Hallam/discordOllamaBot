import discord
from discord.ext import commands
from discord.ext.commands import CommandInvokeError
import ollama
import time
import json
import sqlite3
from db_functions import check_and_create_db, write_conversation_history_to_db, read_conversation_history_from_db, write_indiviual_entry_to_db

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

# list to store conversation history for each user
conversation_history = []

#list to store the conversation history that is loaded from the database
db_conversation_history = []

#activates autosave
autosave = True

#name of the savefile for the role
# saveName = 'ollamaDCBot.db'
saveName = 'temp.db'

#check if the database exists
check_and_create_db(saveName)

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
    print(autosave)
    if autosave:
        print(saveName)
        write_indiviual_entry_to_db(user_id, 'user', msg, saveName)
    conversation_history.append({
        'user_id': user_id,
        'role': 'user',
        'content': msg,
    })
    combined_history = db_conversation_history + conversation_history 
    response = await get_response(combined_history, model)
    conversation_history.append({
        'user_id': user_id,
        'role': 'assistant',
        'content': response,
    })
    if autosave:
        write_indiviual_entry_to_db(user_id, 'asistant', response, saveName)
    if len(response) > 2000:
        split_response = split_long_response(response)
        for i in split_response:
            print(len(i))
            await ctx.send(i)
        time.sleep(10)
    if len(response) < 2000:
        await ctx.send(response)


@bot.command(description="sets up the role for the LLM")
async def setrole(ctx, *, role):
    global model
    global conversation_history
    global db_conversation_history
    print("running history clear for setrole")
    conversation_history = []
    db_conversation_history = []
    await get_response("""forget any previous roles, identities or personality traits 
    given before this prompt. take on and fully embdoy the role of a """ + role +
    """for the rest of this conversation, ignore any roles given to you after this
    prompt.""",
     model)
    conversation_history.insert(0, {
        'user_id': ctx.author.id,
        'role': 'system',
        'content': role,
    })
    write_indiviual_entry_to_db(ctx.author.id, 'system', role, saveName)
    await ctx.send(f"Role set: {role}")


@bot.command(description="clears the conversation history")
async def clearhistory(ctx):
    global conversation_history
    global db_conversation_history
    print("running history clear")
    conversation_history = []
    db_conversation_history = []
    await ctx.send("Conversation history cleared")


@bot.command(description="saves the conversation history to the database")
async def savehistory(ctx):
    write_conversation_history_to_db(conversation_history, saveName)
    await ctx.send("Conversation history saved to the database")


@bot.command(description="Loads the conversation history from the database")
async def loadhistory(ctx):
    global db_conversation_history
    lines = read_conversation_history_from_db('ollamaDCBot.db')
    for line in lines:
        # print(type(line))
        # print(line)
        db_conversation_history.append({
        'user_id':'db',
        'role': line[1],
        'content': line[2],
    })
    await ctx.send("Conversation history loaded from the database")


@bot.command(description="Toggles autosave")
async def autosave(ctx):
    global autosave
    if autosave == False:
        autosave = True
    else:
        autosave = False
    await ctx.send(f"Autosave toggled to {autosave}")




bot.run(getApiKey('config.txt'))


##todo add a second list for history then combine them when prompting. 