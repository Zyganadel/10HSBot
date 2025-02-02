from datetime import datetime
import discord
import discord.ext.commands
import requests
import json


intents = discord.Intents.default();
intents.message_content = True;

encoder = json.JSONEncoder();

version = '4.0.4';

allies = [5823,2373];
roles = {'ally':-1,'recruit':-1,'guest':-1}

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
    header = {'appName':'EDDI','appVersion':version,'APIkey':inraToken};
    dt = datetime.utcnow();
    dtString = dt.isoformat()[:19]+'Z';
    data={'eventName':'getCommanderProfile','eventTimestamp':dtString,'eventData':{'searchName':username}};
    dataFormatted={'header':header,'events':[data]};
    jsonData = encoder.encode(o=dataFormatted);
    print(dataFormatted);
    print(data);
    print(jsonData);
    response = requests.post('https://inara.cz/inapi/v1/', data=jsonData);
    reply = response.json();
    status = reply['header']['eventStatus'];
    print(IsCommanderRegistered(reply));
    await ctx.send(reply);
    pass;

# A function to determine if a commander is in the squadron or not.
def IsCommanderRegistered(data:dict):
    cmdrData = data['events'][0]['eventData'];
    try:
        squadID = cmdrData['commanderSquadron']['squadronID'];
        if(squadID == 665): return True;
    except: pass;
    try:
        wingID = cmdrData['commanderSquadron']['wingID'];
        if (wingID == 665): return True;
    except: pass;
    return False;

bot.run(dsToken);