import discord, asyncio
from discord.ext import commands
from functions.func import blacklist
from functions.music_info import get_song_info, get_embed
from functions.buttons import MusicButtons
import yt_dlp

FFMPEG_BEFORE_OPTS = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.playlist = []
        self.music_infos = []
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("[*]Music Cog Carregado")
    
    async def send_embed(self, ctx):
        await ctx.send(embed = get_embed(ctx, self.music_infos.pop(0)), view = self.view)

    def _play_song(self, url, ctx):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url, before_options=FFMPEG_BEFORE_OPTS))
        
        def after_playing(err):
            if len(self.playlist) > 0:
                self._play_song(self.playlist.pop(0), ctx)

                asyncio.run_coroutine_threadsafe(self.send_embed(ctx), self.bot.loop)

            else:
                asyncio.run_coroutine_threadsafe(self.voice_client.disconnect(), self.bot.loop)
        
        self.voice_client.play(source, after = after_playing)


    @commands.command(name = "play")
    async def play(self, ctx, *, link: str):
        self.voice_client = ctx.guild.voice_client

        if not self.voice_client:
            channel = ctx.author.voice.channel
            self.voice_client = await channel.connect()

        info = get_song_info(link)

        if self.voice_client.is_playing():
            await ctx.send(embed = get_embed(ctx, info, "Adicionado à playlist"))

            self.playlist.append(info["url"])
            self.music_infos.append(info)
            return

        self.view = MusicButtons(self.voice_client, self.playlist)

        await ctx.send(embed = get_embed(ctx, info), view = self.view)
        self._play_song(info["url"], ctx = ctx)

async def setup(bot):
    await bot.add_cog(Music(bot))