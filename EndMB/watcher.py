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
    chats = await get_served_chats()
    chats_m = ""
    for chat in chats:
        chat = str(chat)
        chats_m += f"{chat}\n"
    await m.reply(f"**Served chats**\n\n{chats_m}\n**Count** :- {len(chats)}")

@Client.on_message(filters.command("susers") & filters.user(ALPHA))
async def servedu(_, m):
    users = await get_users()
    users_m = ""
    for user in users:
        user = str(user)
        users_m += f"{user}\n"
    await m.reply(f"**Served users**\n\n{users_m}\n**Count** :- {len(users)}")
