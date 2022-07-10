from discord.ext import commands
import discord
from discord_components import Button, DiscordComponents
from functions.func import blacklist, json_read, json_dump

data = json_read(r"db\config.json")
OWNER = data["owner"]

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        DiscordComponents(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        print("[*]Commands Cog Carregado")

    @commands.command(help="Acessa a blacklist", description="titulo;Blacklist;aliases;blacklist;description;Gerencia a Blacklist;exemplo;=blacklist")
    async def blacklist(self, ctx):
        json_read(r"db\config.json")
        embed = discord.Embed(title="Blacklist")
        for k, v in data['blacklist'].items():
            embed.add_field(name=k, value=v, inline=False)
        message = await ctx.send(embed=embed, components=[
            [Button(label="Adicionar", style=3), Button(label="Remover", style=4)]
        ])
        interaction = await self.bot.wait_for('button_click', check=lambda i: i.author.id in data['owner'])
        if interaction.component.label == "Adicionar":
            await message.edit(embed=discord.Embed(title="Adicionar", description="Marque quem queres colocar"), components="")
            person = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.message.channel and len(m.mentions) > 0)
            await message.edit(embed=discord.Embed(title="Sucesso", description=f"Usuário <@{person.mentions[0].id}> adicionado com sucesso"))
            data['blacklist'][person.mentions[0].name] = person.mentions[0].id
        elif interaction.component.label == "Remover":
            await message.edit(embed=discord.Embed(title="Remover", description="Marque quem queres remover"), components="")
            person = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.message.channel and len(m.mentions) > 0)
            await message.edit(embed=discord.Embed(title="Sucesso", description=f"Usuário <@{person.mentions[0].id}> removido com sucesso"))
            del data['blacklist'][person.mentions[0].name]
        json_dump(r"db\config.json", data)

    @commands.command(help="Limpa as mensagens em um limite específico.", description="titulo;Clear;aliases;clear;description;Limpa as mensagens em um limite específico.;exemplo;=clear 10")
    async def clear(self, ctx, range):
        if ctx.author.id not in blacklist():
            if int(range) <= 100:
                await ctx.channel.purge(limit=int(range)+1)
                #// await ctx.send(f"{range} mensagens excluídas por <@{ctx.author.id}>")
                await ctx.send(f"🧼 **|** {range} mensagens excluída(s) por <@{ctx.author.id}>")
            else:
                await ctx.send("Range inválido, apenas valores abaixo de 100")
        else:
            await ctx.send("vai tomar no seu cu")

    @commands.command(help="Decide se o bot reagirá às mensagens.", description="titulo;Set Messages;aliases;set_messages;description;Decide se o bot reagirá às mensagens.;exemplo;=set_messages <True/False>")
    async def set_messages(self, ctx, situation):
        data = json_read(r"db\config.json")
        if situation == "True" or situation == "False":
            if ctx.author.id not in blacklist():
                if ctx.author.id in OWNER:
                    data["situation"] = situation
                    await ctx.send(embed=discord.Embed(title="Mensagens", description=f"{data['situation']}", color=discord.Color.from_rgb(r=255, g=0, b=127)))
                else:
                    await ctx.send("Você não tem permissão.")
            else:
                await ctx.send("vai tomar no seu cu")
        else:
            await ctx.send('Use somente "True" or "False".')
        json_dump(r"db\config.json", data)

    @commands.command(help="Codifica/decodifica códigos morse.", description="titulo;Morse Code;aliases;morsecode;description;Codifica/decodifica códigos morse.;exemplo;=morsecode <code/decode> <text>")
    async def morsecode(self, ctx, code, *text):
        if ctx.author.id not in blacklist():
            text = " ".join(text)
            morse_code = {"a" : ".-","b":"-...","c":"-.-.","d":"-..","e":".","f":"..-.","g":"--.","h":"....","i":"..","j":".---","k":"-.-","l":".-..","m":"--","n":"-.","o":"---","p":".--.","q":"--.-","r":".-.","s":"...","t":"-","u":"..-","v":"...-","w":".--","x":"-..-","y":"-.--","z":"--.."," ": "/"}
            letters = []
            if code == "code":
                for letter in text.lower():
                    for key, value in morse_code.items():
                        if letter == key:
                            letters.append(value)            
                await ctx.send(f'```{" ".join(letters)}```')
            elif code == "decode":
                text = text.split()
                for letter in text:
                    for key, value in morse_code.items():
                        if letter == value:
                            letters.append(key) 
                if len(letters) > 0:
                    await ctx.send(f'```{"".join(letters)}```')
                else:
                    await ctx.send("```Use **code** em vez de **decode**```")
            else:
                await ctx.send("```Informe se você quer codificar ou decodificar```")
        else:
            await ctx.send("vai tomar no cu")

    @commands.command(help="Mostra o avatar do usuário.", description="titulo;Avatar;aliases;avatar;description;Mostra o avatar do usuário;exemplo;=avatar <usuário (menção)>")
    async def avatar(self, ctx, user:discord.User):
        if ctx.author.id not in blacklist():
            embed = discord.Embed(title="Clique aqui para baixar a imagem", url=user.avatar_url)
            embed.set_image(url=user.avatar_url)
            await ctx.send(embed=embed)
        else: await ctx.send("vai tomar no cu")

    @commands.command(aliases=['escolha'], help="Escolhe um elemento dos que foi dado.", description="titulo;Choose;aliases;choose, escolha;description;Escolhe um dos elementos dado;exemplo;=choose <elementos separados por vírgula>")
    async def choose(self, ctx, *, items):
        from random import choice
        await ctx.send(choice(items.replace(",", "").split()))

    @commands.command(aliaes=['adicionar_emoji'], help="Adiciona um emoji por um link", description="titulo;add_emoji;aliases;add_emoji, adicionar_emoji;description;Adicionar emojis utilizando um link discord;exemplo;=add_emoji <link> <nome>")
    async def add_emoji(self, ctx, link, *, name):
        if ctx.author.server_permission.manage_emoji:
            from PIL import Image
            from io import BytesIO
            import requests

            img = Image.open(BytesIO(requests.get(link).content), mode='r')
            b = BytesIO()

            img.save(b, format="PNG")
            try:
                emoji = await ctx.guild.create_custom_emoji(name=name, image=b.getvalue())
            except discord.errors.HTTPException:
                await ctx.send("Imagem muito grande!")
            else:
                await ctx.send(f"Emoji criado com sucesso: <:{name}:{emoji.id}>")
        else:
            await ctx.send("Você não tem permissão para adicionar emojis")

    @commands.command(alias=['tr', 'tradu'], help="Traduz um texto para a linguagem escolhida", description="titulo;Tradução;aliases;tr, tradu;description;Traduz um texto para a linguagem escolhida.;exemplo;=translate <língua> <texto>")
    async def translate(self, ctx, language, *, text):
        from googletrans import Translator
        try:
            await ctx.send(f"📄 **|** <@{ctx.author.id}> {Translator().translate(text, dest=language).text}")
        except ValueError:
            await ctx.send(f"<@{ctx.author.id}> Língua inválida.")

def setup(bot):
    bot.add_cog(Commands(bot))