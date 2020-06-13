const {
	Command
} = require('discord.js-commando');

//audio file saving func
function generateOutputFile(channel, member) {
    // use IDs instead of username cause some people have stupid emojis in their name
    const fileName = `./recordings/${channel.id}-${member.id}-${Date.now()}.opus`;
    return fs.createWriteStream(fileName);
    }

module.exports = class JoinCommand extends Command {

	constructor(client) {
		super(client, {
			name: 'rec',
			group: 'listen',
			memberName: 'rec',
			description: 'joins/records channel',
			examples: ['rec']
		});
    }

	async run(msg) {
        var voiceChannel = msg.member.voiceChannel;
        if (voiceChannel) {
            await voiceChannel.join()
                .then(connection => {
                    msg.reply("in call, pog");
                    msg.channel.send("zack is gay")

                    var vcMembers = voiceChannel.members.array()

                    // console.log(voiceChannel.members.array())
                    // var vcArray = String(voiceChannel.members.array())
                    // // var vcJson = JSON.stringify(vcArray);
                    // fs.writeFile("./vcArray", vcArray, function(err) {
                    //     if(err) {
                    //         return console.log(err);
                    //     }
                    //     console.log("json saved");
                    // }); 
                    for (var i in vcMembers) {
                        console.log(i)
                        console.log(connection.status)
                        var guildMember = vcMembers[i]
                        console.log(guildMember.user.username)
                        // console.log(connection)
                        // var stream = connection.receiver.createStream(guildMember.user, {'mode': 'opus', 'end': 'silence'})
                        // const outputStream = generateOutputFile(voiceChannel, guildMember.user);
                        // stream.pipe(outputStream);

                        // console.log(stream)
                        
                    }
                    
                    var loop = true
                    while (true) {
                        while  (loop) {
                        console.log("in while loop")
                        var loop = false
                        }
                        connection.on('speaking', (member, speaking) => {
                            console.log(speaking)
                            // if (speaking) {
                            //     console.log('sup dog');
                            // }
                            // else {
                            //     console.log(`a guild member starts/stops speaking: ${member.tag}`);
                            // }
                            
                        });
                    }
                
                //     connection.reciever('speaking', (user, speaking) => {
                //         msg.channel.send("zack is still gay")
                //         if (speaking) {
                //             //oop
                //             msg.channel.send(`I'm listening to ${user}`);
                //             // this creates a 16-bit signed PCM, stereo 48KHz PCM stream.
                //             const audioStream = receiver.createStream(user);
                //             // create an output stream so we can dump our data in a file
                //             const outputStream = generateOutputFile(voiceChannel, user);
                //             // pipe our audio data into the file stream
                //             audioStream.pipe(outputStream);
                //             outputStream.on("data", console.log);
                //             // when the stream ends (the user stopped talking) tell the user
                //             audioStream.on('end', () => {
                //                 msg.channel.send(`I'm no longer listening to ${user}`);
                //             });
                //         }

                // });
            });
        }
        else {
            msg.reply('get in call retard');
        }
	}
};

