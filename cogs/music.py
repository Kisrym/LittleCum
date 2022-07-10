from discord.ext import commands
import discord, youtube_dl, logging, asyncio, math
from discord_components import Button

"""
Créditos ao criador do código original: joek13

Repositório: https://github.com/joek13/py-music-bot
"""


FFMPEG_BEFORE_OPTS = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'

YTDL_OPTS = {
    "default_search": "ytsearch",
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": "in_playlist"
}


class Video:

    def __init__(self, url_or_search, requested_by):
        with youtube_dl.YoutubeDL(YTDL_OPTS) as ydl:
            video = self._get_info(url_or_search)
            video_format = video["formats"][0]
            self.stream_url = video_format["url"]
            self.video_url = video["webpage_url"]
            self.title = video["title"]
            self.uploader = video["uploader"] if "uploader" in video else ""
            self.thumbnail = video["thumbnail"] if "thumbnail" in video else None
            self.requested_by = requested_by
            self._duration = video['duration']

    def _get_info(self, video_url):
        with youtube_dl.YoutubeDL(YTDL_OPTS) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video = None
            if "_type" in info and info["_type"] == "playlist":
                return self._get_info(
                    info["entries"][0]["url"])
            else:
                video = info
            return video

    def embed(self, title="Tocando agora ♪"):
        embed = discord.Embed(title=title, description=f"{self.title}", colour=discord.Color.dark_purple(), url=self.video_url)
        embed.set_footer(text=f"Requisitada por {self.requested_by}")
        embed.set_author(name=self.requested_by.name, icon_url=self.requested_by.avatar_url)
        embed.set_thumbnail(url=self.thumbnail)
        return embed

    def information(self, what="duration"):
        if what == "duration":
            return self._duration
        elif what == "url":
            return self.video_url


async def audio_playing(ctx):
    client = ctx.guild.voice_client
    if client and client.channel and client.source:
        return True
    else:
        raise commands.CommandError("Not currently playing any audio.")

async def in_voice_channel(ctx):
    voice = ctx.author.voice
    bot_voice = ctx.guild.voice_client
    if voice and bot_voice and voice.channel and bot_voice.channel and voice.channel == bot_voice.channel:
        return True
    else:
        raise commands.CommandError(
            "You need to be in the channel to do that.")


