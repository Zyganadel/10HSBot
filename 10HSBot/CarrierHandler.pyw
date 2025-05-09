from datetime import datetime
import time
import discord;
import discord.ext.commands;
from discord import Interaction, app_commands;
from discord.ext.commands import Bot, Context;

class CarrierHandler:

    bot:Bot;

    def __init__(self, bot:Bot):
        pass

    tree:app_commands.CommandTree = bot.tree;

    # Region for commands.

    @bot.Command(name='schedule')
    async def Schedule(self, ctx:Context, system:str):
        await ctx.send(self.GetTimestampString());
        pass

    @tree.command(name='scheduledebug', description='should display a timestamp in unix, and the current time.')
    async def TreeSchedule(self, ctx:Interaction):
        await ctx.response.send_message(self.GetTimestampString());
        pass

    def GetTimestampString(self) -> str:
        dt = datetime.utcnow();
        ts=dt.timestamp();
        return f'Scheduling not implemented. Timestamp is {ts}, which might be <t:{ts}:f>';

    pass




