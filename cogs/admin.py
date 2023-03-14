from discord.ext import commands
import discord
from functions.func import json_read, json_dump
from functions.buttons import OwnerButtons, MensagemButtons, AnnoyingButtons

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(help="Adiciona ou remove donos do bot.", description="titulo;Owner;aliases;owner;description;Gerencia os donos do bot;exemplo;=owner")
    async def owner(self, ctx):
        data = json_read(r'db\config.json')
        if ctx.author.id in data['owner']:
            view = OwnerButtons()
            await ctx.send(embed=discord.Embed(title="Admin", description="\n".join([f"<@{data['owner'][data['owner'].index(x)]}> ----> {x}" for x in json_read(r"db\config.json")['owner']])), view=view)

    @commands.command(help="Adiciona aniversários no bot.", description="titulo;Aniversário;aliases;niver;description;Adiciona aniversários no bot.;exemplo;=niver <id_do_usuário> <data_de_aniversário>")
    async def niver(self, ctx, id:str, date:str):
        if ctx.author.id in json_read(r'db\config.json')['owner']:
            data = json_read(r'db\commands.json')
            try:
                data['aniversarios'][id] = date
                if len(date) != 5: raise IndexError
                elif "/" not in date: raise TypeError
                json_dump(r'db\commands.json', data)
                await ctx.message.add_reaction('✅')
            except (IndexError, TypeError): await ctx.send("Input inválido")

    @commands.command(help="Adiciona mensagens no bot.", description="titulo;Mensagem;aliases;mensagem;description;Gerencia as mensagens que o bot responderá;exemplo;=mensagem <mensagem> <reação_da_mensagem>")
    async def mensagem(self, ctx, name=None, content=None):
        if ctx.author.id in json_read(r'db\config.json')['owner']:
            data = json_read(r'db\commands.json')
            config = json_read(r'db\config.json')
            config['situation'] = "False"
            json_dump(r'db\config.json', config)
            
            view = MensagemButtons()
            der = '\n'.join([x for x in json_read(r'db\commands.json')['messages'].keys()])

            await ctx.send(embed=discord.Embed(title="Mensagens", description=f"{der}"), view = view)

    @commands.command(help="Configura a task 'annoying'", aliases = ['gui'], description="titulo;Annoying;aliases;gui, annoying;description;Configura a task;exemplo;=gui")
    async def annoying(self, ctx):
        if ctx.author.id in json_read(r'db\config.json')['owner']:
            data = json_read(r'db\config.json')
            view = AnnoyingButtons()

            embed = discord.Embed(title="Annoying", description="Informações:")
            embed.add_field(name= "Usuário:", value = data['annoying']['user'], inline = False)
            embed.add_field(name = "Ligado", value = data['annoying']['condition'], inline = False)
            await ctx.send(embed = embed, view = view)

async def setup(bot):
    await bot.add_cog(Admin(bot))
