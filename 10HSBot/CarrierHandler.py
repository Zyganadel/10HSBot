import asyncio
from datetime import datetime, timezone
import time
import discord;
import discord.ext.commands;
from discord import Interaction, Member, app_commands;
from discord.ext.commands import Bot, Context;

class CarrierHandler:

    bot:Bot;

    jumpOffset=300;

    def __init__(self, bot:Bot):
        self.bot=bot;
        self.tree=bot.tree;
        self.CreateCmds(self.bot,self.tree);
        pass

    tree:app_commands.CommandTree;

    # check if a user is permitted to use an elevated command. Only 1st LT. Cmdr. and above should be using carrier system without permission.
    def RoleAuthCheck(user:Member)->bool:
        fltc_role = user.guild.get_role(1370501242597675099);
        alpha_role = user.guild.get_role(769795073030094888);
        return fltc_role in user.roles or alpha_role in user.roles;

    # Region for commands.
    def CreateCmds(self, bot, tree):
        @self.bot.command(name='timedebug')
        async def Schedule(ctx:Context):
            await ctx.send(f'<t:{int(time.time())}:F>');
            pass

        @self.tree.command(name='schedule-jump', description='possibly unstable')
        async def TreeSchedule(ctx:Interaction, destination_system:str, departure_system:str='Umbila', hours:int=0, minutes:int=0):
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
            pass

        pass

    pass
