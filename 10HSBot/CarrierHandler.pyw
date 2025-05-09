from datetime import datetime
import time
import discord;
import discord.ext.commands;
from discord import app_commands;
from discord.ext.commands import Bot, Context;

class CarrierHandler:

    bot:Bot;

    def __init__(self, bot:Bot):
        pass

    tree:app_commands.CommandTree = bot.tree;

    # Region for commands.

    @bot.Command(name='schedule')
    async def Schedule(ctx:Context, system:str):
        dt = datetime.utcnow();
        ts=dt.timestamp()
        ctx.send(f'Scheduling not implemented. Timestamp is {ts}, which might be <t:{ts}:f>');
        pass

    pass




