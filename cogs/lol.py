import discord, requests, os
from riotwatcher import LolWatcher
from discord.ext import commands
from functions.func import blacklist, define, champ
from datetime import datetime
from dotenv import load_dotenv

emblems = {
                "bronze":"<:bronze:896581593118945300>",
                "silver":"<:silver:896583109959614514>",
                "gold":"<:gold:896582843793289307>",
                "platinum":"<:platinum:896583078724636683>",
                "diamond":"<:diamond:896582802567471114>",
                "master":"<:master:896582998953185300>",
                "grandmaster":"<:grandmaster:896582880430542888>",
                "challenger":"<:challenger:896582773891014676>"
            }

load_dotenv()
API_KEY = os.getenv('RGAPI-ce428226-a1c4-4aee-a56e-b9a12c8c41e2')

class Lol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[*]League of Legends Cog Carregado")


    @commands.command(help="Mostra informações sobre determinado player", description="titulo;Informação;aliases;info;description;Mostra informações sobre um player;exemplo;=info <player> [região]")
    async def info(self, ctx, *, summonername, region="br1"):
        if ctx.author.id not in blacklist():
            try:
                summonername = summonername.lower().replace(" ", "")
                for c in ["EUN1", "EUW1", "JP1", "KR", "LA1", "LA2", "NA1", "OC1", "RU", "TR1"]:
                    if c in summonername.upper():
                        region = c
                if region == "br1":
                    summoner_info = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonername}?api_key={API_KEY}").json()
                else:
                    summoner_info = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonername[:-2]}?api_key={API_KEY}").json()
                summoner_ranked_info = LolWatcher(f"{API_KEY}").league.by_summoner(f"{region}", f"{summoner_info['id']}")
                def emblema(tier):
                    for keys, values in emblems.items():
                        if tier.lower() == keys:
                            return values
                def queue_type(queueType):
                    if queueType == "RANKED_FLEX_SR":
                        return "Flex"
                    elif queueType == "RANKED_SOLO_5x5":
                        return "Solo/Duo"
                embed = discord.Embed(
                    title = summoner_info["name"]
                )
                def maestria(i):
                    if i == 7:
                        return "<:m7:930979443520987146>"
                    elif i == 6:
                        return '<:m6:930979417331736616>'
                    elif i == 5:
                        return '<:m5:930979384771379250>'
                    else:
                        return '<:m4:930979314063781949>'
                embed.add_field(name="Level", value=summoner_info["summonerLevel"])
                if len(summoner_ranked_info) > 1:
                    embed.add_field(name=queue_type(summoner_ranked_info[0]["queueType"]), value=emblema(summoner_ranked_info[0]['tier'].lower()) + summoner_ranked_info[0]['tier'].capitalize() + " " + summoner_ranked_info[0]["rank"] + f" ({summoner_ranked_info[0]['leaguePoints']})")
                    embed.add_field(name=queue_type(summoner_ranked_info[1]["queueType"]), value=emblema(summoner_ranked_info[1]['tier'].lower()) + summoner_ranked_info[1]['tier'].capitalize() + " " + summoner_ranked_info[1]["rank"]+ f" ({summoner_ranked_info[1]['leaguePoints']})")
                elif len(summoner_ranked_info) == 1:
                    embed.add_field(name=queue_type(summoner_ranked_info[0]["queueType"]), value=emblema(summoner_ranked_info[0]['tier'].lower()) + summoner_ranked_info[0]['tier'].capitalize() + " " + summoner_ranked_info[0]["rank"]+ f" ({summoner_ranked_info[0]['leaguePoints']})")
                embed.set_footer(text="Se o jogador que pesquisava não condiz com o jogador acima, tente trocar de região.")
                embed.set_thumbnail(url="https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/"+str(summoner_info["profileIconId"]) + ".jpg")

                masteries = requests.get(f"https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_info['id']}?api_key={API_KEY}").json()[:3]
                try:
                    for c in range(3):
                        embed.add_field(name=f"\n{'<:ba:931153229952192522>' if not masteries[c]['chestGranted'] else ''} {define(champ(masteries[c]['championId'], False), False)}", value=f"Rank: {maestria(masteries[c]['championLevel'])}{masteries[c]['championPoints']} pts\nÚltima vez jogado: {datetime.fromtimestamp(int(masteries[c]['lastPlayTime'])/1000.0).strftime('%d/%m/%y')}", inline=False)
                except IndexError:
                    pass

                await ctx.send(embed=embed)
            except KeyError:
                await ctx.send("Usuário não encontrado.")
        else:
            await ctx.send("vai tomar no seu cu")


    @commands.command(help="Mostra informações sobre determinado champion.", aliases=['champ', 'ch'], description="titulo;Campeão;aliases;champion, champ, ch;description;Mostra informações sobre o champion;exemplo;=champion <champion>")
    async def champion(self, ctx, *, champion_name):
        if ctx.author.id not in blacklist():
            champion_name = define(champion_name.replace(" ", "").replace("'", "").capitalize())
            try:
                champion_info = requests.get("http://ddragon.leagueoflegends.com/cdn/12.2.1/data/pt_BR/champion.json").json()["data"][f"{champion_name}"]
            except KeyError:
                await ctx.send("Champion não encontrado")
                return
                
            embed = discord.Embed(
                title= champion_info["name"] + ", " + champion_info["title"],
                description= champion_info["blurb"],
                url=f"https://www.leagueofgraphs.com/pt/champions/builds/{champion_info['name'].replace(' ', '').lower()}"
            )
            embed.set_thumbnail(url="https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/" + str(champion_info["key"]) + ".png")
            embed.add_field(name="Classe(s)", value='\n'.join(champion_info["tags"]))
            embed.add_field(name="Base Stats", value=
                                                "<:health:896579402912108615>Health: "+str(champion_info["stats"]["hp"]) + "\n" +
                                                "<:mana:896579329071386634>Mana: "+str(champion_info["stats"]["mp"]) + "\n" +
                                                "<:armor:896579352483991553>Armor: "+str(champion_info["stats"]["armor"]) + "\n" +
                                                "<:magicresist:896579427746611262>Magic Resist: "+str(champion_info["stats"]["spellblock"]) + "\n" +
                                                "<:movespeed:896579462311837716>Movement Speed: "+str(champion_info["stats"]["movespeed"]) + "\n" +
                                                "<:attackdamage:896579376135675956>Attack Damage: "+str(champion_info["stats"]["attackdamage"])
                                                )
            embed.set_image(url="https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-splashes/"+str(champion_info["key"])+"/"+str(champion_info["key"])+"000.jpg")
            await ctx.send(embed=embed)
        else:
            await ctx.send("vai tomar no seu cu")


    @commands.command(help="Mostra os champions dessa semana", description="titulo;Rotação;aliases;rotation;description;Mostra os champions grátis dessa semana;exemplo;=rotation")
    async def rotation(self, ctx):
        r = requests.get(f"https://br1.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={API_KEY}").json()["freeChampionIds"]
        embed = discord.Embed(title="Rotação grátis", description='**-  {}**'.format("\n - ".join([champ(x, False) for x in r])))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Lol(bot))