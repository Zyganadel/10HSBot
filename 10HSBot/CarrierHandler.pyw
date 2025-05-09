import asyncio
from datetime import datetime, timezone
import time
import discord;
import discord.ext.commands;
from discord import Interaction, app_commands;
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

    # Region for commands.
    def CreateCmds(self, bot, tree):
        @self.bot.command(name='schedule')
        async def Schedule(self, ctx:Context, system:str):
            await ctx.send(self.GetTimestampString());
            pass

        @self.tree.command(name='Schedule Jump', description='Announces a jump, and pings you when you should select the system in game.')
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
            await ctx.followup.send(f'{ctx.user.mention} Chewie get us outta here!!!');
            pass

        pass

    pass
