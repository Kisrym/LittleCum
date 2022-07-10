import discord, requests
from random import randint
from discord.ext import commands
from functions.func import blacklist, json_read

data = json_read(r"db\config.json")

class Nsfw(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('[*]Nsfw Cog Carregado')


    @commands.command(name='nsfw', help="ain eu vou gozar pra krl com esse comando AIIIIIINAIIAIANMNNDASOIDI GOZEI MT IRMAO PQP Q CCOMANDO GOSTOSO, Q VONTADE DE CHUPAR UM PAU, GIGANTE E DELICIOSO AI Q DLÇ BB AI VOU PRO XVIDEOS XHAMSTER PORNHUB FODAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA SWEET LESBIANS E ETC NOSSA VOU BATER UMA GOSTOSA DD+ VIADO Q DLÇ DO KRL DJASOIJDLALDJALKDJMLAJDLKAJDLAJD AIAIAIAIAIAIIAIAAIIA", description="titulo;NSFW;aliases;nsfw;description;Manda conteúdo NSFW do conteúdo escolhido;exemplo;=nsfw <conteúdo>")
    async def nsfw(self, ctx, *, tags=None):
        if ctx.author.id not in blacklist():
            
            if not ctx.channel.is_nsfw():
                await ctx.send('vai tomar no cu fdp arrombado fdpkfosdjifjdaskljfdlka\nprecisa ser um canal nsfw')
                return
        
            if tags == None:
                await ctx.send('Coloque tags pra pesquisar e fdklçsaijdesa tipo \nExemplo: dark_skin neko')

            else:                
                r = requests.get(f'https://r34-json-api.herokuapp.com/posts?tags={tags}').json()
                
                try: await ctx.send(r[randint(0, len(r))]['file_url'])
                except IndexError: await ctx.send(f"<@{ctx.author.id}> tag não encontrada")
        else:
            await ctx.send("vai tomar no cu")
    

    
def setup(bot):
    bot.add_cog(Nsfw(bot))