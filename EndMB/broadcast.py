from pyrogram import Client as End, filters
from pyrogram.types import Message
from Database.users import list_chats
from EndMB.EndAll import ALPHA

@End.on_message(filters.command("broadcast") & filters.user(ALPHA))
async def brdcast(_, m):
    if m.reply_to_message:
        x = m.reply_to_message.message_id
        y = m.chat.id
    else:
        if len(m.command) < 2:
            return await m.reply_text(
                "**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]"
            )
        query = m.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = list_chats()
    for schat in schats:
        chats.append(schat.chat_id)
    for chat in chats:
        bot = await _.get_chat_member(chat, 5546726510)
        pin = bot.can_pin_messages 
        if m.reply_to_message:
            try:
                ok = await _.forward_messages(chat, y, x)
                sent += 1
                if pin:
                    await ok.pin()
            except:
                await m.reply("broadcast failed")
        else:
            try:
                ok = await _.send_message(chat, query)
                sent += 1
                if pin:
                    await ok.pin()
            except:
                await m.reply("broadcast failed")
    
    xD = str(sent)
    await m.reply(f"Broadcasted in {xD} chats")
    
        
