import 'node:fs';
//import ollama from 'ollama' ;
import token from './config.json' assert {type: 'json'};
import { Client, Events, GatewayIntentBits, Collection, Message } from 'discord.js';
import path, { resolve } from 'node:path'
import { Ollama } from 'ollama';
import { response } from 'express';
import { assert } from 'node:console';
import { type } from 'node:os';


//change this to use a different model
const chatModel = 'llama3.2:3b';

//initialises ollama
const ollama = new Ollama({ host: 'http://127.0.0.1:11434' })

//client for discord
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages] });



/**
 * Takes a string, then loops over it pushing a slice from the 
 * start into an array until the string is under 2000 character
 * @param {string} stringToCheck 
 * @returns 
 */
function splitStringOver2000Characters(stringToCheck) {
  let arrayToReturn = []
  stringToCheck = stringToCheck;
  while (stringToCheck.length > 1999) {
    arrayToReturn.push(stringToCheck.slice(0, 1999));
  }
  arrayToReturn.push(stringToCheck.slice(0, 1999));
  stringToCheck = stringToCheck.slice(2000);
  return arrayToReturn;
}


/**
 * creates ollama instance, sends request and awaits response. Returns assembled response
 * @param {string} prompt 
 * @param {string} chatModel 
 * @returns string
 */
async function generateResponse(prompt, chatModel) {
  // const ollama = new Ollama({ host: 'http://127.0.0.1:11434' })
  const message = { role: 'user', content: prompt }
  const result = await ollama.chat({ model: chatModel, messages: [message], stream: false })
  if (result.message.content.length > 1900) {
    // const responseParts = splitStringOver2000Characters(result.message.content);
    // return responseParts;
    return 'message too long to parse'
  } else {
    return result.message.content;
  }
}

/**
 * listens for discord message then passes message content to generateResponse()
 */
client.on("ready", () => {
  console.log(`logged in as ${client.user.tag}`)
})

client.on("messageCreate", msg => {
  getMessageFromDiscord(msg)
})


/**
 * takes message from discord passes it to ollama function then sends result back to discord
 * @param {Message} msg 
 */
async function getMessageFromDiscord(msg) {
  if (msg.content === '') {
    msg.reply('empty message')
  } else {
    if (msg.author.bot) {
    } else {
      let chatResponse = await generateResponse(msg.content, chatModel)
      if (typeof chatResponse === 'string') {
        generateResponse(msg.content, chatModel).then(returnString => (msg.reply(returnString)));
      } else if (chatResponse.isArray()){
        for (let part of chatResponse){
          msg.reply(part);
          await sleep(3500);
        }
      }
    }
  }
}


/**
 * takes a time in ms and pauses execution for the duration but 
 * needs passing to async function.
 */
function sleep(ms){
  return new Promise(resolve => setTimeout(resolve, ms));
}



// Log in to Discord with token
client.login(token.token);
