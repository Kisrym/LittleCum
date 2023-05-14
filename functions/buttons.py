import discord
from functions.func import json_read, json_dump
from functions.video import Video

class OwnerButtons(discord.ui.View):
    @discord.ui.button(label = "Adicionar", style = discord.ButtonStyle.success)
    async def adicionar(self, interaction: discord.Interaction, button: discord.ui.button):
        data = json_read(r'db\config.json')
        await interaction.response.edit_message(embed=discord.Embed(title="Adicionar", description="Marque quem queres colocar"))

        person = await interaction.client.wait_for('message', check=lambda m: m.author == interaction.user and m.channel == interaction.channel and len(m.mentions) > 0)
        await interaction.message.edit(embed=discord.Embed(title="Sucesso", description=f"Usuário <@{person.mentions[0].id}> adicionado com sucesso"))

        if person.mentions[0].id not in data['owner']: data['owner'].append(person.mentions[0].id)
        json_dump(r'db\config.json', data)

    @discord.ui.button(label = "Remover", style = discord.ButtonStyle.danger)
    async def remover(self, interaction: discord.Interaction, button: discord.ui.button):
        data = json_read(r'db\config.json')
        des = "\n".join([f"<@{data['owner'][data['owner'].index(x)]}> ----> {x}" for x in json_read(r"db\config.json")['owner']])

        await interaction.response.edit_message(embed=discord.Embed(title="Admin", description=f'{des}\nEscreva o id de quem você quer remover: '))
        person = await interaction.client.wait_for('message', check=lambda m: m.author == interaction.user and m.channel == interaction.channel)

        if int(person.content) == 235076578223063041:
            return
        
        if int(person.content) not in data["owner"]:
            return

        await interaction.message.edit(embed=discord.Embed(title="Sucesso", description=f"Usuário <@{person.content}> removido com sucesso"))
        data['owner'].remove(int(person.content))
        json_dump(r'db\config.json', data)

