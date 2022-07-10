from discord.ext import commands
import json
from random import choice, randint
from functions.func import blacklist, json_dump, json_read

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[*]Events Cog Carregado")

    #commands.Cog.listener() == bot.event
    @commands.Cog.listener()
    async def on_message(self, message):
        with open(r"db\commands.json", "r") as arquivo:
            data = json.load(arquivo)
            messages = data["messages"]
        if json_read(r"db\config.json")['situation'] == "True":
            if message.author == self.bot.user: #Aqui anula se a mensagem for a mensagem do próprio bot, para evitar loop infinito
                return
            if message.author.id not in blacklist():
                for keys, values in messages.items():
                    if type(values) == list:
                        if keys in message.content[:len(keys)]:
                            await message.channel.send(choice(values))
        if message.author.id in blacklist(): await message.delete()

        eita = randint(0, 10)
        if message.author.id == 360212994619211789:
            data["c"] += 1
        if data["c"] == 10: 
            if eita == 10:
                await message.channel.send("https://cdn.discordapp.com/attachments/838429983865045002/897596411170918440/Pastel_feiraaoo.png")
            data["c"] = 0

        json_dump(r"db\commands.json", data)

def setup(bot):
    bot.add_cog(Events(bot))