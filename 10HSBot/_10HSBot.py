from datetime import datetime
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
    dt = datetime.utcnow();    
    print(f'Logged in as {client.user} at {dt.isoformat()[:19]}Z');
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
    headers={'appName':'10HSBot','appVersion':version,'APIkey':inraToken,'isBeingDeveloped':'True'};
    dt = datetime.utcnow();
    dtString = dt.isoformat()[:19]+'Z';
    params={'eventName':'getCommanderProfile','eventTimestamp':dtString,'eventData':{'searchName':username}};
    y = requests.post('https://inara.cz/inapi/v1/', headers=headers, params=params);
    await ctx.send('This command is not implemented yet.');
    print(username);
    print(y.text);
    print(y.content.decode());
    print(y.headers);
    print(y.status_code);
    pass;

bot.run(dsToken);