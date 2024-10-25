const { SlashCommandBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
    .setName('prompt')
    .setDescription('Sends prompt to llm'),
    async execute(interaction) {
         console.log(interaction);//will be async when not console.log
    },
}