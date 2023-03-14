from discord.ext import commands
import discord, requests, xmljson, json
from lxml.etree import fromstring

class Dicionario(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[*]Dictionary Cog Carregado")
    
    @commands.command(help="Retorna uma palavra aleatória do dicionário.", description="titulo;Random Word;aliases;wrandom;description;Retorna uma palavra aleatória do dicionário;exemplo;=wrandom")
    async def wrandom(self, ctx):
        while True:
            try:
                word = requests.get(f"https://api.dicionario-aberto.net/word/{requests.get('https://api.dicionario-aberto.net/random').json()['word']}/1").json()[0]['xml']

                a = json.loads(json.dumps(xmljson.parker.data(fromstring(word))))

                await ctx.send(embed=discord.Embed(title=f"{a['form']['orth']}", description=f"{a['sense']['def'].replace('_', '').replace('[', '').replace(']', '').replace(':', '')}"))
                break
            except TypeError or AttributeError:
                pass

    @commands.command(help="Retorna o significado de uma palavra escolhida.", aliases=['palavra'], description="titulo;Word;aliases;word, palavra;description;Retorna o significado de uma palavra;exemplo;=word <palavra>")
    async def word(self, ctx, word):
        _ = '\n'
        try: word = requests.get(f"https://api.dicionario-aberto.net/word/{word}/1").json()[0]['xml']
        except IndexError: await ctx.send(f"<@{ctx.author.id}> Palavra não registrada.")
        a = json.loads(json.dumps(xmljson.parker.data(fromstring(word))))
        try: await ctx.send(embed=discord.Embed(title=f"{a['form']['orth']}", description=f"{a['sense']['def'].replace('_', '').replace('[', '').replace(']', '').replace(':', '')}"))
        except TypeError: await ctx.send(embed=discord.Embed(title=f"{a['form']['orth']}", description="\n".join([f"{x} - {a['sense'][0]['def'].replace('_', '').replace('[', '').replace(']', '').replace(':', '').split(_)[x]}" for x in range(len(a['sense'][0]['def'].replace('_', '').replace('[', '').replace(']', '').replace(':', '').split('\n'))) if x > 0 and x != len(a['sense'][0]['def'].replace('_', '').replace('[', '').replace(']', '').replace(':', '').split(_))-1])))

    @commands.command(help="Mostra palavras com o mesmo prefixo", description="titulo;Prefixo;aliases;prefix;description;Mostra palavras com o mesmo prefixo.;exemplo;=prefix <palavra> [quantidade de palavras]")
    async def prefix(self, ctx, word, range=5):
        a = requests.get(f"https://api.dicionario-aberto.net/prefix/{word}").json()
        await ctx.send(embed=discord.Embed(title=word, description="\n".join([x['word'] for x in a[:range]])))

    @commands.command(help="Mostra palavras com o mesmo sufixo", description="titulo;Sufixo;aliases;sufix;description;Mostra palavras com o mesmo sufixo;exemplo;=sufix <palavra> [quantidade de palavras]")
    async def sufix(self, ctx, word, range=5):
        a = requests.get(f"https://api.dicionario-aberto.net/suffix/{word}").json()
        await ctx.send(embed=discord.Embed(title=word, description="\n".join([x['word'] for x in a[:range]])))  

    @commands.command(help="Mostra palavras parecidas com a escolhida", description="titulo;Proximidade;aliases;near;description;Mostra palavras parecidas com a escolhida;exemplo;=near <palavra> [quantidade de palavras]")
    async def near(self, ctx, word, range=5):
        a = requests.get(f"https://api.dicionario-aberto.net/near/{word}").json()
        await ctx.send(embed=discord.Embed(title=word, description="\n".join([x for x in a[:range]])))  

    
async def setup(bot):
    await bot.add_cog(Dicionario(bot))