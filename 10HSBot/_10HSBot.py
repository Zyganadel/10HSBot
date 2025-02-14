from datetime import datetime
from os import mkdir
import discord
from discord import Interaction, Member, app_commands, channel, user
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
roles = {'ally':758089412515987496,'recruit':401075831885004802,'guest':1339805493282996257}
welcomeChannelID = 465952730880671764;

# Define the bot token so we can access it later. inara key is pre-defined and static so we can use as is.
dsToken:str;

# If the tokens file exists and is readable, read the token from file because its annoying to keep typing it in.
try:
    authFile = open("data\\auth.txt");

    # Read data
    dsToken = authFile.readline();
    InaraHelper.inaraKey = authFile.readline();
    authFile.close();
    print("In theory, our tokens should have loaded.");
except OSError as e:
    # Ensure file and dir exist.
    mkdir("data");
    authFile = open("data\\auth.txt", "wt");

    # Get data from user.
    dsToken = input('Input 10hs bot token');
    InaraHelper.inaraKey = input('Input inara token');

    # Format and write data to file.
    data = [dsToken,'\n'+InaraHelper.inaraKey];
    authFile.writelines(data);
    authFile.close();
    pass;

# dsToken = input('Input 10hs bot token');
# InaraHelper.inaraKey = input('Input inara token');

client = discord.Client(intents=intents);
bot = discord.ext.commands.Bot(command_prefix='h!', intents=intents);

tree:app_commands.CommandTree = bot.tree;

@bot.event
async def on_ready():
    dt = datetime.utcnow();    
    print(f'Logged in as {client.user} at {dt.isoformat()[:19]}Z');
    print(f'Have {len(bot.commands)} commands.');
    await bot.tree.sync();
    pass;

@tree.command(name='test',description='test command')
async def test1(ctx:Interaction):
    await ctx.response.send_message('this probably works.');
    pass;
@bot.command(name='test',locale_str='blerg', with_app_command=True)
async def test(ctx:Context, message: str):
    print(message);
    await ctx.send('hi');
    pass;

@tree.command(name='link', description='Assigns roles based on your wing/squad according to INARA.')
async def link1(ctx:Interaction, username:str):
    user:Member = ctx.user;
    await executeLink(ctx.channel,user,username);
    await ctx.response.send_message('done.');
    pass;
@bot.command(name='link', with_app_command=True)
async def link(ctx:Context, username: str):
    # Get data
    user:Member = ctx.author;
    await executeLink(ctx.channel,user,username);
    pass;

async def executeLink(channel:channel, user:Member, name:str):
    # Get data
    try:
        roleID:int = SolveRoleIDForCMDR(name);
    
        # Assign role
        role=user.guild.get_role(roleID);
        await user.add_roles(role, reason='User initiated linking.');
        await user.edit(nick=f'CMDR {name}');
        await channel.send(f'CMDR {name}, your role was updated to {role.name}.');
        pass;
    except BaseException as e:
        await user.edit(nick=f'CMDR {name}');
        await channel.send(f'CMDR {name}, something broke. it\'s most likely that we just don\'t have a guest role and our system thinks you are supposed to be a guest.');
        pass;
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
bot.tree.sync();