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
        self.guizinho.start()
        self.birthday.start()
        self.dump.start()
        print("[*]Tasks Cog Carregado")
    
    @tasks.loop(hours=8)
    async def birthday(self):
        data = json_read(r"db\commands.json")
        for c, v in data["aniversarios"].items():
            if f"{date.today().day}/{date.today().month}" == v:
                await self.bot.get_channel(838429983865045002).send(f"Feliz aniversário <@{c}>!")

    @tasks.loop(minutes=10) #? minutes=10
    async def guizinho(self):
        if json_read(r"db\config.json")["guizinho"] == "True":
            await asyncio.sleep(2)
            channel = self.bot.get_channel(838429983865045002)
            await channel.send("<@305852325346541568>")
            await channel.purge(limit=1)

    @tasks.loop(minutes=10)
    async def export(self): #! IMPORT AS INFORMAÇÕES DA DATABASE
        await asyncio.sleep(5)
        exportar_database()

def setup(bot):
    bot.add_cog(Tasks(bot)) 