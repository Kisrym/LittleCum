from tabnanny import check
from discord.ext import commands
import discord, asyncio
from unidecode import unidecode
from discord_components import DiscordComponents, Button
from functions.func import blacklist
from time import perf_counter

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        DiscordComponents(bot)
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('[*]Games Cog Carregado')
    
    @commands.command(help="Jogo da velha normal ue", aliases=['velha', 'jogodavelha', 'tic'], description="titulo;Jogo da velha;aliases;tictactoe, velha, jogodavelha, tic;description;Jogo da velha normal;exemplo;=tictactoe")
    async def tictactoe(self, ctx):
        #! funções
        def formatar_template(template):
            a = 0
            final = []
            for c in template:
                if a == 3:
                    final.append("\n")
                    a = 0
                final.append(c)
                a += 1
                
            return "".join(final)
        
        def validate(lista, l):
            if lista[:3].count(l) == 3 or lista[3:6].count(l) == 3 or lista[6:9].count(l) == 3:
                return True
                
            elif lista[0:9:3].count(l) == 3 or lista[1:9:3].count(l) == 3 or lista[2:9:3].count(l) == 3:
                return True
                
            elif lista[0:9:4].count(l) == 3 or lista[2:8:2].count(l) == 3:
                return True
                
            else:
                return False
        
        if ctx.author.id not in blacklist():
            #! Interface inicial
            players = []
            players.append(ctx.author.id)
            
            interface = await ctx.send(embed=discord.Embed(title="Tic Tac Toe", description="Para participar, clique no botão abaixo."), components=[Button(label="Participar", style=3)])
            
            res = await self.bot.wait_for('button_click', check=lambda i: i.author.id != ctx.author.id)
            if res.component.label == 'Participar':
                players.append(res.author.id)
            
            await interface.edit(embed=discord.Embed(title="Tic Tac Toe", description= "Participantes:\n" + '\n'.join([f'<@{x}>' for x in players]) + "\n**INICIANDO JOGO...**"), components="")
            
            #! Jogo
            vez = 0
            template = ["🟥", "🟥", "🟥", "🟥", "🟥", "🟥", "🟥", "🟥", "🟥"]

            mensagem = await ctx.send(formatar_template(template), components = 
                [[Button(label = "❌", custom_id= "0"), Button(label = "❌", custom_id="1"), Button(label = "❌", custom_id="2")],
                [Button(label = "❌", custom_id= "3"), Button(label = "❌", custom_id="4"), Button(label = "❌", custom_id="5")],
                [Button(label = "❌", custom_id= "6"), Button(label = "❌", custom_id="7"), Button(label = "❌", custom_id="8")]]
                )
            
            while True:
                if vez % 2 == 0:
                    await mensagem.edit(formatar_template(template), components = 
                                [[Button(label = "❌", custom_id= "0"), Button(label = "❌", custom_id="1"), Button(label = "❌", custom_id="2")],
                                [Button(label = "❌", custom_id= "3"), Button(label = "❌", custom_id="4"), Button(label = "❌", custom_id="5")],
                                [Button(label = "❌", custom_id= "6"), Button(label = "❌", custom_id="7"), Button(label = "❌", custom_id="8")]]
                                )
                    
                    res = await self.bot.wait_for('button_click', check=lambda i: i.author.id == players[0])
                    if template[int(res.component.custom_id)] == '🟥':
                        template[int(res.component.custom_id)] = '❌'
                    
                    try: await res.respond()
                    except: pass
                    
                else:
                    await mensagem.edit(formatar_template(template), components = 
                        [[Button(label = "⭕", custom_id= "0"), Button(label = "⭕", custom_id="1"), Button(label = "⭕", custom_id="2")],
                        [Button(label = "⭕", custom_id= "3"), Button(label = "⭕", custom_id="4"), Button(label = "⭕", custom_id="5")],
                        [Button(label = "⭕", custom_id= "6"), Button(label = "⭕", custom_id="7"), Button(label = "⭕", custom_id="8")]]
                        )
                    
                    res = await self.bot.wait_for('button_click', check=lambda i: i.author.id == players[1])
                    if template[int(res.component.custom_id)] == '🟥':
                        template[int(res.component.custom_id)] = '⭕'
                        
                    try: await res.respond()
                    except: pass
                    
                vez += 1
                
            #! ver quem ganhou
                if validate(template, '❌'):
                    await ctx.channel.purge(limit=1)
                    await interface.edit(embed = discord.Embed(title="Tic Tac Toe", description=f"<@{players[0]}> venceu!! 🥳🥳"), components="")
                    break
                elif validate(template, '⭕'):
                    await ctx.channel.purge(limit=1)
                    await interface.edit(embed = discord.Embed(title="Tic Tac Toe", description=f"<@{players[1]}> venceu!! 🥳🥳"), components="")
                    break
                elif template.count('🟥') == 0:
                    await ctx.channel.purge(limit=1)
                    await interface.edit(embed = discord.Embed(title="Tic Tac Toe", description="Empate!! 😔😔"), components="")
                    break
        
        else:
            await ctx.send("vai se foder arrombado")
    
    @commands.command(help="jogo da forca normal ora bolas", aliases = ['forca'], description=f"titulo;Jogo da forca;aliases;jogodaforca, forca;description;Jogo da forca normal ora bolas;exemplo;=jogodaforca")
    async def jogodaforca(self, ctx):
        HANGMANPICS = ['''
        +---+
        |   |
            |
            |
            |
            |
        =========''', '''
        +---+
        |   |
        O   |
            |
            |
            |
        =========''', '''
        +---+
        |   |
        O   |
        |   |
            |
            |
        =========''', '''
        +---+
        |   |
        O   |
       /|   |
            |
            |
        =========''', '''
        +---+
        |   |
        O   |
       /|\  |
            |
            |
        =========''', '''
        +---+
        |   |
        O   |
       /|\  |
       /    |
            |
        =========''', '''
        +---+
        |   |
        O   |
       /|\  |
       / \  |
            |
        =========''']
        
        if ctx.author.id not in blacklist():
            user = await self.bot.fetch_user(ctx.message.author.id)
            await user.send(embed = discord.Embed(title="Jogo da Forca", description="Digite aqui a palavra secreta: "))
            
            palavra_secreta = await self.bot.wait_for('message', check=lambda i: i.author.id == ctx.author.id)
            palavra_secreta = unidecode(palavra_secreta.content.replace(" ", "").lower())
            players = []
            backlash = '\n'
            
            info = await ctx.send(embed = discord.Embed(title="Jogo da Forca", description = "Quem irá participar?"), components = [Button(label = "Participar", style = 3)])
            while True:
                try:
                    await info.edit(embed = discord.Embed(title="Jogo da Forca", description = f"Quem irá participar?\n**Jogadores:**\n{''.join([f'<@{x}>{backlash}' for x in players])}"), components = [Button(label = "Participar", style = 3)])
                    res = await self.bot.wait_for('button_click', check = lambda i: i.channel == ctx.channel and i.author.id not in players and i.author.id != ctx.author.id, timeout = 10)
                    
                    if res.component.label == "Participar":
                        players.append(res.author.id)
                        
                    try: await res.respond()
                    except: pass
                    
                except: 
                    break
            
            if len(players) == 0:
                await info.edit(embed = discord.Embed(title = "Jogo da Forca", description = "Jogo encerrado. Nenhum player"), components = "")
                return
            
            await info.edit(embed = discord.Embed(title="Jogo da Forca", description = f"Jogo iniciado!!\n**Jogadores:**\n{''.join([f'<@{x}>{backlash}' for x in players])}"), components = "")
            channel = await ctx.guild.create_text_channel(f"jogo-da-forca")
            tries = 6
            acertos = 0
            word = list('-' * len(palavra_secreta))
            letras = []
            
            players_dict = dict(zip([x for x in range(len(players))], players))
            cont = 0
            
            info = await channel.send(embed=discord.Embed(title="Jogo da Forca", description=f"```{HANGMANPICS[tries]}```\n**{''.join(word)}**\nDigite uma letra"))
            
            HANGMANPICS.reverse()
            
            while True:
                acertou = False
                if cont == len(players): cont = 0 #? reiniciando o contador
                await info.edit(embed=discord.Embed(title="Jogo da Forca", description=f"```{HANGMANPICS[tries]}```\n**{''.join(word)}**\nLetras que já foram: **{', '.join(letras)}**\nDigite uma letra <@{players_dict.get(cont)}>:"))
                
                letra = await self.bot.wait_for('message', check=lambda i: i.channel == channel and i.author.id == players_dict.get(cont))
                if (len(letra.content) == 1 and letra.content not in letras):
                    letras.append(letra.content)
                    for l in range(len(palavra_secreta)):
                        if letra.content == palavra_secreta[l]:
                            acertou = True
                            word[l] = palavra_secreta[l]
                            if acertou == True: acertos += 1
                        elif letra.content not in palavra_secreta:
                            tries -= 1
                            break
                    
                    cont += 1
                
                elif letra.content == palavra_secreta:
                    acertos = len(palavra_secreta)
                    word = [x for x in palavra_secreta]
                
                if tries > 0 and acertos >= len(palavra_secreta) and palavra_secreta == str("".join(word)):
                    await channel.send(embed=discord.Embed(title="Jogo da Forca", description=f"```{HANGMANPICS[tries]}```\n**{''.join(word)}**\n<@{letra.author.id}> ganhou!!!"))
                    break
                
                elif tries == 0 and palavra_secreta != word:
                    await channel.send(embed=discord.Embed(title="Jogo da Forca", description=f"```{HANGMANPICS[tries]}```\n**{''.join(word)}**\nTodo mundo perdeu :(\nA palavra era: **{palavra_secreta}**"))
                    break
                
            await asyncio.sleep(10)
            await channel.delete()
        else:
            await ctx.send("vai se foder arrombado")
        
    @commands.command(aliases=['ppt', 'jokenpo'], help="Jogo de Jokenpo fodase", description=f"titulo;Pedra Papel Tesoura;aliases;pedrapapeltesoura, ppt, jokenpo;description;Jogo de Jokenpo normal;exemplo;=ppt")
    async def pedrapapeltesoura(self, ctx):
        players = []
        jogadas = []
        icones = {
            "pedra":"👊",
            "papel":"🖐️",
            "tesoura":"✌️"
        }
        
        info = await ctx.send(embed=discord.Embed(title="Pedra Papel Tesoura", description="Para participar, clique no botão abaixo."), components=[Button(label="Participar", style=3)])
        res = await self.bot.wait_for('button_click', check=lambda i: i.channel == ctx.channel and i.author.id != ctx.author.id, timeout=10)
        
        if res.component.label == "Participar":
            players.append(ctx.author.id)
            players.append(res.author.id)
        
        _ = "\n"
        
        await info.edit(embed=discord.Embed(title="Pedra Papel Tesoura", description=f"Jogo iniciado!\nParticipantes:\n{_.join([f'<@{x}>' for x in players])}"), components="")
        
        jogo = await ctx.send(embed=discord.Embed(title="Pedra Papel Tesoura", description=f"Vez de <@{players[0]}>. Espere a jogada."), components = [[
            Button(label="👊", style=1),
            Button(label="🖐️", style=1),
            Button(label="✌️", style=1)
        ]])
        
        for vez in range(2):
            res = await self.bot.wait_for('button_click', check=lambda i: i.channel == ctx.channel and i.author.id == players[vez], timeout=10)
            
            if res.component.label == "👊":
                jogadas.append("pedra")
            elif res.component.label == "🖐️":
                jogadas.append("papel")
            elif res.component.label == "✌️":
                jogadas.append("tesoura")
        
        if jogadas[0] == jogadas[1]:
            await jogo.edit(embed=discord.Embed(title="Pedra Papel Tesoura", description=f"**<:trollface:843147626219307029> Empate <:trollface:843147626219307029>**!\n\n**Jogadas:**\n**{jogadas[0].capitalize()} {icones.get(jogadas[0])}**: <@{players[0]}>\n**{jogadas[1].capitalize()} {icones.get(jogadas[1])}:** <@{players[1]}>"), components="")
        
        if jogadas[0] == "pedra" and jogadas[1] == "tesoura":
            await jogo.edit(embed=discord.Embed(title="Pedra Papel Tesoura", description=f"Vencedor: <@{players[0]}> 🏆!\n\n**Jogadas:**\n**{jogadas[0].capitalize()} {icones.get(jogadas[0])}:** <@{players[0]}>\n**{jogadas[1].capitalize()} {icones.get(jogadas[1])}:** <@{players[1]}>"), components="")
        elif jogadas[1] == "pedra" and jogadas[0] == "tesoura":
            await jogo.edit(embed=discord.Embed(title="Pedra Papel Tesoura", description=f"Vencedor: <@{players[1]}> 🏆!\n\n**Jogadas:**\n**{jogadas[0].capitalize()} {icones.get(jogadas[0])}:** <@{players[0]}>\n**{jogadas[1].capitalize()} {icones.get(jogadas[1])}:** <@{players[1]}>"), components="")
        
        if jogadas[0] == "papel" and jogadas[1] == "pedra":
            await jogo.edit(embed=discord.Embed(title="Pedra Papel Tesoura", description=f"Vencedor: <@{players[0]}> 🏆!\n\n**Jogadas:**\n**{jogadas[0].capitalize()} {icones.get(jogadas[0])}:** <@{players[0]}>\n**{jogadas[1].capitalize()} {icones.get(jogadas[1])}:** <@{players[1]}>"), components="")
        elif jogadas[1] == "papel" and jogadas[0] == "pedra":
            await jogo.edit(embed=discord.Embed(title="Pedra Papel Tesoura", description=f"Vencedor: <@{players[1]}> 🏆!\n\n**Jogadas:**\n**{jogadas[0].capitalize()} {icones.get(jogadas[0])}:** <@{players[0]}>\n**{jogadas[1].capitalize()} {icones.get(jogadas[1])}:** <@{players[1]}>"), components="")

        jogo.delete()
        
def setup(bot):
    bot.add_cog(Games(bot))