class MensagemButtons(discord.ui.View):
    @discord.ui.button(label = "Adicionar", style = discord.ButtonStyle.success)
    async def adicionar(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = json_read(r'db\commands.json')
        config = json_read(r'db\config.json')

        await interaction.response.edit_message(embed=discord.Embed(title="Mensagens", description="Escreva o nome e a mensagem."))

        a = await interaction.client.wait_for('message', check=lambda i: i.author.id in config['owner'] and i.author.id == interaction.user.id and i.channel == interaction.channel)
        name, *content = a.content.split()
        content = " ".join(content)

        if name in data['messages'].keys():
            data['messages'][name].append(content)
        else:
            data['messages'][name] = []
            data['messages'][name].append(content)

        await interaction.message.edit(embed=discord.Embed(title="Mensagens", description="Mensagem adicionada com sucesso."))

        json_dump(r'db\commands.json', data)
        json_dump(r'db\config.json', config)

        await interaction.delete_original_response()

    
    @discord.ui.button(label = "Remover", style = discord.ButtonStyle.danger)
    async def remover(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = json_read(r'db\commands.json')
        config = json_read(r'db\config.json')

        der = '\n'.join([x for x in json_read(r'db\commands.json')['messages'].keys()])
        backslash = '\\'

        await interaction.response.edit_message(embed=discord.Embed(title="Mensagens", description=f"{der}\n**Escolha uma das mensagens pra remover seu conteúdo:**"))
        a = await interaction.client.wait_for('message', check=lambda i: i.author.id in config['owner'] and i.author.id == interaction.user.id and i.channel == interaction.channel)

        if a.content not in [x for x in json_read(r'db\commands.json')['messages'].keys()]:
            await interaction.message.edit(embed=discord.Embed(title="Mensagens", description="Mensagem inexistente."))
        else:
            await interaction.message.edit(embed=discord.Embed(title="Mensagens", description="\n".join([f"**{x+1}:** {json_read(f'db{backslash}commands.json')['messages'][a.content.strip()][x]}" for x in range(len(json_read('db\commands.json')['messages'][a.content.strip()]))])))
            i = await interaction.client.wait_for('message', check=lambda i: i.author.id in config['owner'] and i.author.id == interaction.user.id and i.channel == interaction.channel)
            try:
                data['messages'][a.content.strip()].pop(int(i.content) - 1)
            except ValueError: await interaction.message.edit(embed=discord.Embed(title="Mensagens", description="Use números como index"))     
            except IndexError: await interaction.message.edit(embed=discord.Embed(title="Mensagens", description="Index inválido."))
            else: await interaction.message.edit(embed=discord.Embed(title="Mensagens", description="Mensagem excluída com sucesso."))
            
            if len(data['messages'][a.content]) == 0:
                del data['messages'][a.content]

        json_dump(r'db\commands.json', data)
        json_dump(r'db\config.json', config)

        await interaction.delete_original_response()

    @discord.ui.button(label = "Lista", style = discord.ButtonStyle.blurple)
    async def lista(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = json_read(r'db\commands.json')
        config = json_read(r'db\config.json')

        der = '\n'.join([x for x in json_read(r'db\commands.json')['messages'].keys()])
        backslash = '\\'

        await interaction.message.edit(embed=discord.Embed(title="Mensagens", description=f"{der}\n**Escolha uma das mensagens para ver seu conteúdo:**"))
        a = await interaction.client.wait_for('message', check=lambda i: i.author.id in config['owner'] and i.author.id == interaction.user.id and i.channel == interaction.channel)
        await interaction.message.edit(embed=discord.Embed(title="Mensagens", description="\n".join([f"**{x+1}:** {json_read(f'db{backslash}commands.json')['messages'][a.content.strip()][x]}" for x in range(len(json_read('db\commands.json')['messages'][a.content.strip()]))])))

        json_dump(r'db\commands.json', data)
        json_dump(r'db\config.json', config)

        await interaction.delete_original_response()

class AnnoyingButtons(discord.ui.View):
    @discord.ui.button(label = "Adicionar usuário", style=discord.ButtonStyle.success)
    async def adicionar_usuario(self, interaction: discord.Interaction, button: discord.ui.Button):
        config = json_read(r'db\config.json')

        await interaction.response.edit_message(embed = discord.Embed(title = "Annoying", description = "Marque o usuário: "))
        person = await interaction.client.wait_for('message', check=lambda m: m.author == interaction.user and m.channel == interaction.channel and len(m.mentions) > 0)

        config['annoying']['user'] = str(person.mentions[0].id)
        await interaction.message.edit(embed = discord.Embed(title = "Annoying", description = "Usuário adicionado com sucesso"))
    
        json_dump(r'db\config.json', config)

    @discord.ui.button(label = json_read(r'db\config.json')['annoying']['condition'], style=discord.ButtonStyle.danger)
    async def ligado(self, interaction: discord.Interaction, button: discord.ui.Button):
        config = json_read(r'db\config.json')
        config['annoying']['condition'] = "True" if config['annoying']['condition'] == "False" else "False"
                    
        await interaction.response.edit_message(embed = discord.Embed(title = "Annoying", description = "Situação atualizada."))
        json_dump(r'db\config.json', config)

class BlacklistButtons(discord.ui.View):
    @discord.ui.button(label = "Adicionar", style=discord.ButtonStyle.success)
    async def adicionar(self, interaction: discord.Interaction, button: discord.ui.Button):
        config = json_read(r'db\config.json')
        await interaction.response.edit_message(embed=discord.Embed(title="Adicionar", description="Marque quem queres colocar"))

        person = await interaction.client.wait_for('message', check=lambda m: m.author == interaction.user and m.channel == interaction.channel and len(m.mentions) > 0)

        await interaction.message.edit(embed=discord.Embed(title="Sucesso", description=f"Usuário <@{person.mentions[0].id}> adicionado com sucesso"))

        config['blacklist'][person.mentions[0].name] = person.mentions[0].id
        json_dump(r'db\config.json', config)

    @discord.ui.button(label = "Remover", style=discord.ButtonStyle.danger)
    async def remover(self, interaction: discord.Interaction, button: discord.ui.Button):
        config = json_read(r'db\config.json')

        await interaction.response.edit_message(embed=discord.Embed(title="Remover", description="Marque quem queres remover"))
        person = await interaction.client.wait_for('message', check=lambda m: m.author == interaction.user and m.channel == interaction.channel and len(m.mentions) > 0)
        await interaction.message.edit(embed=discord.Embed(title="Sucesso", description=f"Usuário <@{person.mentions[0].id}> removido com sucesso"))
        del config['blacklist'][person.mentions[0].name]

        json_dump(r'db\config.json', config)

class MusicButtons(discord.ui.View):
    def __init__(self, voice_client, playlist):
        super().__init__()
        self.voice_client = voice_client
        self.playlist = playlist
    
    @discord.ui.button(label = "Pause", style = discord.ButtonStyle.blurple)
    async def pause_resume(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.voice_client.is_paused():
            button.label = "Pause"
            button.style = discord.ButtonStyle.blurple

            self.voice_client.resume()
            await interaction.response.edit_message(view = self)

        else:
            button.label = "Resume"
            button.style = discord.ButtonStyle.success

            self.voice_client.pause()
            await interaction.response.edit_message(view = self)
    
    @discord.ui.button(label = "Stop", style = discord.ButtonStyle.danger)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.voice_client.disconnect()
        self.playlist = []

    @discord.ui.button(label = "Skip", style = discord.ButtonStyle.gray)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.voice_client.stop()