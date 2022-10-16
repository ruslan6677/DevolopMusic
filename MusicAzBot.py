#Buralara əl dəymə...
#Deploy butonuna bas deploy elə.
#Sahibim @HuseynH

import os, youtube_dl, requests, aiohttp, wget, time, lyricsgenius
from config import Config
from youtube_search import YoutubeSearch
from pyrogram.handlers import MessageHandler
from yt_dlp import YoutubeDL
from pyrogram import Client, filters
import yt_dlp
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message, CallbackQuery
)


#config#

bot = Client(
    'MusicAzBot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

#start mesajı
@bot.on_message(filters.command(['start']))
def start(client, message):
    MusicAzBot = f'**Salam** {message.from_user.mention}\n\n**ℹ️ [Mən](http://t.me/{Config.BOT_USERNAME})\n\nsizin üçün musiqini yükləmə botuyam.Məndən istifadə etmək çox asanddır🥰**\n\n**✅ Botun istifadə qaydasını öyrənmək üçün** /help **əmrindən istifadə edin**'
    message.reply_text(
        text=MusicAzBot, 
        quote=False,
         reply_markup=InlineKeyboardMarkup(
            [
                [
                  InlineKeyboardButton(
                        "⚙ Əmrlər", callback_data="help"
                    ),
                   
                   InlineKeyboardButton(
                        "🧑‍💻Sahib Əmrləri", callback_data="owner"
                    ) 
                ],
                [
                  InlineKeyboardButton(
                        "➕ ❰ Məni Qrupa Əlavə Et ❱ ➕", url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true"
                    )
                ],
                [ InlineKeyboardButton(
                        "🔊 Playlis", url="https://t.me/MusicAzPlaylist"
                    )
                ]
                
           ]
        ),
    )
  
#kömək mesajı  
@bot.on_callback_query(filters.regex("help"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
  f"""**{Config.BOT_USERNAME} Əmrləri Bunlardır ⤵️**\n\n**Məsələn:**\n**1.** /song `Payam Turk ft. İslam Şirvani — Mənəm Türk`\n**2.** /video  `Payam Turk ft. İslam Şirvani — Mənəm Türk`\n**3.** /lyrics `Payam Turk ft. İslam Şirvani — Mənəm Türk`**

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                  InlineKeyboardButton(
                        "➕ ❰ Məni Qrupa Əlavə Et ❱ ➕", url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true"
                    )
                    
                ],
                [
                  InlineKeyboardButton(
                        "🔄 Geri Qayıt", callback_data="start"),
                    InlineKeyboardButton(
                        "🔙 bağla", callback_data="close"
                    )
                ]
            ]
        )
    )  
  

@bot.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()



#bot sahibi əmrləri

@bot.on_callback_query(filters.regex("owner"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🎛️{Config.BOT_USERNAME} !</b>**Sahib Əmrləri Və Sahibləri**
  **/alive - Botun işlək olduğunu yoxlamaq üçün əmrdir.**
        
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                  InlineKeyboardButton(
                        "➕ ❰ Məni Qrupa Əlavə Et ❱ ➕", url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🧑‍💻 Developer", url=f"t.me/Xwarn"
                    ),
                    InlineKeyboardButton('Sahib 👨🏻‍💻', url=f'T.me/{Config.BOT_OWNER}')
                ],
                [
                    InlineKeyboardButton(
                        "🔄 Geri Qayıt", callback_data="start"),
                    InlineKeyboardButton(
                        "🔙 Bağla", callback_data="close"
                    )
                ]
            ]
        )
    )

   
#alive mesaji#

@bot.on_message(filters.command("alive") & filters.user(Config.BOT_OWNER))
async def live(client: Client, message: Message):
    livemsg = await message.reply_text('`Mən İşləyirəm MusicAzBot`')
    
#musiqi əmri#

buttons = {
  "markup_for_private": InlineKeyboardMarkup([[InlineKeyboardButton('Playlist ♬', url=f'https://t.me/{Config.PLAYLIST_NAME}')]]),
  "add_to_group": InlineKeyboardMarkup([[InlineKeyboardButton('〆 Qrupa əlavə et 〆', url=f'https://t.me/{Config.BOT_USERNAME}?startgroup=true')]]),
}

@bot.on_message(filters.command("song") & ~filters.edited)
def song(_, message):
    isteyen = message.from_user.mention 
    query = " ".join(message.command[1:])
    m = message.reply("<b>Musiqi Axtarılır ... 🔍</b>")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        m.edit("İstədiyiniz musiqi tapılmadı 😔")
        print(str(e))
        return
    m.edit("`📥 Musiqini tapdım və endirirəm.`")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        caption_for_logchannel = f'''
**╭───────────────**
**├▷ ♬ Başlıq: [{title[:35]}]({link})**
**├───────────────**
**├▷👤 İstəyən: {isteyen}**
**├───────────────**
**├▷🌀 Bot: @{Config.BOT_USERNAME}**
**╰───────────────**
'''
        caption_for_private = f'''
**╭───────────────**
**├▷ ♬ Başlıq: [{title[:35]}]({link})**
**├───────────────**
**├▷🌀 Bot: @{Config.BOT_USERNAME}**
**╰───────────────**
'''

        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("📤 Yüklənir..")
        message.reply_audio(audio_file, caption=caption_for_private, quote=False, title=title, duration=dur, thumb=thumb_name, performer="MusicAzPlaylist", reply_markup=buttons['markup_for_private'])
        m.delete()
        bot.send_audio(chat_id=Config.PLAYLIST_ID, audio=audio_file, caption=caption_for_logchannel, performer="@MusicAzBot", title=title, duration=dur, thumb=thumb_name, reply_markup=buttons['add_to_group'])
    except Exception as e:
        m.edit('**⚠️ Gözlənilməyən xəta yarandı.**\n**Xahiş edirəm xətanı sahibimə xəbərdar et!**')
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
        
##############################

### video


@bot.on_message(filters.command("video") & ~filters.edited)
async def vsong(client, message):
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        message.from_user.mention
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("📥 **Video Axtarılır...**")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"🚫 **Xəta Bu Xəta Təkrar Olarsa Sahibimlə Əlaqə Saxla:** {e}")
    preview = wget.download(thumbnail)
    await msg.edit("📤 **Videonu tapdım və endirirəm ...**")
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=ytdl_data["title"],
    )
    try:
        os.remove(file_name)
        await msg.delete()
    except Exception as e:
        print(e)
############################        
        
####lyrics

@bot.on_message(filters.command("lyrics") & ~filters.edited)
async def lrsearch(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**İstifadə:**\n\n/lyrics [ Musiqi Adı]")
    m = await message.reply_text("Mahnı sözləri axtarılır")
    query = message.text.split(None, 1)[1]
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    y.verbose = False
    S = y.search_song(query, get_full_info=False)
    if S is None:
        return await m.edit("Lyrics not found :p")
    xxx = f"""
** Yüklədi {Config.BOT_USERNAME} 🇦🇿**

**Axtarılan Mahnı:-** __{query}__
 **Found Lyrics For:-** __{S.title}__
 **Rəssam:-** {S.artist}

 **__ Mahnı sözləri:__**

{S.lyrics}"""
    if len(xxx) > 4096:
        await m.delete()
        filename = "lyrics.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(xxx.strip()))
        await message.reply_document(
            document=filename,
            caption=f"**Sözlər çox olduğundan fayl edib atdım...:**\n\n`Lyrics`",
            quote=False,
        )
        os.remove(filename)
    else:
        await m.edit(xxx)


bot.run()
