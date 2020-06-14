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
            const conn = await msg.member.voiceChannel.join();
            msg.reply("in call, pog");
            const receiver = conn.receiver;

            conn.play('jingle.mp3');

            conn.on('speaking', (user, speaking) => {
            if (speaking) {
                msg.channel.sendMessage(`I'm listening to ${user}`);
                // this creates a 16-bit signed PCM, stereo 48KHz PCM stream.
                const audioStream = receiver.createPCMStream(user);
                // create an output stream so we can dump our data in a file
                const outputStream = generateOutputFile(voiceChannel, user);
                // pipe our audio data into the file stream
                audioStream.pipe(outputStream);
                outputStream.on("data", console.log);
                // when the stream ends (the user stopped talking) tell the user
                audioStream.on('end', () => {
                    msg.channel.sendMessage(`I'm no longer listening to ${user}`);
                });
                }
            })
        }
        else {
            msg.reply('get in call retard');
        }
	}
};

