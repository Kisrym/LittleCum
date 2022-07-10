from discord.ext import commands
from discord_components import DiscordComponents
from functions.func import json_read

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        DiscordComponents(bot)
        self.OWNER = json_read(r"db\config.json")["owner"]

    @commands.Cog.listener()
    async def on_ready(self):
        print("[*]Voice Cog Carregado")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        data = json_read(r"db\config.json")
        for c in data["blacklist"].values():
            if member.id == c:
                await member.move_to(None)


def setup(bot):
    bot.add_cog(Voice(bot))