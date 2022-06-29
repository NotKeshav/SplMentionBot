from pyrogram import Client as End, filters
from pyrogram.types import Message
from Database.users import list_chats
from EndMB.EndAll import ALPHA

@End.on_message(filters.command("broadcast") & filters.user(ALPHA))
async def brdcast(_, m):
    if message.reply_to_message:
        x = message.reply_to_message.message_id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]"
            )
        query = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = list_chats()
    for schat in schats:
        chats.append(schat.chat_id)
    for chat in chats:
        if m.reply_to_message:
            try:
                await _.forward_messages(chat, y, x)
                sent += 1
            except:
                await m.reply("broadcast failed")
        else:
            try:
                await _.send_message(chat, query)
                sent += 1
            except:
                await m.reply("broadcast failed")
    
    xD = str(sent)
    await m.reply(f"Broadcasted in {xD} chats")
    
        
