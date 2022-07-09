from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("alive"))
async def hehe(_, m):
    if m.from_user.id == 1927705508:
        await m.reply("yes! Am alive owner 🤧")
