

// Import necessary discord.js classes
import 'ollama';
import 'node:fs';
import ollama from 'ollama' ;
import token from './config.json' assert {type: 'json'};

let prompt = 'reply with You have to give me a prompt to generate from!';

const chatModel = 'llama3.2:3b';

async function generateResponse(prompt){
  const result = await ollama.generate({
    model:chatModel,
    prompt:prompt,
    steam:false,
  })
  console.log( response.message)
  return response;
}

import {Client, Events, GatewayIntentBits, Collection} from 'discord.js';
import path from 'node:path'
import { Ollama } from 'ollama';
import { response } from 'express';
import { assert } from 'node:console';

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages] });

// Log in client and respond when ready
client.once(Events.ClientReady, (readyClient) => {
  console.log(`Ready! Logged in as ${readyClient.user.tag}`);
// Log in client and respond when ready
client.once(Events.ClientReady, (readyClient) => {
  console.log(`Ready! Logged in as ${readyClient.user.tag}`);
});

client.on('messageCreate', async (msg) => {
  // if (!msg.content.trim()) return; // Ignore empty messages

  // if (msg.author.bot) return; // Ignore bot messages
client.on('messageCreate', async (msg) => {
  // if (!msg.content.trim()) return; // Ignore empty messages

  // if (msg.author.bot) return; // Ignore bot messages

  // if (msg.content.toLowerCase().includes('ping')) {
    console.log(1)
  //const reply = await generateResponse(msg.content)
    //console.log(await generateResponse(msg.content))
    //let replyToDC = msg.reply(generateResponse(prompt));
    let replyToDC = console.log(await generateResponse(prompt));
  
});


  // if (msg.content.toLowerCase().includes('ping')) {
    console.log(1)
  //const reply = await generateResponse(msg.content)
    //console.log(await generateResponse(msg.content))
    //let replyToDC = msg.reply(generateResponse(prompt));
    let replyToDC = console.log(await generateResponse(prompt));
  
});



// Log in to Discord with token
client.login(token.token);
client.login(token.token);

//append return questions in the following format before the prompt
//append return questions in the following format before the prompt