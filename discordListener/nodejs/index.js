var startTime = process.hrtime();
//apis
console.log("getting apis...");
const path = require('path');
const fs = require('fs');
const os = require('os');
const Discord = require('discord.js');
const superagent = require('superagent');
const express = require("express");


//pull keys file
const keys = JSON.parse(fs.readFileSync('./keys.json')); //read all keys
//keys
console.log("pulling keys...");
var token = keys.discordtoken; //discord api key
var botSudoId = keys.botsudo; //bot sudo id

const port = '5001'
var prefix = "s!"

var api = express();
api.use(express.static(__dirname + '/'));

//make client global
var client = new Discord.Client({
	owner: botSudoId,
	commandPrefix: prefix,
	disableEveryone: true,
	unknownCommandResponse: false
});

//audio file saving func
function generateOutputFile(channel, member) {
	// use IDs instead of username cause some people have stupid emojis in their name
	const fileName = `audio/${channel.id}-${member.id}-${Date.now()}.pcm`;
	console.log('creating file')
	return fs.createWriteStream(fileName)
  }

const sleep = (waitTimeInMs) => new Promise(resolve => setTimeout(resolve, waitTimeInMs));

function checkApi(callback) { // this is god awful and i hate javascript for this reason
	console.log('checking api')
	superagent.get('http://python-manager:5000/alive')
		.end((err, res) => {
			if (err) {
				console.log('api not up, retrying in 5..');
				sleep(5000).then(() => {
					// This will execute  5 seconds from now
					checkApi()
				});
			}
			else {
				console.log(res.body);
				if (res.body == 'OKAY') {
					callback();
				}
				else checkApi()
			}
		});
}

//ready?
client.on('ready', () => {
	console.log(`Logged in as ${client.user.tag}!`);
	console.log('waiting for python manager..')
	checkApi(function() {
		console.log('yay it found it')
	})

	let updatePres = setInterval(function () {
		client.user.setPresence({
			game: {
				name: `how many funko pops do YOu have?`,
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
					message.channel.send('i am fongus. red.')
					break;
				case "te":
					console.log('teetetete')
					superagent.get('http://python-manager:5000/')
						.end((err, res) => {
							if (err) {
								return console.log(err);
							}
							console.log(res.body);
						});
					break;
				case "rec":
					var voiceChannel = message.member.voice.channel;
					if (voiceChannel) {
						voiceChannel.join()
							.then(conn => {
								message.reply("in call, pog");
								const receiver = conn.receiver;

								conn.play('jingle.mp3');

								var vcMembers = voiceChannel.members.array()

								for (var i in vcMembers) {
									var guildMember = vcMembers[i]
									console.log(guildMember.user.username)
									// console.log(connection)
									var stream = receiver.createStream(guildMember.user, {'mode': 'pcm', 'end': 'manual'})
									const outputStream = generateOutputFile(voiceChannel, guildMember)
									stream.pipe(outputStream);
								}
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

api.get("/", (req, res) => {
	console.log('deeeeeeeeeeeeeeeeeeeeeeeeee')
	res.send("Hello World");
});

api.get("/alive", (req, res) => {
	superagent.get('http://python-manager:5000/')
		.end((err, res) => {
			if (err) {
				return console.log(err);
			}
			console.log(res.body);
			if (res.body == 'OKAY') apiUp = true;
		});
	res.send("OKAY");
});

api.post('/add', (req, res) => {
	// console.log(req);
	res.json({
		'f': 'ffffffffffffffffffffff'
	})
	console.log('Post request recieved')
});

api.listen(port, () => {
	console.log("API is up, port:" + port);
});

client.login(token);