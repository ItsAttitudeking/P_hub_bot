import os
from aiohttp import ClientSession
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from Python_ARQ import ARQ 
from asyncio import get_running_loop
from wget import download

# Config Check-----------------------------------------------------------------
if os.path.exists("config.py"):
    from config import *
elif os.path.exists("sample_config.py"):
    from sample_config import *
else:
    raise Exception("Your Config File Is Invalid or Maybe Doesn't Exist! Please Check Your Config File or Try Again.")

# ARQ API and Bot Initialize---------------------------------------------------
session = ClientSession()
arq = ARQ("https://thearq.tech", ARQ_API_KEY, session)
pornhub = arq.pornhub
phdl = arq.phdl

app = Client("P_Hub_Bot", bot_token=Bot_token, api_id=6,
             api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")
print("\n ➢𝐎𝐀𝐍 Bot Started!...\n")

db = {}

async def download_url(url: str):
    loop = get_running_loop()
    file = await loop.run_in_executor(None, download, url)
    return file

async def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":")))
    )
# Start  -----------------------------------------------------------------------
@app.on_message(
    filters.command("start") & ~filters.edited
)
async def start(_, message):
    m= await message.reply_text(
        text = "[🔔](https://telegra.ph/file/508d8bc4e86ff19a7c958.jpg) *Hi Iam @P_Hub_Robot 🔞* \n\n *📥You can Download Videos from PHub upto 1080p* ! \n\n\n 🔗𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 : *@Attitude_Network*"
       )

# Help-------------------------------------------------------------------------
@app.on_message(
    filters.command("help") & ~filters.edited
)
async def help(_, message):
    await message.reply_text(
        """**📍Below are My Commands...🔧**

📌 /help ➢ To Show This Message.
📌 /repo ➢ To Get the Repo.

🔎To Search in PHub just simply Type something

🔗𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 : @Attitude_Network"""
    )
    
# Repo  -----------------------------------------------------------------------
@app.on_message(
    filters.command("repo") & ~filters.edited
)
async def repo(_, message):
    m= await message.reply_text(
        text="""[➢𝐎𝐀𝐍 : Repo📍](https://github.com/ItsAttitudeking/P_hub_bot) | [Support Group](https://t.me/OAN_Support)""",
        disable_web_page_preview=True
       )

# Let's Go----------------------------------------------------------------------
@app.on_message(
    filters.private & ~filters.edited & ~filters.command("help") & ~filters.command("start") & ~filters.command("repo")
    )
async def sarch(_,message):
    try:
        if "/" in message.text.split(None,1)[0]:
            await message.reply_text(
                "**⏳Usage:**\n🕹️Just type Something to search in PHub Directly"
            )
            return
    except:
        pass
    m = await message.reply_text("📡Getting Results.....")
    search = message.text
    try:
        resp = await pornhub(search,thumbsize="large")
        res = resp.result
    except:
        await m.edit("❌Found Nothing... Try again")
        return
    if not resp.ok:
        await m.edit("❌Found Nothing... Try again")
        return
    resolt = f"""
**Title:** {res[0].title}
**views:** {res[0].views}
**rating:** {res[0].rating}"""
    await m.delete()
    m = await message.reply_photo(
        photo=res[0].thumbnails[0].src,
        caption=resolt,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔵Next🔵",
                                         callback_data="next"),
                    InlineKeyboardButton(,"🔴Delete🔴",
                                         callback_data="delete"),
                ],
                [
                    InlineKeyboardButton("🟡Download🟡",
                                         callback_data="dload")
                ]
            ]
        ),
        parse_mode="markdown",
    )
    new_db={"result":res,"curr_page":0}
    db[message.chat.id] = new_db
    
 # Next Button--------------------------------------------------------------------------
