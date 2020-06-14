global.startTime = process.hrtime();
//apis
console.log("getting apis...");
global.path = require('path');
global.fs = require('fs');
global.os = require('os');
global.Discord = require('discord.js');

//pull keys file
const keys = JSON.parse(fs.readFileSync('./keys.json')); //read all keys
//keys
console.log("pulling keys...");
global.token = keys.discordtoken; //discord api key
global.botSudoId = keys.botsudo; //bot sudo id

//debug setup
global.prefix = "s!"

//make client global
global.client = new Discord.Client({
	owner: botSudoId,
	commandPrefix: prefix,
	disableEveryone: true,
	unknownCommandResponse: false
});

//audio file saving func
function generateOutputFile(channel, member) {
	// use IDs instead of username cause some people have stupid emojis in their name
	const fileName = `./recordings/${channel.id}-${member.id}-${Date.now()}.pcm`;
	return fs.createWriteStream(fileName);
  }

//ready?
client.on('ready', () => {
	console.log(`Logged in as ${client.user.tag}!`);
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

client.on('message', message => { //check for message
			if (message.author.equals(client.user)) return; //check if the client sent the message, if so ignore
			if (!message.content.startsWith(prefix)) return; //check for prefix
			var args = message.content.substring(prefix.length).split(" "); //take each argument
			switch (args[0].toLowerCase()) {
				//reply statements
				case "help":
					message.channel.send('hello my name is dnak bot, i am a dnak discrod bot made by djmango. features include youtube music, youtube playlists and custom definitions. type ./commands for commands')
					break;
				case "rec":
					var voiceChannel = message.member.voice.channel;
					if (voiceChannel) {
						voiceChannel.join()
							.then(conn => {
								message.reply("in call, pog");
								const receiver = conn.receiver;

								conn.play('jingle.mp3');

								conn.on('speaking', (user, speaking) => {
									if (speaking) {
										message.channel.send(`I'm listening to ${user}`);
										// this creates a 16-bit signed PCM, stereo 48KHz PCM stream.
										const audioStream = receiver.createStream(user);
										// create an output stream so we can dump our data in a file
										const outputStream = generateOutputFile(voiceChannel, user);
										// pipe our audio data into the file stream
										audioStream.pipe(outputStream);
										outputStream.on("data", console.log);
										// when the stream ends (the user stopped talking) tell the user
										audioStream.on('end', () => {
											message.channel.send(`I'm no longer listening to ${user}`);
										});
									}
								})
							})
					} else {
						message.reply('get in call retard');
					}
					break;
			}
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