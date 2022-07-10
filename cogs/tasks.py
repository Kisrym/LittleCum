import requests, asyncio
from discord.ext import commands, tasks
from datetime import date
from functions.func import json_read, json_dump

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
    async def dump(self): #! IMPORT AS INFORMAÇÕES DA DATABASE
        await asyncio.sleep(5)
        r = requests.get("https://littlecum-39790-default-rtdb.firebaseio.com/.json").json()
        config = json_read(r"db\config.json")
        commands = json_read(r"db\commands.json")

        r['config'] = config
        r['commands'] = commands

        r = str(r).replace("\'", "\"")

        requests.patch(r"https://littlecum-39790-default-rtdb.firebaseio.com/.json", data=f'{r}')

    @tasks.loop(minutes=10)
    async def read(self): #! LÊ OS ITENS DA DATABASE
        r = requests.get("https://littlecum-39790-default-rtdb.firebaseio.com/.json").json()
        json_dump(r"db\config.json", r['config'])
        json_dump(r"db\commands.json", r['commands'])

def setup(bot):
    bot.add_cog(Tasks(bot)) 