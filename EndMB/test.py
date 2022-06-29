from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("lmao"))
async def lmao(_, m):
    if m.reply_to_message:
        x = m.reply_to_message.message_id
        y = m.chat.id
        z = -1001604656390
        await _.forward_messages(z, y, x)
