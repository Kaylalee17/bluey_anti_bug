from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv, PairStatusEv
from time import sleep
import threading
import os
import random
import logging
logging.basicConfig(filename="worker.log", level=logging.INFO, format="%(asctime)s %(message)s")

SESSION_FILE = "/data/bot.sqlite3"
PHONE = "2348129982887"

first_time = not os.path.exists(SESSION_FILE)  # check BEFORE making client
client = NewClient(SESSION_FILE)

@client.event(ConnectedEv)
def on_connected(client, event):
    print("Connected ✅")

@client.event(PairStatusEv)
def on_pair(client, event):
    print("Paired ✅")


#=== READING IMAGE === 
with open("krypt.jpeg", "rb") as f:
    image = f.read()

#=== BOT MESSAGES ===

words = [
    "*Every system has a crack. I just happen to speak its language.*",
    "*They see a screen. I see a door nobody locked right. I'm KRYPT type !menu to see what i can do.*",
    "*Not here to break things for fun. Here to prove I understand them better than the people who built them.*",
    "*Behind every firewall is someone who thought ‘good enough’ — I don’t do good enough.*",
    "*I don’t chase ghosts in the machine. I become one.*",
    "*Patience isn’t weakness. It’s watching the pattern until it breaks itself.*",
    "*I don’t need permission to understand how something works. I need time.*",
    "*Every password is a story someone thought was clever enough.*",
    "*he quiet ones in the room are usually the ones who already found the exploit.*"
      ]
watermark = "> © ᴍᴀᴅᴇ ʙʏ ʙʟᴀᴄᴋғᴏx"
menu_message = f'''
⬡═―—⊱ [ Ｋ𝕽Y͜͡『PŤ  ｖ𝟷 ] ⊰―—═⬡
╔═══════════════╗
𓆣  Dᴇᴠᴇʟᴏᴘᴇʀ ❄ ʙʟᴜᴇʏ🥋
𓆣  ᴘʟᴀᴛғᴏʀᴍ ❄ Wʜᴀᴛsᴀᴘᴘ 🪀
𓆣  Pᴜʀᴘᴏsᴇ ❄ ᴀɴᴛɪ-ʙᴜɢ 
𓆣  Sᴛᴀᴛᴜs ❄ ᴏɴʟɪɴᴇ
➤ *prifix: !*
╚═══════════════╝
'''

def message(client, event):
    chat_jid = event.Info.MessageSource.Chat
    mixed = random.choice(words)
    caption = f'''
{menu_message}
\n{mixed}
\n{watermark}
'''
    img_msg = client.build_image_message(image, caption=caption)
    client.send_message(chat_jid, message=img_msg)


    
@client.event(MessageEv)
def on_message(client, event):
    logging.info(f"Received message from {event.Info.MessageSource.Sender}")
    text = event.Message.conversation or getattr(event.Message.extendedTextMessage, "text", "") or ""
    if "krypt" in text.lower():
        message(client, event)
if __name__ == "__main__":
    threading.Thread(target=client.connect, daemon=True).start()

    if first_time:
        for _ in range(10):
            sleep(3)
            try:
                print("Pairing code:", client.PairPhone(PHONE, show_push_notification=True))
                break
            except Exception as e:
                print("Retrying...", e)

    while True:
        sleep(1)
