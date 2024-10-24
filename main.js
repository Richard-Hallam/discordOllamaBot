import 'node:fs';
//import ollama from 'ollama' ;
import token from './config.json' assert {type: 'json'};
import {Client, Events, GatewayIntentBits, Collection} from 'discord.js';
import path from 'node:path'
import { Ollama } from 'ollama';
import { response } from 'express';
import { assert } from 'node:console';


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
function splitStringOver2000Characters(stringToCheck){
  let arrayToReturn = []
  while (stringToCheck.length > 1999){
    arrayToReturn.push(stringToCheck.slice(0,1999));
    let stringToCheck = stringToCheck.slice(2000);
  }
  arrayToReturn.push(stringToCheck.slice(0,1999));
  return arrayToReturn;
}


/**
 * creates ollama instance, sends request and awaits response. Returns assembled response
 * @param {string} prompt 
 * @param {string} chatModel 
 * @returns string
 */
async function generateResponse(prompt, chatModel){
  // const ollama = new Ollama({ host: 'http://127.0.0.1:11434' })
  const message = {role: 'user', content: prompt}

  

  const result = await ollama.chat({ model: chatModel, messages: [message], stream: false })
  let stringToReturn = '';
   console.log(result);
   return result.message.content;
}

/**
 * listens for discord message then passes message content to generateResponse()
 */
client.on("ready", () => {
  console.log(`logged in as ${client.user.tag}`)
})

client.on("messageCreate", msg => {
  if (msg.content === ''){
    msg.reply('empty message')
  }else{
    if (msg.author.bot){ 
    } else{

    generateResponse(msg.content, chatModel).then(returnString => (msg.reply('reply:' + returnString)));
}}})





// Log in to Discord with token
client.login(token.token);
