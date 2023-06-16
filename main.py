from pyrogram import Client, filters
import os

# Set the temporary storage directory
TEMP_STORAGE = "./temp_storage"

# Create the temporary storage directory if it doesn't exist
if not os.path.exists(TEMP_STORAGE):
    os.makedirs(TEMP_STORAGE)

# Add your API ID, API Hash, and bot token here
API_ID = 14091414
API_HASH = "1e26ebacf23466ed6144d29496aa5d5b"
BOT_TOKEN = "5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo"
# config.py

ADMIN = [5500572462, 5205602399]


# Define the bot client
app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Handle the /rename command
@app.on_message(filters.command("rename") & filters.sudo)
async def rename_file(bot, message):
    if message.from_user.id not in ADMIN:
        await message.reply("You are not authorized to use this command.")
        return

    new_name = message.command[1]

    # Check if the message has a document or video
    if message.document or message.video:
        # Determine the file type (document or video)
        file_type = "document" if message.document else "video"

        # Get the file ID and file name
        file_id = message.document.file_id if message.document else message.video.file_id
        file_name = message.document.file_name if message.document else message.video.file_name

        # Download the file to the temporary storage directory
        file_path = os.path.join(TEMP_STORAGE, file_name)
        await bot.download_media(message=file_id, file_name=file_path)

        # Rename the file
        renamed_file_path = os.path.join(TEMP_STORAGE, new_name)
        os.rename(file_path, renamed_file_path)

        # Send the renamed file back to the user
        await bot.send_document(chat_id=message.chat.id, document=renamed_file_path)

        # Delete the temporary file
        os.remove(renamed_file_path)

    else:
        await message.reply("Please upload a document or video.")

# Start the bot
app.run(workers=200)
