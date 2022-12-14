from pyrogram import Client as End, filters
from pyrogram.types import Message
import os
import asyncio
from pyrogram import enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Database.Mongo.users import add_user, is_user
#
ALPHA = [5868832590]

S_P = "https://te.legra.ph/file/418fb2cb59a8a6017dd3c.jpg"

chatQueue = []

stopProcess = False

@End.on_message(filters.command(["tagall", "all"]) | filters.command("@all", ""))
async def everyone(client, message):
  global stopProcess
  try: 
    try:
      sender = await client.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if len(chatQueue) > 5:
        await message.reply("⛔️ | I'm already working on my maximum number of 5 chats at the moment. Please try again shortly.")
      else:  
        if message.chat.id in chatQueue:
          await message.reply("🚫 | There's already an ongoing process in this chat. Please /stop to start a new one.")
        else:  
          chatQueue.append(message.chat.id)
          if len(message.command) > 1:
            inputText = message.text.split(None, 1)[1]
          elif len(message.command) == 1:
            inputText = ""    
          membersList = []
          async for member in client.get_chat_members(message.chat.id):
            if member.user.is_bot == True:
              pass
            elif member.user.is_deleted == True:
              pass
            else:
              membersList.append(member.user)
          i = 0
          lenMembersList = len(membersList)
          if stopProcess: stopProcess = False
          while len(membersList) > 0 and not stopProcess :
            j = 0
            text1 = f"{inputText}\n\n"
            try:    
              while j < 10:
                user = membersList.pop(0)
                if user.username == None:
                  text1 += f"{user.mention} "
                  j+=1
                else:
                  text1 += f"@{user.username} "
                  j+=1
              try:     
                await client.send_message(message.chat.id, text1)
              except Exception:
                pass  
              await asyncio.sleep(10) 
              i+=10
            except IndexError:
              try:
                await client.send_message(message.chat.id, text1)  
              except Exception:
                pass  
              i = i+j
          if i == lenMembersList:    
            await message.reply(f"✅ | Successfully mentioned **total number of {i} members**.\n❌ | Bots and deleted accounts were rejected.") 
          else:
            await message.reply(f"✅ | Successfully mentioned **{i} members.**\n❌ | Bots and deleted accounts were rejected.")    
          chatQueue.remove(message.chat.id)
    else:
      await message.reply("👮🏻 | Sorry, **only admins** can execute this command.")  
  except FloodWait as e:
    await asyncio.sleep(e.value) 

@End.on_message(filters.command(["remove", "clean"]))
async def remove(client, message):
  global stopProcess
  try: 
    try:
      sender = await client.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      bot = await client.get_chat_member(message.chat.id, "self")
      if bot.status == ChatMemberStatus.MEMBER:
        await message.reply("🕹 | I need admin permissions to remove deleted accounts.")  
      else:  
        if len(chatQueue) > 5 :
          await message.reply("⛔️ | I'm already working on my maximum number of 5 chats at the moment. Please try again shortly.")
        else:  
          if message.chat.id in chatQueue:
            await message.reply("🚫 | There's already an ongoing process in this chat. Please /stop to start a new one.")
          else:  
            chatQueue.append(message.chat.id)  
            deletedList = []
            async for member in client.get_chat_members(message.chat.id):
              if member.user.is_deleted == True:
                deletedList.append(member.user)
              else:
                pass
            lenDeletedList = len(deletedList)  
            if lenDeletedList == 0:
              await message.reply("👻 | No deleted accounts in this chat.")
              chatQueue.remove(message.chat.id)
            else:
              k = 0
              processTime = lenDeletedList*10
              temp = await client.send_message(message.chat.id, f"🚨 | Total of {lenDeletedList} deleted accounts has been detected.\n⏳ | Estimated time: {processTime} seconds from now.")
              if stopProcess: stopProcess = False
              while len(deletedList) > 0 and not stopProcess:   
                deletedAccount = deletedList.pop(0)
                try:
                  await client.ban_chat_member(message.chat.id, deletedAccount.id)
                except Exception:
                  pass  
                k+=1
                await asyncio.sleep(10)
              if k == lenDeletedList:  
                await message.reply(f"✅ | Successfully removed all deleted accounts from this chat.")  
                await temp.delete()
              else:
                await message.reply(f"✅ | Successfully removed {k} deleted accounts from this chat.")  
                await temp.delete()  
              chatQueue.remove(message.chat.id)
    else:
      await message.reply("👮🏻 | Sorry, **only admins** can execute this command.")  
  except FloodWait as e:
    await asyncio.sleep(e.value)                               
        
