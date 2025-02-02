import discord
import discord.ext.commands


intents = discord.Intents.default();
intents.message_content = True;

token = input('Input 10hs bot token to start.');

client = discord.Client(intents=intents);
bot = discord.ext.commands.Bot(command_prefix='h!', intents=intents);

@bot.event
async def on_ready():
    print(f'Logged in as {client.user}');
    print(f'Have {len(bot.commands)} commands.');
    await bot.tree.sync();
    pass;


@bot.hybrid_command(name='test', with_app_command=True)
async def test(ctx:discord.ext.commands.Context, message: str):
    print(message);
    await ctx.send('cat');
    pass;

bot.run(token)