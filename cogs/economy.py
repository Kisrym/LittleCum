import discord
from discord.ext import commands
import time
from random import randint
from functions.func import json_read, json_dump, blacklist

class Economy(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print("[*]Economy Cog Carregado")

    @commands.command(help='"Inicia sua "conta bancaria"', description="titulo;Iniciar economia;aliases;economyinit;description;Inicia sua conta bancária;exemplo;=economyinit")
    async def economyinit(self, ctx):
        data = json_read(r"db\moneycum.json")
        if ctx.author.id not in blacklist():
            if str(ctx.author.id) not in data["db"]:
                await ctx.send('Criando Perfil...')
                data["db"][str(ctx.author.id)] = {}
                data["db"][str(ctx.author.id)]["dinheiro"] = 1000
                data["db"][str(ctx.author.id)]["time"] = 0
                json_dump(r"db\moneycum.json", data)
                await ctx.send('Perfil Criado')
            else:
                await ctx.send("Você ja tem um perfil")
        else:
            await ctx.send("vai tomar no cu")

    @commands.command(help='"Trabalha" para poder conseguir dinheiro.', description="titulo;Trabalho;aliases;work;description;Trabalha para conseguir dinheiro;exemplo;=work")
    async def work(self, ctx):
        if ctx.author.id not in blacklist():
            data = json_read(r"db\moneycum.json")
            if str(ctx.author.id) not in data["db"]:
                await ctx.send('Você precisa criar uma perfil, use o comando "economyinit"')
            elif data["db"][str(ctx.author.id)]["time"] >= int(f'{time.localtime().tm_year}{time.localtime().tm_mon}{time.localtime().tm_mday}'):
                await ctx.send("Você não pode resgatar mais dinheiro hoje.")
            else:                                           # arruma o bot shirao
                dinheirohoje = randint(400, 1100)
                data["db"][str(ctx.author.id)]["dinheiro"] += dinheirohoje
                data["db"][str(ctx.author.id)]["time"] = int(f'{time.localtime().tm_year}{time.localtime().tm_mon}{time.localtime().tm_mday}')
                json_dump(r"db\moneycum.json", data)
                embed = discord.Embed(title="Dinheiro resgatado",description=f"Valor que você pegou hoje: {dinheirohoje}")
                await ctx.send(embed=embed)
        else:
            await ctx.send("vai tomar no cu")

    @commands.command(help="Mostra quanto dinheiro você possui.", description="titulo;Banco;aliases;bank;description;Mostra o quanto dinheiro você tem;exemplo;=bank")
    async def bank(self, ctx):
        if ctx.author.id not in blacklist():
            data = json_read(r"db\moneycum.json")
            if str(ctx.author.id) not in data["db"]:
                await ctx.send('Você precisa criar uma perfil, use o comando "economyinit"')
            else:
                maney = data["db"][str(ctx.author.id)]["dinheiro"]
                await ctx.send(f'Seu dinheiro: {maney}')
        else:
            await ctx.send("vai tomar no cu")
    
    @commands.command(help="Abre a loja", description="titulo;Loja;aliases;loja;description;Abre a loja;exemplo;=loja [item que você quer comprar]")
    async def loja(self, ctx, comprakkk=None):
        if ctx.author.id not in blacklist():
            data = json_read(r"db\moneycum.json")
            coisinhas = data["coisasdalojinha"]

            if comprakkk == None:
                embed=discord.Embed(title="Lojinha", colour=378912)
                for keys, values in coisinhas.items():
                    embed.add_field(name=keys, value=f'{values["description"]}\nPreço: {values["preco"]}', inline=False)
                await ctx.send(embed=embed)
                
            elif comprakkk not in coisinhas.keys():
                await ctx.send('tu é broxa')
                return
            else:
                if str(ctx.author.id) not in data["coisasdalojinha"][str(comprakkk)]["compradopor"]:
                    if data["db"][str(ctx.author.id)]["dinheiro"] >= coisinhas[str(comprakkk).lower()]["preco"]:
                        data["db"][str(ctx.author.id)]["dinheiro"] -= coisinhas[str(comprakkk)]["preco"]
                        data["coisasdalojinha"][str(comprakkk)]["compradopor"].append(str(ctx.author.id))
                        await ctx.send('Comprado')
                        json_dump(r"db\moneycum.json", data)
                    else:
                        await ctx.send('pobrekkkk')
                else:
                    await ctx.send('Você ja comprou isso')
        else:
            await ctx.send("vai tomar no cu")
        
    
    @commands.command(help="Rouba alguma pessoa mencionada.", description="titulo;Roubo;aliases;roubar;description;Rouba a pessoa mecionada;exemplo;=roubar <usuário (menção)>")
    async def roubar(self, ctx, user:discord.User=None):
        if ctx.author.id not in blacklist():
            if user == None:
                await ctx.send('você precisa mencionar alguem para roubar:smirk:')
            else:
                data = json_read(r"db\moneycum.json")
                coisinhas = data["coisasdalojinha"]
                if str(ctx.author.id) not in coisinhas["arma"]["compradopor"]:
                    await ctx.send('você precisa comprar uma arma para assaltar jogadores burroburroburro')
                else:
                    if str(user.id) not in data["db"]:
                        await ctx.send('Usuario mencionado nao tem perfil criado no bot')
                    else:
                        ab = randint(200,700)

                        if data["db"][str(user.id)]["dinheiro"] <= 200:
                            await ctx.send('esse jogador é muito pobre, nem roubar vai dar')
                        elif data["db"][str(user.id)]["dinheiro"] <= ab:
                            eita = randint(1,10)
                            if eita == 5:
                                await ctx.send('Você tentou roubar mas é burro e nao conseguiu')
                            else:
                                yeb = data["db"][str(user.id)]["dinheiro"] 
                                data["db"][str(ctx.author.id)]["dinheiro"] += yeb
                                data["db"][str(user.id)]["dinheiro"] -= yeb
                                await ctx.send('Dinheiro roubado: {}, esse ai entrou na falencia, tirou ate o ultimo centavo'.format(yeb))
                        else:
                            eita = randint(1,5)
                            if eita == 5:
                                await ctx.send('Você tentou roubar mas é burro e nao conseguiu')
                            else:
                                ab = randint(200,700)
                                data["db"][str(user.id)]["dinheiro"] -= ab
                                data["db"][str(ctx.author.id)]["dinheiro"] += ab
                                await ctx.send('Dinheiro roubado: {}'.format(ab))
                            
            json_dump(r"db\moneycum.json", data)
        else:
            await ctx.send('vai tomar no cu')

def setup(bot:commands.Bot):
    bot.add_cog(Economy(bot))