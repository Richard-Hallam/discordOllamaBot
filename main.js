// Import necessary discord.js classes
const fs = require('node:fs');
const path = require('node:path');
const { Client, Collection, Events, GatewayIntentBits } = require('discord.js');
const { token } = require('./config.json');

// Create a new client instance
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages] });

// Log in client
client.once(Events.ClientReady, readyClient => {
	console.log(`Ready! Logged in as ${readyClient.user.tag}`);
});

client.commands = new Collection();

// Load commands from a directory (assuming you have a commands folder)
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
	const filePath = path.join(commandsPath, file);
	const command = require(filePath);

	// Set a new item in the Collection with the key as the command name and the value as the exported module
	if ('data' in command && 'execute' in command) {
		client.commands.set(command.data.name, command);
	} else {
		console.log(`[WARNING] The command at ${filePath} is missing a required "data" or "execute" property.`);
	}
}

// Handle message-based commands
client.on("messageCreate", msg => {
	console.log(msg);
	if (msg.author.bot) return; // Ignore bot messages

	if (msg.content.includes("ping")) {
		console.log('pong')
		msg.reply("pong");
	}
});

// Handle slash commands
client.on(Events.InteractionCreate, async interaction => {
	if (!interaction.isChatInputCommand()) return; // Ignore non-slash command interactions

	const command = client.commands.get(interaction.commandName);

	if (!command) return;

	try {
		await command.execute(interaction);
	} catch (error) {
		console.error(`Error executing ${interaction.commandName}`);
		interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
	}
});

// Log in to Discord with token
client.login(token);
