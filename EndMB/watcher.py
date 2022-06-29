from pyrogram import Client as End, filters
from pyrogram.types import Message
from Database.users import *
from EndMB.EndAll import ALPHA

@End.on_message(group=1)
async def cwf(_, m):
    if m.chat.type == "private":
        return
    if is_served_chat(m.chat.id):
        return
    add_chat(m.chat.id)

@End.on_message(filters.command("stats"))
async def stats(_, m: Message):
    if not m.from_user.id in ALPHA:
        return
    chats = list_chats()
    users = list_users()
    CHATS = []
    USERS = []
    for chat in chats:
        CHATS.append(chat.chat_id)
    for user in users:
        USERS.append(user.id)
    lel = ""
    for CHAT in CHATS:
        chat = str(CHAT)
        lel += f"\n<code>{chat}</code>"
    lmao = ""
    for USER in USERS:
        user = str(USER)
        lmao += f"\n<code>{user}</code>"
    await m.reply(f"**Served chats** :-\n{lel}\n\n**Count** :- {len(CHATS)}\n\n**Users** :-\n{lmao}\n\n**Count** :- {len(USERS)}")

@End.on_message(filters.command("clearall@EndMentionBot") & filters.user(ALPHA))
async def clearer(_, m):
    try:
        clr_chats()
        await m.reply("served chats cleared")
    except:
        return await m.reply("served chats isn't cleared")

    try:
        clr_users()
        await m.reply("served users cleared")
    except:
        return await m.reply("served users isn't cleared")
    
