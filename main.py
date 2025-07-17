from pyrogram import Client, filters
import requests
import os
import asyncio

# Environment থেকে Config নিচ্ছি (Render বা অন্য যেকোন পরিবেশে environment variables সেট করতে হবে)
API_ID = int(os.environ.get("26410524"))
API_HASH = os.environ.get("e503790c6eec1397c2f580eef2123920")
BOT_TOKEN = os.environ.get("7602997776:AAF8w26cPg_91QvqXx1wC8nlaiW7ILRYD6c")
ALLOWED_GROUP = -1002842901553

bot = Client("sourcecode_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def format_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return "http://" + url
    return url

@bot.on_message(filters.group & filters.text & filters.chat(ALLOWED_GROUP))
async def get_source(client, message):
    text = message.text.lower().strip()

    if text.startswith("view "):
        url_raw = text.split(" ", 1)[1].strip()
        url = format_url(url_raw)

        loading_msg = await message.reply("🔄 Loading: 30%")
        await asyncio.sleep(1)
        await loading_msg.edit("🔄 Loading: 40%")
        await asyncio.sleep(1)
        await loading_msg.edit("🔄 Loading: 90%")
        await asyncio.sleep(1)
        await loading_msg.edit("✅ Loading: 100%")

        try:
            response = requests.get(url, timeout=10)
            html_content = response.text

            filename = url_raw.replace("https://", "").replace("http://", "").replace("/", "_").replace(".", "_") + ".html"
            filepath = f"/tmp/{filename}"

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)

            await loading_msg.edit(" ফাইল নিচে দেওয়া হলো 😅")
            await message.reply_document(document=filepath, caption=f"🌐 Source from: `{url}`", quote=True)
            os.remove(filepath)

        except Exception as e:
            await loading_msg.edit(f"❌ erro :\n`{str(e)}`")

@bot.on_message(filters.group & ~filters.chat(ALLOWED_GROUP))
async def reject_other_groups(client, message):
    await message.reply("❌ এই বট ব্যবহার করতে গেলে https://t.me/+yxoojuaOI0g4MWNl")

print("✅ Bot is running...")
bot.run()