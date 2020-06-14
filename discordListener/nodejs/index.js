global.startTime = process.hrtime();
//apis
console.log("getting apis...");
global.path = require('path');
global.fs = require('fs');
global.os = require('os');
global.Commando = require('discord.js-commando');
global.Discord = require('discord.js');

//pull keys file
const keys = JSON.parse(fs.readFileSync('./keys.json')); //read all keys
//keys
console.log("pulling keys...");
global.token = keys.discordtoken; //discord api key
global.botSudoId = keys.botsudo; //bot sudo id

//debug setup
global.prefix = "s!"

//bot settings
console.log("configuring commando...");
//make client global
global.client = new Commando.Client({
	owner: botSudoId,
	commandPrefix: prefix,
	disableEveryone: true,
	unknownCommandResponse: false
});
global.discordClient = new Discord.Client();

//audio file saving func
function generateOutputFile(channel, member) {
	// use IDs instead of username cause some people have stupid emojis in their name
	const fileName = `./recordings/${channel.id}-${member.id}-${Date.now()}.pcm`;
	return fs.createWriteStream(fileName);
  }

//command groups
client.registry
	.registerDefaultTypes()
	.registerGroups([
		['listen', 'listening ability']
	])
	.registerDefaultGroups()
	.registerDefaultCommands()
	.registerCommandsIn(path.join(__dirname, 'commands'));
//ready?
client.on('ready', () => {
	console.log(`Logged in as ${client.user.tag}!`);
	global.servers = (`Servers:\n${client.guilds.map(g => g.name).join("\n")}`);
	console.log(`Servers:\n${client.guilds.map(g => g.name).join("\n")}`);
	let localUsers = client.users.array().length;
	let updatePres = setInterval(function () {
		let localUsers = client.users.array().length;
		client.user.setPresence({
			game: {
				name: `how many funko pops do YOu have? | ${localUsers} users`,
				type: 0
			}
		});
	}, 60000);
	updatePres;
});

//handlers for errors and disconnects
client.on('disconnect', function (event) {
	if (event.code != 1000) {
		console.log("Discord client disconnected with reason: " + event.reason + " (" + event.code + "). Attempting to reconnect in 6s...");
		setTimeout(function () {
			client.login(token);
		}, 6000);
	}
});

client.on('error', function (err) {
	console.log("Discord client error '" + err.code + "'. Attempting to reconnect in 6s...");
	client.destroy();
	setTimeout(function () {
		client.login(token);
	}, 6000);
});

process.on('rejectionHandled', (err) => {
	console.log(err);
	console.log("an error occurred. reconnecting...");
	client.destroy();
	setTimeout(function () {
		client.login(token);
	}, 2000);
});

process.on('exit', function () {
	client.destroy();
});

client.login(token);