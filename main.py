from discord.ext import commands
import discord, os
from dotenv import load_dotenv
from functions.func import json_read
from functions.database import importar_database

bot = commands.Bot(command_prefix='=', case_insensitive = True)
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"[Nome] {bot.user.name}\n[I] {bot.user.id}\n")
    importar_database()
    
@bot.command()
async def help(ctx, cog="all"):
    comando = False
    embed = discord.Embed(title="Help", colour=discord.Color.red())
    cogs = [c for c in bot.cogs.keys()] if cog == "all" else [c for c in bot.cogs.keys() if c == cog.capitalize()]
    
    if len(cogs) == 0:
        cogs = [c for c in bot.cogs.keys()]
        comando = True
    
    try:
        cogs.remove("Events")
        cogs.remove("Tasks")
        cogs.remove("Voice")
    except ValueError:
        pass
    
    if comando == False:
        if ctx.author.id not in json_read(r"db\config.json")['owner']: cogs.remove("Admin")
        command_list = ""
        for c in cogs:
            for command in bot.get_cog(c).walk_commands():
                if command.hidden:
                    continue

                elif command.parent != None:
                    continue
                
                command_list += f"**{command}** - *{command.help}*\n"
            embed.add_field(name=c, value=command_list, inline=False)
            command_list = ""
    else:
        cog = bot.get_command(cog)
        
        cog_help = cog.description.split(";")
        cog_help = dict(zip(*[iter(cog_help)]*2))
        embed = discord.Embed(title = cog_help['titulo'], description=f"Sinônimos: `{cog_help['aliases']}`\n\n{cog_help['description']}", colour=discord.Color.red())
        embed.add_field(name="Exemplo(s)", value = cog_help['exemplo'])
        
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/868305867978711140/e5db8fe0c9ea6f4818f54b2b00ea35d8.webp?size=80")
    embed.set_footer(text="Use =help <nome do comando> para informações mais detalhadas.")
    await ctx.message.add_reaction("✅")
    await ctx.send(embed=embed)


for f in os.listdir('./cogs'):
    if f.endswith('.py'):
        bot.load_extension(f'cogs.{f[:-3]}')

load_dotenv()
bot.run(os.getenv('TOKEN'))