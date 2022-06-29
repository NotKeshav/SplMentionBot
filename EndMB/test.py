from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("lmao"))
async def lmao(_, m):
    if m.reply_to_message and len(m.command) == 2:
        x = m.reply_to_message.message_id
        y = m.chat.id
        z = m.int(text.split(None, 1)[1])
        await _.forward_messages(z, y, x)
