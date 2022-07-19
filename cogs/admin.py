from discord.ext import commands
import discord
from discord_components import DiscordComponents, Button
from functions.func import json_read, json_dump

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        DiscordComponents(bot)
    

    @commands.command(help="Adiciona ou remove donos do bot.", description="titulo;Owner;aliases;owner;description;Gerencia os donos do bot;exemplo;=owner")
    async def owner(self, ctx):
        data = json_read(r'db\config.json')
        if ctx.author.id in data['owner']:
            message = await ctx.send(embed=discord.Embed(title="Admin", description="\n".join([f"<@{data['owner'][data['owner'].index(x)]}> ----> {x}" for x in json_read(r"db\config.json")['owner']])), components=[
                [Button(label="Adicionar", style=3), Button(label="Remover", style=4)]
            ])
            res = await self.bot.wait_for('button_click', check=lambda i: i.author.id in data['owner'])
            if res.component.label == "Adicionar":
                await message.edit(embed=discord.Embed(title="Adicionar", description="Marque quem queres colocar"), components="")

                person = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.message.channel and len(m.mentions) > 0)
                await message.edit(embed=discord.Embed(title="Sucesso", description=f"Usuário <@{person.mentions[0].id}> adicionado com sucesso"))

                if person.mentions[0].id not in data['owner']: data['owner'].append(person.mentions[0].id)
            elif res.component.label == "Remover":
                des = "\n".join([f"<@{data['owner'][data['owner'].index(x)]}> ----> {x}" for x in json_read(r"db\config.json")['owner']])
                await message.edit(embed=discord.Embed(title="Admin", description=f'{des}\nEscreva o id de quem você quer remover: '), components="")

                person = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.message.channel)
                try:
                    if int(person.content) == 235076578223063041: raise ValueError 
                    await message.edit(embed=discord.Embed(title="Sucesso", description=f"Usuário <@{person.content}> removido com sucesso"))
                    data['owner'].remove(int(person.content))
                except ValueError: await message.edit(embed=discord.Embed(title="Usuário inválido.", description=""))


            json_dump(r'db\config.json', data)

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
            placeholder = config['situation']
            config['situation'] = "False"
            json_dump(r'db\config.json', config)
            
            der = '\n'.join([x for x in json_read(r'db\commands.json')['messages'].keys()]) #? f"{der}\n**Escolha uma das mensagens pra editar:**"
            message = await ctx.send(embed=discord.Embed(title="Mensagens", description=f"{der}"), components=[
                [Button(label="Adicionar", style=3), Button(label="Remover", style=4), Button(label="Lista", style=1)]
            ])

            res = await self.bot.wait_for('button_click', check=lambda i: i.author.id in config['owner'])

            backslash = '\\'
            if res.component.label == "Adicionar":
                
                await message.edit(embed=discord.Embed(title="Mensagens", description="Escreva o nome e a mensagem."), components="")
                a = await self.bot.wait_for('message', check=lambda i: i.author.id in config['owner'] and i.author.id == ctx.author.id and i.channel == ctx.message.channel)
                name, *content = a.content.split()
                content = " ".join(content)

                if name in data['messages'].keys():
                    data['messages'][name].append(content)
                else:
                    data['messages'][name] = []
                    data['messages'][name].append(content)
                await message.edit(embed=discord.Embed(title="Mensagens", description="Mensagem adicionada com sucesso."), components="")

            elif res.component.label == 'Remover':
                await message.edit(embed=discord.Embed(title="Mensagens", description=f"{der}\n**Escolha uma das mensagens pra remover seu conteúdo:**"), components="")
                a = await self.bot.wait_for('message', check=lambda i: i.author.id in config['owner'] and i.author.id == ctx.author.id and i.channel == ctx.message.channel)

                if a.content not in [x for x in json_read(r'db\commands.json')['messages'].keys()]:
                    await message.edit(embed=discord.Embed(title="Mensagens", description="Mensagem inexistente."))
                else:
                    await message.edit(embed=discord.Embed(title="Mensagens", description="\n".join([f"**{x+1}:** {json_read(f'db{backslash}commands.json')['messages'][a.content.strip()][x]}" for x in range(len(json_read('db\commands.json')['messages'][a.content.strip()]))])))
                    i = await self.bot.wait_for('message', check=lambda i: i.author.id in config['owner'] and i.author.id == ctx.author.id and i.channel == ctx.message.channel)
                    try:
                        data['messages'][a.content.strip()].pop(int(i.content) - 1)
                    except ValueError: await message.edit(embed=discord.Embed(title="Mensagens", description="Use números como index"))     
                    except IndexError: await message.edit(embed=discord.Embed(title="Mensagens", description="Index inválido."))
                    else: await message.edit(embed=discord.Embed(title="Mensagens", description="Mensagem excluída com sucesso."))
                    
                    if len(data['messages'][a.content]) == 0:
                        del data['messages'][a.content]

            elif res.component.label == "Lista":
                await message.edit(embed=discord.Embed(title="Mensagens", description=f"{der}\n**Escolha uma das mensagens para ver seu conteúdo:**"), components="")
                a = await self.bot.wait_for('message', check=lambda i: i.author.id in config['owner'] and i.author.id == ctx.author.id and i.channel == ctx.message.channel)
                await message.edit(embed=discord.Embed(title="Mensagens", description="\n".join([f"**{x+1}:** {json_read(f'db{backslash}commands.json')['messages'][a.content.strip()][x]}" for x in range(len(json_read('db\commands.json')['messages'][a.content.strip()]))])))

            config['situation'] = placeholder
            json_dump(r'db\commands.json', data)
            json_dump(r'db\config.json', config)

    @commands.command(help="Configura a task 'annoying'", aliases = ['gui'], description="titulo;Annoying;aliases;gui, annoying;description;Configura a task;exemplo;=gui")
    async def annoying(self, ctx):
        if ctx.author.id in json_read(r'db\config.json')['owner']:
            data = json_read(r'db\config.json')

            embed = discord.Embed(title="Annoying", description="Informações:")
            embed.add_field(name= "Usuário:", value = data['annoying']['user'], inline = False)
            embed.add_field(name = "Ligado", value = data['annoying']['condition'], inline = False)
            mensagem = await ctx.send(embed = embed, components = [Button(label = "Adicionar usuário", style = 3), Button(label = data['annoying']['condition'], style = 4, custom_id = "Ligado")])

            res = await self.bot.wait_for('button_click', check=lambda i: i.author.id == ctx.author.id and i.channel == ctx.message.channel)

            if res.component.label == "Adicionar usuário":
                await mensagem.edit(embed = discord.Embed(title = "Annoying", description = "Marque o usuário: "), components = "")
                person = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.message.channel and len(m.mentions) > 0)

                data['annoying']['user'] = str(person.mentions[0].id)
                await mensagem.edit(embed = discord.Embed(title = "Annoying", description = "Usuário adicionado com sucesso."), components = "")

            elif res.component.custom_id == "Ligado":
                data['annoying']['condition'] = "True" if data['annoying']['condition'] == "False" else "False"
                    
                await mensagem.edit(embed = discord.Embed(title = "Annoying", description = "Situação atualizada."), components = "")

            json_dump(r'db\config.json', data)

def setup(bot):
    bot.add_cog(Admin(bot))
