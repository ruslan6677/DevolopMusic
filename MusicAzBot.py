#sahibim #Ruslan

#əməyə xatir kanala qoşulun @DvBotlar
import os, youtube_dl, requests, aiohttp, wget, time
from config import Config
from youtube_search import YoutubeSearch
from pyrogram.handlers import MessageHandler
from yt_dlp import YoutubeDL
from io import BytesIO
from aiohttp import ClientSession
from pyrogram import Client, filters, idle
import yt_dlp
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)

bot = Client(
    'MusicAzBot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

##Grupa girende Salamlama

@bot.on_message(filters.new_chat_members, group=1)
async def hg(bot: Client, msg: Message):
    for new_user in msg.new_chat_members:
        if str(new_user.id) == str(Config.BOT_ID):
            await msg.reply(
                f'''`Salam` {msg.from_user.mention} `Məni` {msg.chat.title} `Qrupa əlavə etdiyiniz üçün təşəkkürlər⚡️` \n\n **🤖Qruplardakı userləri tag Edmə üçün Yaradıldım.\n🤖Kömək üçün /start yazmaq kifayətdir.✨**''')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#-------------------------------------------------------------OWNERS SALAMLAMA MSJ---------------------------------------------------------------------------------------#
      
#	elif str(new_user.id) == str(Config.OWNER_ID):
#           await msg.reply('🤖 [Ədalət 𝗧𝗮𝗴𝗴𝗲𝗿](https://t.me/ordayam_5_deqiqeye)-un Sahibi, Qrupa Qatıldı.\n Xoş Gəldin  Aramıza Sahib, Necəsən?🥰.')





#start mesajı

## Əmrlər --------------------------------
@bot.on_message(filters.command(['start']))
def start(client, message):
    MusicAzBot = f'[👋](https://telegra.ph/file/cbfc9ed3f10a194193bcd.jpg) Salam @{message.from_user.username}\n\nMən Bir musiqi botuyam və məndən istifade asandir\n Bir problem olduqda Sahiblə əlaqəyə keçin .\nMusiqi  yükləmək üçün:\n1) /song (musiqi adı)\n2) /song (youtube linki)\n3 /video video adı\n4 /video (youtube linki) Xəta əmələ gələrsə sahiblə əlaqə yaradın'
    message.reply_text(
        text=MusicAzBot, 
        quote=False,
         reply_markup=InlineKeyboardMarkup(
            [
                [
                  InlineKeyboardButton(
                        "➕ ❰ Məni Qrupa Əlavə Et ❱ ➕", url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true"
                    )
                ],
                [ 
                  InlineKeyboardButton(
                        "🔊 Playlis", url=f"https://t.me/{Config.PLAYLIST_NAME}"
                    ),
                  InlineKeyboardButton(
                        "🧑‍⚖️ Sahibim", url=f"https://t.me/{Config.BOT_OWNER}"
                    ),
                ],
                [                     
                  InlineKeyboardButton(
                        "🇦🇿 Botlarım", url=f"https://t.me/{Config.CHANNEL}"
                    ),
                ],
                [
                  InlineKeyboardButton(
                        "💌 Etiraf Botu", url=f"https://t.me/{Config.ETIRAF_BOT}"
                    ),
                ],
                [
                  InlineKeyboardButton(
                        "💬 Etiraf Kanalı", url=f"https://t.me/{Config.ETIRAF_KANALI}"
                    )
                               
                ]
                
           ]
        ),
    )
  
  
#alive mesaji
@bot.on_message(filters.command("alive") & filters.user(Config.BOT_OWNER))
async def live(client: Client, message: Message):
    livemsg = await message.reply_text('`Mükəmməl işləyirəm DevolopMusic`')
    
#musiqi əmri#

@bot.on_message(filters.command("song") & ~filters.edited)
def song(_, message):
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
    m.edit("`📥 Musiqini tapdım və yükləyirəm.`")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎧 **Başlıq**: [{title[:35]}]({link})\n⏳ **Müddət**: `{duration}`\n'f"🎵 Yüklədi [Music Bot](https://t.me/{Config.BOT_USERNAME})"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("📤 Yüklənir..")
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name, performer=f"{Config.PLAYLIST_NAME}")
        m.delete()
        bot.send_audio(chat_id=Config.PLAYLIST_ID, audio=audio_file, caption=rep, performer=f"{Config.BOT_USERNAME}", parse_mode='md', title=title, duration=dur, thumb=thumb_name)
    except Exception as e:
        m.edit('**⚠️ Gözlənilməyən xəta yarandı.**\n**Xahiş edirəm xətanı sahibimə xəbərdar et!**')
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


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
        return await msg.edit(f"🚫 **Hata:** {e}")
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


bot.run()
print("Bot İsleyir")
