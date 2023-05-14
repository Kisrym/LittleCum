import yt_dlp
import discord

ydl_opts = {
    'format': 'bestaudio/best',
    'default_search' : 'auto',
    'no_playlist' : True,
    'outtmpl': '%(id)s.mp3',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320'
    }],
    'audio-quality': '0'
}

def get_song_info(link: str) -> dict:
    info ={}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        song_info = ydl.extract_info(link, download=False)

        if "www.youtube" not in link:
            song_info = song_info["entries"][0]

        info['url'] = song_info['formats'][4]['url']
        info["title"] = song_info["title"]
        info["thumbnail"] = song_info["thumbnail"]
        info["video_url"] = song_info["webpage_url"]

    return info

def get_embed(ctx, info: dict, title = "Tocando agora ♪"):
    embed = discord.Embed(title = title, description=f"{info['title']}", colour=discord.Color.dark_purple(), url=info['video_url'])
    embed.set_footer(text=f"Requisitada por {ctx.author.name}")
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar)
    embed.set_thumbnail(url = info["thumbnail"])

    return embed
