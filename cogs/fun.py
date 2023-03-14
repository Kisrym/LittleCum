from discord.ext import commands
from functions.func import blacklist
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from unidecode import unidecode
import PIL.Image, discord
from io import BytesIO
import requests, os

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("[*]Fun Cog Carregado")

    @commands.command(name="say", help="Fala uma frase.", description="titulo;Say;aliases;say;description;Fala uma frase;exemplo;=say <mensagem>")
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(aliases=["as"], help="Transforma uma imagem em ascii", description="titulo;Ascii;aliases;as;description;Transforma uma imagem em uma arte ascii;exemplo;=ascii <link da imagem>")
    async def ascii(self, ctx, link):

        img = PIL.Image.open(BytesIO(requests.get(link).content), mode='r')

        img.save("imagem.png", format="PNG")
        a_chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

        def resize_image(image, new_width=100):
            width, height = image.size
            ratio = height / width
            new_height = int(new_width * ratio)
            resize_image = image.resize((new_width, new_height))
            return resize_image

        def grayify(image):
            grayscale_image = image.convert("L")
            return grayscale_image

        def pixels_to_ascii(image):
            pixels = image.getdata()
            characters = "".join([a_chars[pixel//25] for pixel in pixels])
            return characters

        new_image_data = pixels_to_ascii(grayify(resize_image(PIL.Image.open("imagem.png"))))
        pixel_count = len(new_image_data)
        ascii_image = "\n".join(new_image_data[i:(i+100)] for i in range(0, pixel_count, 100))

        with open(r'imagem.txt', 'w') as texto:
            texto.write(ascii_image)
        with open(r"imagem.txt", "rb") as texto:
            await ctx.send(file=discord.File(texto, "ascii.txt"))

        os.remove(r"imagem.txt")
        os.remove(r"imagem.png")


    @commands.command(help="faz aquele efeito de viado la fds", description="titulo;Efeito;aliases;effect;description;Faz um efeito de 'degradê' no texto;exemplo;=effect <texto>")
    async def effect(self, ctx, *text):
        if ctx.author.id not in blacklist():
            text = " ".join(text)
            x = 0
            uau =[]
            for _ in text:
                x += 1
                uau.append(text[0:x])
                uau.append("\n")
            for _ in text:
                x -= 1
                uau.append(text[0:x])
                uau.append("\n")
            uau = "".join(uau)
            await ctx.send(embed=discord.Embed(description=uau, color=discord.Color.from_rgb(r=102, b=255, g=178)))
        else:
            await ctx.send("vai tomar no cu")

    @commands.command(help="Motra a determinada personalidade do MBTI (tmb n sei pq fiz isso)", description="titulo;Mbti;aliases;mbti;description;Mostra a determinada persoalidade do MBTI;exemplo;=mbti <personalidade>")
    async def mbti(self, ctx, person):
        def __define(name):
            name = unidecode(name.lower())
            p = {"arquiteto":"intj","logico":"intp","comandante":"entj","inovador":"entp","advogado":"infj","mediador":'infp',"protagonista":'enfj','ativista':'enfp','logistico':'istj','defensor':'isfj','executivo':'estj','consul':'esfj','virtuoso':'istp','aventureiro':'isfp','empresario':'estp','animador':'esfp'}
            for k, v in p.items():
                if name == k or name == v:
                    return {"nome":k, "id":v}

        person = __define(person)
        html = urlopen(Request(f"https://www.16personalities.com/br/personalidade-{person['id']}", headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}))
        
        soup = BeautifulSoup(html.read(), 'lxml')

        titulo = soup.find_all('h1')[0].get_text()
        texto = soup.find_all('p')[0].get_text()

        if texto == [x for x in soup.find_all('blockquote')[0].get_text().split('\n') if x != ''][0]:
            texto = soup.find_all('p')[1].get_text()

        file = discord.File(BytesIO(requests.get(f"https://firebasestorage.googleapis.com/v0/b/media-storage-960d5.appspot.com/o/{person['id']}.png?alt=media&token=48a02b7f-407b-4320-8476-1d0ff05d194c").content), filename = "im.png")

        embed = discord.Embed(title=f" {titulo}{person['id'].upper()}", description=texto)
        embed.set_thumbnail(url="attachment://im.png")
        await ctx.send(file = file, embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))