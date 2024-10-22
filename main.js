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


/**
 * creates ollama instance, sends request and awaits response. Returns assembled response
 * @param {string} prompt 
 * @param {string} chatModel 
 * @returns string
 */
async function generateResponse(prompt, chatModel){
  const ollama = new Ollama({ host: 'http://127.0.0.1:11434' })
  const message = {role: 'user', content: prompt}

  const result = await ollama.chat({ model: chatModel, messages: [message], stream: true })
  let stringToReturn = ''
   console.log(await result)
   const responseParts = [];
    for await (const part of result) {
      stringToReturn += part.message.content;
      responseParts.push(part.message.content);
   }
   console.log(responseParts)
   console.log(stringToReturn)
   let yeet = stringToReturn;
   return yeet;

}



//client for discord
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages] });


/**
 * listens for discord message then passes message content to generateResponse()
 */
client.on("ready", () => {
  console.log(`logged in as ${client.user.tag}`)
})

client.on("messageCreate", msg => {
  console.log(msg)
  if (msg.content === ''){
    msg.reply('empty message')
  }else{
    if (msg.author.bot){ 
    } else{
    generateResponse(msg.content, chatModel).then(dcMessage=>(msg.reply(dcMessage)))
}}})





// Log in to Discord with token
client.login(token.token);
