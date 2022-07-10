import discord, asyncio
from discord.ext import commands
from functions.func import blacklist, json_read, json_dump

data = json_read(r"db\config.json")
OWNER = data["owner"]

class Random(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('[*]Random Cog Carregado')

    @commands.command(aliases=['status_change'], help="Muda o status do bot", description="titulo;Status;aliases;status, status_change;description;Muda o status do bot;exemplo;=status")
    async def status(self, ctx):
        message = await ctx.send(embed=discord.Embed(title="Status", description="**Não pertubar** - 🔴\n**Ausente** - 🟡\n**Disponivel** - 🟢\n**Invisible** - ⚫"))
        uau = ['🔴', '🟡', '🟢', '⚫']
        for b in uau:
            await message.add_reaction(b)

        reaction, user = await self.bot.wait_for("reaction_add", check = (lambda reaction, user: reaction.emoji in uau and user == ctx.author))
        if reaction.emoji == '🟢':
            await self.bot.change_presence(status=discord.Status.online)
        elif reaction.emoji == '🟡':
            await self.bot.change_presence(status=discord.Status.idle)
        elif reaction.emoji == '🔴':
            await self.bot.change_presence(status=discord.Status.dnd)
        elif reaction.emoji == '⚫':
            await self.bot.change_presence(status=discord.Status.offline)

        await message.edit(embed=discord.Embed(title="Status", description=f"{reaction.emoji} Status alterado com sucesso! {reaction.emoji}"))

        for b in uau:
            await message.remove_reaction(b, self.bot.user)


    @commands.command(help="Mostra o ping do bot", description="titulo;Ping;aliases;ping;description;Mostra o ping do bot;exemplo;=ping")
    async def ping(self, ctx):
        if ctx.author.id not in blacklist():
            await ctx.send(f'Pong! In {round(self.bot.latency * 1000)}ms')
        else:
            await ctx.send("vai tomar no seu cu")

    
    @commands.command(aliases=["cf"], help="Converte Celsius para Fahrenheit", description="titulo;Conversão;aliases;converse, cf;description;Converte Celsius para Fahrenheit;exemplo;=cf 100")
    async def converse(self, ctx, celsius):
        if ctx.author.id not in blacklist():
            await ctx.send(embed=discord.Embed(title="Conversor", description=f"Fahrenheit: {(float(celsius) * (9/5))+32}"))
        else:
            await ctx.send("vai tomar no seu cu")


    @commands.command(help="Se casa com a pessoa mencionada (requer aliança)", description="titulo;Casamento;aliases;casar;description;Se casa com a pessoa mencionada (requer aliança)\nPara conseguir a aliança, use `=loja`;exemplo;=casar <usuário (menção)>")
    async def casar(self, ctx,user:discord.User):
        if ctx.author.id not in blacklist():
            data = json_read(r"db\moneycum.json")
            if str(ctx.author.id) not in data["db"]:
                await ctx.send('Você precisa criar uma perfil, use o comando "economyinit"')
            elif str(ctx.author.id) not in data["coisasdalojinha"]["alianca"]["compradopor"]:
                await ctx.send("Você nao comprou a aliança na lojinha")
            elif str(ctx.author.id) in data["namorecos"]:
                await ctx.send("Você ja esta casado")
            else:
                embed = discord.Embed(title="Casamento", description=f"<@{ctx.author.id}> quer se casar com <@{user.id}>!\n<@{user.id}> aceita?", color=discord.Color.from_rgb(r=255, g=102, b=102))
                message = await ctx.send(embed=embed)
                for c in ["✅", "❌"]:
                    await message.add_reaction(c)

                try:
                    reaction, user = await self.bot.wait_for("reaction_add", check = lambda r, u: u == user and str(r.emoji) in "✅❌", timeout=30) # r=reaction, u=user
                except asyncio.TimeoutError:
                    await message.edit(embed=discord.Embed(title="Casamento", description="Tempo encerrado", color=discord.Color.from_rgb(r=255, g=102, b=102)))
                    return
        
                if str(reaction.emoji) == "✅":
                    data["namorecos"][str(ctx.author.id)] = str(user.id)
                    await ctx.send(embed=discord.Embed(title="Casamento", description=f"Parabéns, <@{ctx.author.id}> se casou com <@{user.id}>❤️", color=discord.Color.from_rgb(r=255, g=102, b=102)))
                    json_dump(r"db\moneycum.json", data)

                elif str(reaction.emoji) == "❌":
                    await message.edit(embed=discord.Embed(title="Casamento", description=f"<@{user.id}> não aceitou o pedido :(", color=discord.Color.from_rgb(r=255, g=102, b=102)))
        else:
            await ctx.send("vai tomar no cu")
        

def setup(bot):
    bot.add_cog(Random(bot))