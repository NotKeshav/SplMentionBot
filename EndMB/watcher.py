from pyrogram import Client, filters
from pyrogram.types import Message
from Database.Mongo.chats import *
from Database.Mongo.users import *
from EndMB.EndAll import ALPHA

@Client.on_message(group=1)
async def watch(_, m):
    if m.chat.type == "private":
        return
    is_served_ = await is_served_chat(m.chat.id)
    if is_served_:
        return
    await add_served_chat(m.chat.id)

@Client.on_message(filters.command("schats") & filters.user(ALPHA))
async def servedc(_, m):
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
        if str(chat) == "-1001680465920":
            chats.remove((chat))
    LISTED = []
    msg = ""
    for i in chats:
        if i in LISTED:
            continue
        LISTED.append(i)
        i = str(i)
        msg += f"\n<code>{i}</code>"
    await m.reply(f"**Served chats**\n\n{msg}\n\n**Count** :- {len(chats)}")

@Client.on_message(filters.command("susers") & filters.user(ALPHA))
async def servedu(_, m):
    chats = []
    schats = await get_users()
    for chat in schats:
        chats.append(int(chat["a"]))
        if str(chat) == "-1001680465920":
            chats.remove((chat))
    msg = ""
    for i in chats:
        i = str(i)
        msg += f"\n<code>{i}</code>"
    await m.reply(f"**Served users**\n\n{msg}\n\n**Count** :- {len(chats)}")


PIC = "https://te.legra.ph/file/d0def824525604b2c1fb8.jpg"

@Client.on_message(filters.new_chat_members, group=2)
async def welcome(_, m):
    chat_id = m.chat.id
    await add_served_chat(chat_id)
    get = (await _.get_me())
    men = get.mention
    bot_id = get.id
    for x in m.new_chat_members:
        try:
            if x.id == bot_id:
                await m.reply_photo(PIC, caption=f"Thanks for having me in {m.chat.title}\n\n{men} is alive !\n\nFor queries : @NotKeshav")
        except:
            pass 

ALPHA = [5711561310, 5868832590]

@Client.on_message(filters.command("info") & filters.user(ALPHA))
async def info(_, m):
    if len(m.command) == 2:
        lel = int(m.text.split(None, 1)[1])
        if str(lel)[0] == "-":
            id = lel
        else:
            omfoo = "-" + str(lel)
            id = int(omfoo)

    getter = await _.get_chat(id)
    try:
        username = getter.username
    except:
        username = "None"
    try:
        link = getter.invite_link
    except:
        link = "None"
    await m.reply(f"Group name :- {getter.title}\n\nInvite link :- {link}\n\nUsername :- @{username}")
