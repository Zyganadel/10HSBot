import asyncio
from datetime import datetime, timezone
import os
import time
import discord;
import discord.ext.commands;
import CarrierHandler;
from discord import Guild, Interaction, Member, TextChannel, app_commands;
from discord.ext.commands import Bot, Context;

indexFileName:str='data\\userIndex.txt';

class ActivityManager(object):

    bot:Bot;
    tree:app_commands.CommandTree;
    guild:Guild;

    def __init__(self, bot:Bot):
        self.bot=bot;
        self.tree=bot.tree;
        self.CreateCmds(self.bot,self.tree);
        pass;

    def PostInit(self):
        self.guild=self.bot.get_guild(200305786637778945);
        return;

    # Check if a user is permitted to use an elevated command. Only Ship Commander and above should be able to access these commands.
    def RoleAuthCheck(self, user:Member)->bool:
        state = False;
        sc_role = user.guild.get_role(1340439327364087930);
        officer_role = user.guild.get_role(401077126138167296);
        fltc_role = user.guild.get_role(1370501242597675099);
        alpha_role = user.guild.get_role(769795073030094888);

        permitted = [sc_role,officer_role,fltc_role,alpha_role];

        for x in user.roles:
            if x in permitted: state = True;
            pass;
        return state;

    def CreateCommands(self,bot,tree):

        # when someone joins, create a file for them to track whether or not they've opted in.
        @self.bot.event
        async def on_member_join(member: Member):
            file = open(f'data\\{member.id}.mdat', 'wt');

            # fill the file with default values.
            file.write('True\n0\n0');
            pass;

        # when someone leaves, delete the file used to store their data.
        @self.bot.event
        async def on_member_leave(member: Member):
            os.remove(f'data\\{member.id}.mdat');
            pass;

        @self.tree.command(name='opt-in-or-out', description='opts in or out of the activity tracker, and clears any status.')
        async def OptInOut(ctx:Interaction, state:bool):
            save(Pilot(ctx.user,state,0,0));
            pass;

        pass;

    pass;

class Pilot:
    userID:int;
    optStatus:bool=True;

    vcTime:int=0;
    eliteTime:int=0;

    def __init__(self,userID,status,vct,et):
        self.userID=userID;
        self.optStatus=status;
        self.vcTime=vct;
        self.eliteTime.et;
        pass;

    pass;

def load(member:Member)->Pilot:
    file = open(f'data\\{member.id}.mdat', 'rt');
    status=bool(CarrierHandler.trimstring(file.readline()));
    vct=int(CarrierHandler.trimstring(file.readline()));
    et=int(CarrierHandler.trimstring(file.readline()));

    value = Pilot(member.id,status,vct,et);
    pass;

def save(pilot:Pilot):
    file = open(f'data\\{pilot.userID}.mdat', 'wt');
    lines = [''];
    lines.append(f'{pilot.optStatus}\n');
    lines.append(f'{pilot.vcTime}\n');
    lines.append(f'{pilot.eliteTime}\n');
    pass;