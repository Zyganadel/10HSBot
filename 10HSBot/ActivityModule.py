import asyncio
from datetime import datetime, timezone
import time
from unittest.mock import Base
import discord;
import discord.ext.commands;
from discord import Guild, Interaction, Member, TextChannel, app_commands;
from discord.ext.commands import Bot, Context;

indexFileName:str='data\\userIndex.txt';

class my_class(object):

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

    pass




