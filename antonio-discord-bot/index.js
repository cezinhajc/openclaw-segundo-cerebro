require('dotenv').config();
  const { Client, GatewayIntentBits, Partials } = require('discord.js');

  const client = new Client({
    intents: [
      GatewayIntentBits.Guilds,
      GatewayIntentBits.GuildMessages,
      GatewayIntentBits.MessageContent ,
      GatewayIntentBits.DirectMessages
    ],
    partials: [Partials.Channel]
  });

  client.once('clientReady', () => {
    console.log(`Bot online como ${client.user.tag}`);
  });

  client.on('messageCreate', async (message) => {
    try {
      if (message.author.bot) return;

      console.log('Mensagem recebida:', message.content);
      console.log('Canal tipo:', message.channel.type);

      await message.reply('Recebi sua mensagem. Teste OK do Antonio.');
    } catch (error) {
      console.error('Erro no messageCreate:', error);
    }
  });

  client.login(process.env.DISCORD_BOT_TOKEN);
