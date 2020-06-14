const {
	Command
} = require('discord.js-commando');

module.exports = class JoinCommand extends Command {
	constructor(client) {
		super(client, {
			name: 'leave',
			group: 'listen',
			memberName: 'leave',
			description: 'leaves channel',
			examples: ['leave']
		});
	}
	async run(msg, args) {
        // If the client isn't in a voiceChannel, don't execute any other code
        if(!msg.guild.voiceConnection)
        {
            msg.reply("i'm not in a call")
            return;
        }

        // Get the user's voiceChannel (if he is in one)
        let userVoiceChannel = msg.member.voiceChannel;

        // Return from the code if the user isn't in a voiceChannel
        if (!userVoiceChannel) {
            return;
        }

        // Get the client's voiceConnection
        let clientVoiceConnection = msg.guild.voiceConnection;

        // Compare the voiceChannels
        if (userVoiceChannel === clientVoiceConnection.channel) {
            // The client and user are in the same voiceChannel, the client can disconnect
            clientVoiceConnection.disconnect();
            msg.channel.send('im out fam');
        } else {
            // The client and user are NOT in the same voiceChannel
            msg.channel.send('You can only execute this command if you share the same voiceChannel as the client!');
        }
        }
};