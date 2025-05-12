import asyncio
from datetime import datetime, timezone
import time
from unittest.mock import Base
import discord;
import discord.ext.commands;
from discord import Guild, Interaction, Member, TextChannel, app_commands;
from discord.ext.commands import Bot, Context;

indexFileName:str='data\\carrierIndex.txt';

class CarrierHandler:

    bot:Bot;
    tree:app_commands.CommandTree;

    jumpOffset=1200;

    carriers=[];

    def __init__(self, bot:Bot):
        self.bot=bot;
        self.tree=bot.tree;
        self.CreateCmds(self.bot,self.tree);
        pass;

    def PostInit(self):
        guild=self.bot.get_guild(200305786637778945);
        self.carriers = load(guild,indexFileName);
        pass;


    # check if a user is permitted to use an elevated command. Only 1st LT. Cmdr. and above should be using carrier system without permission.
    def RoleAuthCheck(self, user:Member)->bool:
        fltc_role = user.guild.get_role(1370501242597675099);
        alpha_role = user.guild.get_role(769795073030094888);
        return fltc_role in user.roles or alpha_role in user.roles;

    def OwnerOrRoleAuthCheck(self, user:Member, channel:TextChannel)->int:
        # return all clear if user is an admin.
        if(self.RoleAuthCheck(user)): return 0;

        # otherwise, check if the user is the owner of the channel.
        for carrier in self.carriers:
            # cast so we can access things easier.
            if(type(carrier)!=Carrier): continue;
            c:Carrier=carrier;

            if(c.owner==user):
                # if the channels and owners match, return all clear.
                if(c.channel==channel): return 0;
                # otherwise, return not your channel.
                else: return -1;
            pass;
        # if the user has no carrier, let them know.
        return -2;

    def GetCarrier(self, channel:TextChannel)->Carrier:
        for carrier in self.carriers:
            # cast so we can access things easier.
            if(type(carrier)!=Carrier): continue;
            c:Carrier=carrier;

            if(c.channel==channel): return c;
            continue;
        pass;

    # Region for commands.
    def CreateCmds(self, bot, tree):
        # a debug command to test things.
        @self.bot.command(name='staticdebug')
        async def Schedule(ctx:Context):
            # check that time is working.
            await ctx.send(f'<t:{int(time.time())}:F>');
            # check authorisation.
            await ctx.send(f'Auth check: {self.RoleAuthCheck(ctx.author)}');
            pass;

        @self.tree.command(name='schedule-jump', description='possibly unstable')
        async def TreeSchedule(ctx:Interaction, destination_system:str, departure_system:str='', hours:int=0, minutes:int=0):
            authResponse=self.OwnerOrRoleAuthCheck();
            if(authResponse==-1): await ctx.response.send_message(ephemeral=True, content='This is not your carrier channel.');
            elif(authResponse==-2): await ctx.response.send_message(ephemeral=True, content='This is not your channel. Maybe get one first.');

            carrier:Carrier=self.GetCarrier(ctx.channel);
            if(departure_system=='' and carrier != None): departure_system=carrier.current_system;
            carrier.target_system=destination_system;

            departureOffset = minutes*60+hours*3600;
            response = f'''
### :warning: **Attention** :warning:
Carrier {ctx.channel.name} has scheduled a jump.

### Trip Details:
- Departure System: `{departure_system}`
- Destination System: `{destination_system}`
- Scheduled Departure Time: <t:{int(time.time())+departureOffset}:F>
            '''
            await ctx.response.send_message(response);
            await asyncio.sleep(departureOffset);
            await ctx.followup.send(f'{ctx.user.mention} You should schedule the jump now.');
            pass;

        @self.tree.command(name='register-existing', description='Registers a carrier to an existing channel.')
        async def TreeRegisterExisting(ctx:Interaction, name:str, owner:str, carrierid:str, ping:bool=True):
            # check authorisation.
            if(not self.RoleAuthCheck(ctx.user)):
                await ctx.response.send_message(ephemeral=True, content='Either something went wrong or you are not authorised to use this.');
                return;
            # check if owner is a valid id.
            try:
                owner=int(owner);
            except:
                await ctx.response.send_message(ephemeral=True,content='Owner was not an int.');
                return;

            # create carrier
            self.carriers.append(Carrier(ctx.guild,ctx.channel_id,owner,name,carrierid));
            save(indexFileName, self.carriers);

            # after its saved, inform the user.
            message:str
            if(ping):message = f'Registered carrier {name} ({carrierid}) for <@{owner}> in this channel.';
            else:message = f'Registered carrier {name} ({carrierid}) for {ctx.guild.get_member(owner).nick} in this channel.';
            await ctx.response.send_message(message);

            pass;

        pass;

    pass;

class Carrier:

    channel:TextChannel
    owner:Member
    name:str
    carrierid:str

    # our home system is mitnahas, so assume a carrier with no home location is in that system.
    current_system:str = 'Mitnahas';
    # set a default value so if someone reports a jump, it wont break.
    target_system:str=''; 

    def __init__(self, guild:Guild, cid:int, oid:int, name:str, carrierid:str):
        self.channel=guild.get_channel(cid);
        self.owner=guild.get_member(oid);
        self.name=name;
        self.carrierid=carrierid;

        pass;

    pass;

def loadIndividual(guild:Guild, file:str)->Carrier:
    try:
        
        f=open(file);
        # each arg should be on a separate line.
        cid=f.readline();
        oid=f.readline();
        carrier=Carrier(guild,int(cid),int(oid),f.readline(),f.readline());
        carrier.current_system=f.readline();
        f.close();
        return carrier; 
    except BaseException as e:
        print(f'Error: {e}.');
        pass;
    pass;

def saveIndividual(file:str, carrier:Carrier):
    # ensure the file exists.
    try:
        c=carrier; # shorten it because we'll spam it.
        lines=[f'{c.channel.id}\n',f'{c.owner.id}\n',c.name+'\n',c.carrierid+'\n',c.current_system+'\n'];
        f=open(file,'wt');
        f.writelines(lines);
        f.close();
        return 0;
    except BaseException as e:
        print(f'Error: {e}.');
        return -1;
    pass;


def load(guild:Guild, file:str)->list:
    carriers=list();
    try:
        f=open(file);
        files = f.readlines();
        for x in files:
            # Remove escape char.
            x=x[:len(x)-1];
            carriers.append(loadIndividual(guild,f'data\\{x}.cdat'));
            continue;
        f.close();        
    except BaseException as e:
        print(f'Error: {e}.');
        pass;
    return carriers;

def save(file:str, carriers:list):
    lines=[];
    for x in carriers:
        # cast so we can access things easier.
        if(type(x)!=Carrier): continue;
        c:Carrier=x;
        name=c.carrierid;
        fname=f'data\\{name}.cdat';
        saveIndividual(fname,c);
        lines.append(name+'\n');
        continue;
    f=open(file,'wt');
    f.writelines(lines);
    f.close();
    pass;