@End.on_message(filters.command(["stop", "cancel"]))
async def stop(client, message):
  global stopProcess
  try:
    try:
      sender = await client.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if not message.chat.id in chatQueue:
        await message.reply("🤷🏻‍♀️ | There is no ongoing process to stop.")
      else:
        stopProcess = True
        await message.reply("🛑 | Stopped.")
    else:
      await message.reply("👮🏻 | Sorry, **only admins** can execute this command.")
  except FloodWait as e:
    await asyncio.sleep(e.value)

@End.on_message(filters.command(["admins", "staff"]) | filters.command(["@admin", "@admins"], ""))
async def admins(client, message):
  try: 
    adminList = []
    ownerList = []
    async for admin in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
      if admin.privileges.is_anonymous == False:
        if admin.user.is_bot == True:
          pass
        elif admin.status.name == "OWNER":
          ownerList.append(admin.user)
        else:  
          adminList.append(admin.user)
      else:
        pass   
    lenAdminList= len(ownerList) + len(adminList)  
    text2 = f"**GROUP STAFF - {message.chat.title}**\n\n"
    try:
      owner = ownerList[0]
      if owner.username == None:
        text2 += f"👑 Owner\n└ {owner.mention}\n\n👮🏻 Admins\n"
      else:
        text2 += f"👑 Owner\n└ @{owner.username}\n\n👮🏻 Admins\n"
    except:
      text2 += f"👑 Owner\n└ <i>Hidden</i>\n\n👮🏻 Admins\n"
    if len(adminList) == 0:
      text2 += "└ <i>Admins are hidden</i>"  
      await client.send_message(message.chat.id, text2)   
    else:  
      while len(adminList) > 1:
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"├ {admin.mention}\n"
        else:
          text2 += f"├ @{admin.username}\n"    
      else:    
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"└ {admin.mention}\n\n"
        else:
          text2 += f"└ @{admin.username}\n\n"
      text2 += f"✅ | **Total number of admins**: {lenAdminList}\n❌ | Bots and hidden admins were rejected."  
      await client.send_message(message.chat.id, text2)           
  except FloodWait as e:
    await asyncio.sleep(e.value)       

@End.on_message(filters.command(["bots"]))
async def bots(client, message):  
  try:    
    botList = []
    async for bot in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
      botList.append(bot.user)
    lenBotList = len(botList) 
    text3  = f"**BOT LIST - {message.chat.title}**\n\n🤖 Bots\n"
    while len(botList) > 1:
      bot = botList.pop()
      text3 += f"├ @{bot.username}\n"  
    else:    
      bot = botList.pop()
      text3 += f"└ @{bot.username}\n\n"
      text3 += f"✅ | **Total number of bots**: {lenBotList}"  
      await client.send_message(message.chat.id, text3)
  except FloodWait as e:
    await asyncio.sleep(e.value)

uname = None
name = None
@End.on_message(filters.command("start") & filters.private)
async def start(client, message):
    global uname, name
    if not name:
        name = (await client.get_me()).first_name
    if not uname:
        uname = (await client.get_me()).username
    START_MARKUP = [
    [
    InlineKeyboardButton("➕ Add to your chat ➕", url=f"t.me/{uname}?startgroup=true")
    ]
    ]
    try:
        is_user = await is_user(message.from_user.id)
    except:
        pass
    try:
        if not is_user:
            await add_user(message.from_user.id)
    except:
        pass
    text = f'''
Heya {message.from_user.mention},\n
My name is **{name}**, belongs to @Spoiled_Community. I'm here to help you to get everyone's attention by mentioning all members in your chat.\n
I have some additional cool features and also I can work in channels.\n
Don't forget to join my channel to recieve information on all the latest updates.\n
Hit /help to find out my commands and the use of them.
'''
    await client.send_photo(message.chat.id, S_P, caption=text, reply_markup=InlineKeyboardMarkup(START_MARKUP))


@End.on_message(filters.command("help"))
async def help(client, message):
    text = '''
let's have a quick look at my commands.\n
**Commands**:\n
- /all "input": <i>Mention all members.</i>
- /remove: <i>Remove all deleted accounts.</i>
- /admins: <i>Mention all admins.</i>
- /bots: <i>Get the full bot list.</i>
- /stop: <i>Stop an on going process.</i>\n
If you have any questions on how to use me, feel free to ask @NotKeshav.
'''
    await client.send_message(message.chat.id, text, disable_web_page_preview=True)
