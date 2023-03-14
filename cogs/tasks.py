import requests, asyncio
from discord.ext import commands, tasks
from datetime import date
from functions.func import json_read
from functions.database import exportar_database

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.annoying.start()
        self.birthday.start()
        self.export.start()
        print("[*]Tasks Cog Carregado")
    
    @tasks.loop(hours=8)
    async def birthday(self):
        data = json_read(r"db\commands.json")
        for c, v in data["aniversarios"].items():
            if f"{date.today().day}/{date.today().month}" == v:
                await self.bot.get_channel(838429983865045002).send(f"Feliz aniversário <@{c}>!")

    @tasks.loop(minutes = 1)
    async def annoying(self):
        if json_read(r"db\config.json")["annoying"]["condition"] == "True":
            await asyncio.sleep(2)
            channel = self.bot.get_channel(838429983865045002)
            await channel.send("<@" + json_read(r'db\config.json')['annoying']['user'] + ">")
            await channel.purge(limit=1)

    @tasks.loop(minutes=10)
    async def export(self):
        await asyncio.sleep(5)
        exportar_database()

async def setup(bot):
    await bot.add_cog(Tasks(bot))