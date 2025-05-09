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

        @self.tree.command(name='scheduledebug', description='do not use yet')
        async def TreeSchedule(ctx:Interaction, Destination_System:str, Departure_System:str='Umbila', hours:int=0, minutes:int=0):
            departureOffset = minutes*60+hours*3600;
            response = f'''
            Carrier {ctx.channel.name} is scheduling a jump.

            Trip Details:
            - Departure System: `{Departure_System}`
            - Destination System: `{Destination_System}`
            - Departure Time: <t:{int(time.time())+departureOffset}:F>
            '''
            await ctx.response.send_message(response);
            await asyncio.sleep(departureOffset);
            await ctx.followup.send(f'{ctx.user.mention} Chewie get us outta here!!!');
            pass

        pass

    pass
