import ollama from 'ollama'

let chatModel = 'llama3.2:3b';
let prompt = 'make a haiku about a bird who speaks in haiku';

const response = await ollama.chat(
    {
    model: chatModel,
    messages: [{role:'user', content: prompt}]
    }
)