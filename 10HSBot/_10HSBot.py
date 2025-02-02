import discord
import discord.ext.commands
import requests


intents = discord.Intents.default();
intents.message_content = True;

version = '0.0.1';

dsToken = input('Input 10hs bot token');
inraToken = input('Input inara token');

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
    await ctx.send('hi');
    pass;

@bot.hybrid_command(name='link', with_app_command=True)
async def test(ctx:discord.ext.commands.Context, username: str):
    headers={'appName':'10HSBot','appVersion':version,'APIkey':inraToken,'isBeingDeveloped':True};
    params={};
    y = requests.get('https://inara.cz/inapi/v1/', headers=headers);
    print(username);
    await ctx.send('This command is not implemented yet.');
    pass;

bot.run(dsToken);