@app.on_callback_query(filters.regex("next"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("❌Something Wrong ..... **Search Again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page+1
    db[query.message.chat.id]['curr_page'] = cur_page
    if len(res) <= (cur_page+1):
        cbb = [
                [
                    InlineKeyboardButton("🟣Previous🟣",
                                         callback_data="previous"),
                    InlineKeyboardButton("🟢Download🟢",
                                         callback_data="dload"),
                ],
                [
                    InlineKeyboardButton("🔴Delete🔴",
                                         callback_data="delete"),
                ]
              ]
    else:
        cbb = [
                [
                    InlineKeyboardButton("🟣Previous🟣",
                                         callback_data="previous"),
                    InlineKeyboardButton("🔵Next🔵",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("🔴Delete🔴",
                                         callback_data="delete"),
                    InlineKeyboardButton("🟢Download🟢",
                                         callback_data="dload")
                ]
              ]
    resolt = f"""
**Title:** {res[cur_page].title}
**views:** {res[cur_page].views}
**rating:** {res[cur_page].rating}"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )
 
# Previous Button-------------------------------------------------------------------------- 
@app.on_callback_query(filters.regex("previous"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("❌Something Wrong ..... **Search Again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page-1
    db[query.message.chat.id]['curr_page'] = cur_page
    if cur_page != 0:
        cbb=[
                [
                    InlineKeyboardButton("🟣Previous🟣",
                                         callback_data="previous"),
                    InlineKeyboardButton("🔵Next🔵",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("🔴Delete🔴",
                                         callback_data="delete"),
                    InlineKeyboardButton("🟢Download🟢",
                                         callback_data="dload")
                ]
            ]
    else:
        cbb=[
                [
                    InlineKeyboardButton("🔵Next🔵",
                                         callback_data="next"),
                    InlineKeyboardButton("🔴Delete🔴",
                                         callback_data="Delete"),
                ],
                [
                    InlineKeyboardButton("🟢Download🟢",
                                         callback_data="dload")
                ]
            ]
    resolt = f"""
**Title:** {res[cur_page].title}
**views:** {res[cur_page].views}
**rating:** {res[cur_page].rating}"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )

# Download Button--------------------------------------------------------------------------    
@app.on_callback_query(filters.regex("dload"))
async def callback_query_next(_, query):
    m = query.message
    data = db[m.chat.id]
    res = data['result']
    curr_page = int(data['curr_page'])
    dl_links = await phdl(res[curr_page].url)
    db[m.chat.id]['result'] = dl_links.result.video
    db[m.chat.id]['thumb'] = res[curr_page].thumbnails[0].src
    db[m.chat.id]['dur'] = res[curr_page].duration
    resolt = f"""
**Title:** {res[curr_page].title}
**views:** {res[curr_page].views}
**rating:** {res[curr_page].rating}"""
    pos = 1
    cbb = []
    for resolts in dl_links.result.video:
        b= [InlineKeyboardButton(f"{resolts.quality} - {resolts.size}", callback_data=f"phubdl {pos}")]
        pos += 1
        cbb.append(b)
    cbb.append([InlineKeyboardButton("🔴Delete🔴", callback_data="delete")])
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )

# Download Button 2--------------------------------------------------------------------------    
@app.on_callback_query(filters.regex(r"^phubdl"))
async def callback_query_dl(_, query):
    m = query.message
    capsion = m.caption
    entoty = m.caption_entities
    await m.edit(f"**Downloading Now :\n\n{capsion}")
    data = db[m.chat.id]
    res = data['result']
    curr_page = int(data['curr_page'])
    thomb = await download_url(data['thumb'])
    durr = await time_to_seconds(data['dur'])
    pos = int(query.data.split()[1])
    pos = pos-1
    try:
        vid = await download_url(res[pos].url)
    except Exception as e:
        print(e)
        await m.edit("❌Oops Download Error... Try again")
        return
    await m.edit(f"**Uploading Now :\n\n'''{capsion}'''")
    await app.send_chat_action(m.chat.id, "upload_video")
    await m.edit_media(media=InputMediaVideo(vid,thumb=thomb, duration=durr, supports_streaming=True))
    await m.edit_caption(caption=capsion, caption_entities=entoty)
    if os.path.isfile(vid):
        os.remove(vid)
    if os.path.isfile(thomb):
        os.remove(thomb)
    
# Delete Button-------------------------------------------------------------------------- 
@app.on_callback_query(filters.regex("delete"))
async def callback_query_delete(_, query):
    await query.message.delete()
    
app.run()
