const { SlashCommandBuilder } = require('discord.js');
/**
 * Handles sending user input to llm
 */
module.exports = {
	data: new SlashCommandBuilder()
		.setName('ping')
		.setDescription('Replies with Pong!'),
	async execute(interaction) {
		await interaction.reply('Pong!');
        console.log(interaction);
	},
};