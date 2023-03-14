import discord
from discord.ext import commands
import requests
from random import randint

class Nsfw(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    @commands.command(help = "Manda imagens NSFW da tag específica", description = "titulo;NSFW;aliases;nsfw;description;Manda uma imagem NSFW;exemplo;=nsfw neko")
    async def nsfw(self, ctx, tag: str):
        r = requests.get(f"https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags={tag}&json=1").json()
        await ctx.send(r[randint(0, len(r))]['file_url'])
        
async def setup(bot:commands.Bot):
    await bot.add_cog(Nsfw(bot))