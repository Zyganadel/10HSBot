from datetime import datetime
import discord
import discord.ext.commands
from discord.ext.commands import Context
from discord.abc import Snowflake
import requests
import json

from InaraHelper import InaraHelper
from InaraHelper import InaraData

intents = discord.Intents.default();
intents.members=True;
intents.message_content = True;

encoder = json.JSONEncoder();

version = '4.0.4';

allies = [5823,2373];
roles = {'ally':758089412515987496,'recruit':401075831885004802,'guest':0}

dsToken = input('Input 10hs bot token');
InaraHelper.inaraKey = input('Input inara token');

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
async def test(ctx:Context, message: str):
    print(message);
    await ctx.send('hi');
    pass;

@bot.hybrid_command(name='link', with_app_command=True)
async def test(ctx:Context, username: str):
    # header = {'appName':'EDDI','appVersion':version,'APIkey':inraToken};
    # dt = datetime.utcnow();
    # dtString = dt.isoformat()[:19]+'Z';
    # data={'eventName':'getCommanderProfile','eventTimestamp':dtString,'eventData':{'searchName':username}};
    # dataFormatted={'header':header,'events':[data]};
    # jsonData = encoder.encode(o=dataFormatted);
    # print(dataFormatted);
    # print(data);
    # print(jsonData);
    # response = requests.post('https://inara.cz/inapi/v1/', data=jsonData);
    # reply = response.json();
    # status = reply['header']['eventStatus'];
    # print(IsCommanderRegistered(reply));
    # await ctx.send(reply);

    # Get data
    roleID:int = SolveRoleIDForCMDR(username);
    user:discord.Member = ctx.author;
    
    # Assign role
    role=ctx.guild.get_role(roleID);
    await user.add_roles(role, reason='User initiated linking.');
    await user.edit(nick=f'CMDR {username}');
    await ctx.send(f'CMDR {username}, your role was updated to {role.name}.');
    pass;

@bot.event
async def on_member_join(member: discord.Member):
    # Get data
    roleID:int = SolveRoleIDForCMDR(member.display_name);
    
    # Assign role
    role=member.guild.get_role(roleID);
    await member.add_roles(role, reason='Automated linking.');
    await member.edit(nick=f'CMDR {member.display_name}');
    pass;

def SolveRoleIDForCMDR(name:str):
    data = InaraHelper.GetCMDRData(name);
    roleID:int;
    # if data invalid, make them a guest.
    if(not data.isValid): roleID = roles['guest'];
    # else read their squadron data if any, and assign roles based on it.
    else:
        affiliation:int=-1;
        if(data.wingId != -1): affiliation = data.wingId;
        if(data.squadronId != -1): affiliation = data.squadronId;

        if(affiliation == -1 or affiliation == 665): roleID = roles['recruit'];
        elif(affiliation in allies): roleID = roles['ally'];
        else: roleID = roles['guest'];
    return roleID;

bot.run(dsToken);