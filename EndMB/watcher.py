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
    msg = ""
    for i in chats:
        i = str(i)
        msg += f"\n<code>{i}</code>"
    await m.reply(f"**Served chats**\n\n{msg}\n**Count** :- {len(chats)}")

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
    await m.reply(f"**Served users**\n\n{msg}\n**Count** :- {len(chats)}")