async def is_audio_requester(ctx):
    music = ctx.bot.get_cog("Music")
    state = music.get_state(ctx.guild)
    permissions = ctx.channel.permissions_for(ctx.author)
    if permissions.administrator or state.is_requester(ctx.author):
        return True
    else:
        raise commands.CommandError(
            "You need to be the song requester to do that.")


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.states = {}
        self.new_link = []

    def get_state(self, guild):
        if guild.id in self.states:
            return self.states[guild.id]
        else:
            self.states[guild.id] = GuildState()
            return self.states[guild.id]


    @commands.command(aliases=["stop"], help="Para a música atual e limpa a playlist.", description="titulo;Sair;aliases;leave, stop;description;Para a música atual e limpa a playlist;exemplo;=leave")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx):
        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)
        if client and client.channel:
            await client.disconnect()
            state.playlist = []
            state.now_playing = None
        else:
            raise commands.CommandError("Not in a voice channel.")

    @commands.command(aliases=["resume"], help="Pausa a música atual", description="titulo;Pause;aliases;pause, resume;description;Pausa a música atual;exemplo;=pause")
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    @commands.check(is_audio_requester)
    async def pause(self, ctx):
        client = ctx.guild.voice_client
        self._pause_audio(client)

    def _pause_audio(self, client):
        if client.is_paused():
            client.resume()
        else:
            client.pause()

    @commands.command(help="Skipa uma música", description="titulo;Skip;aliases;skip;description;Skipa uma música;exemplo;=skip")
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def skip(self, ctx):
        state = self.get_state(ctx.guild)
        client = ctx.guild.voice_client
        if ctx.channel.permissions_for(
                ctx.author).administrator or state.is_requester(ctx.author):
            client.stop()
            try:
                video = Video(self.new_link[0], ctx.author)
            except: pass
            client.stop()
            await self.mensagem_uau.delete()
            try:
                await self.a.delete()
            except: pass
            self.mensagem_uau = await ctx.send(embed=video.embed(), components=[[Button(label="Pause", style=1), Button(label="Stop", style=4), Button(label="Skip", style=3)]], delete_after=video.information("duration"))
            try:
                self.new_link.pop(0)
            except: pass
        else:
            channel = client.channel
            self._vote_skip(channel, ctx.author)
            users_in_channel = len([
                member for member in channel.members if not member.bot
            ])
            required_votes = math.ceil(
                0.5 * users_in_channel)
            await ctx.send(
                f"{ctx.author.mention} voted to skip ({len(state.skip_votes)}/{required_votes} votes)"
            )

    def _vote_skip(self, channel, member):
        logging.info(f"{member.name} votes to skip")
        state = self.get_state(channel.guild)
        state.skip_votes.add(member)
        users_in_channel = len([
            member for member in channel.members if not member.bot
        ])
        if (float(len(state.skip_votes)) /
                users_in_channel) >= 0.5:
            logging.info(f"Enough votes, skipping...")
            channel.guild.voice_client.stop()

    def _play_song(self, client, state, song):
        state.now_playing = song
        state.skip_votes = set()
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(song.stream_url, before_options=FFMPEG_BEFORE_OPTS), volume=state.volume)

        def after_playing(err):
            if len(state.playlist) > 0:
                next_song = state.playlist.pop(0)
                self._play_song(client, state, next_song)
            else:
                asyncio.run_coroutine_threadsafe(client.disconnect(),
                                                 self.bot.loop)

        client.play(source, after=after_playing)

    @commands.command(aliases=["q", "playlist"], help="Mostra todas as músicas na playlist", description="titulo;Playlist;aliases;queue, playlist, q;description;Mostra todas as músicas na playlist;exemplo;=queue")
    @commands.guild_only()
    @commands.check(audio_playing)
    async def queue(self, ctx):
        state = self.get_state(ctx.guild)
        await ctx.send(embed=self._queue_text(state.playlist))

    def _queue_text(self, queue):
        if len(queue) > 0:
            embed = discord.Embed(title="Playlist", description=f"{len(queue)} músicas na playlist")
            for index, song in enumerate(queue):
                embed.add_field(name=f"{index+1} - **{song.title}**", value=f"(requisitada por **{song.requested_by.name}**", inline=False)
            return embed
        else:
            return "```A playlist está vazia```"


    @commands.command(help="Toca uma música", aliases=['p'], description="titulo;Play;aliases;play, p;description;Toca uma música;exemplo;=play <link>")
    @commands.guild_only()
    async def play(self, ctx, *, url):

        self.author = ctx.author
        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)

        if client and client.channel:
            try:
                video = Video(url, ctx.author)
            except youtube_dl.DownloadError as e:
                logging.warn(f"Error downloading video: {e}")
                await ctx.send(
                    "There was an error downloading your video, sorry.")
                return
            state.playlist.append(video)
            self.new_link.append(video.information("url"))
            self.a = await ctx.send(embed=video.embed("Adicionado à playlist"))

        else:
            if ctx.author.voice is not None and ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel
                try:
                    video = Video(url, ctx.author)
                except youtube_dl.DownloadError as e:
                    await ctx.send(
                        "There was an error downloading your video, sorry.")
                    return
                client = await channel.connect()
                self._play_song(client, state, video)
                self.mensagem_uau = await ctx.send(embed=video.embed(), components=[
                [Button(label="Pause", style=1), Button(label="Stop", style=4), Button(label="Skip", style=3)]
            ], delete_after=video.information())
                while True:
                    voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
                    res = await self.bot.wait_for("button_click", check= lambda x: x.author.id == ctx.author.id)
                    if res.component.label == "Pause":
                        voice.pause()
                        await self.mensagem_uau.edit(embed=video.embed(), components=[
                            [Button(label="Resume", style=3), Button(label="Stop", style=4), Button(label="Skip", style=3)]
                        ])

                        try: await res.respond()
                        except: pass
                    
                    elif res.component.label == "Resume":
                        voice.resume()
                        await self.mensagem_uau.edit(embed=video.embed(), components=[
                        [Button(label="Pause", style=1), Button(label="Stop", style=4), Button(label="Skip", style=3)]
                        ])
                        try: await res.respond()
                        except: pass

                    elif res.component.label == "Stop":
                        await client.disconnect()
                        state.playlist = []
                        state.now_playing = None
                        await self.mensagem_uau.delete()
                    
                    elif res.component.label == "Skip":
                        try:
                            video = Video(self.new_link[0], ctx.author)
                        except: pass
                        client.stop()
                        await self.mensagem_uau.delete()
                        self.mensagem_uau = await ctx.send(embed=video.embed(), components=[[Button(label="Pause", style=1), Button(label="Stop", style=4), Button(label="Skip", style=3)]], delete_after=video.information("duration"))
                        try:
                            self.new_link.pop(0)
                        except: pass

            else:
                raise commands.CommandError(
                    "Você precisa estar em um chat de voz para usar isso")
    

class GuildState:

    def __init__(self):
        self.volume = 1.0
        self.playlist = []
        self.skip_votes = set()
        self.now_playing = None

    def is_requester(self, user):
        return self.now_playing.requested_by == user

    
def setup(bot):
    bot.add_cog(Music(bot))