import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import yt_dlp

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN')


def get_video_info(url: str) -> dict:
    """Extract video information using yt-dlp."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info.get('title', 'Unknown'),
            'duration': info.get('duration', 0),
            'thumbnail': info.get('thumbnail', None),
            'url': info.get('url', url),
            'ext': info.get('ext', 'mp4'),
            'formats': info.get('formats', [])
        }


def download_video(url: str, output_path: str) -> str:
    """Download video using yt-dlp and return the file path."""
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
        'merge_output_format': 'mp4',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Find the downloaded file
    if os.path.exists(output_path):
        return output_path
    
    # If exact path doesn't exist, try to find the file with extension
    base_path = output_path.split('.')[0]
    for ext in ['mp4', 'webm', 'mkv', 'avi']:
        test_path = f"{base_path}.{ext}"
        if os.path.exists(test_path):
            return test_path
    
    raise FileNotFoundError(f"Downloaded file not found at {output_path}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages containing URLs."""
    url = update.message.text.strip()
    
    # Basic URL validation
    if not (url.startswith('http://') or url.startswith('https://')):
        await update.message.reply_text(
            "❌ Please send a valid URL.\n"
            "This bot supports YouTube, Instagram, Twitter/X, TikTok, Facebook, "
            "and many other platforms supported by yt-dlp."
        )
        return
    
    # Send waiting message
    waiting_message = await update.message.reply_text(
        "🔍 Fetching video information... Please wait."
    )
    
    downloaded_file_path = None
    
    try:
        # Get video info first
        logger.info(f"Processing URL: {url}")
        video_info = await asyncio.to_thread(get_video_info, url)
        title = video_info['title']
        
        # Update waiting message with title
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=waiting_message.message_id,
            text=f"📥 Downloading: {title[:50]}{'...' if len(title) > 50 else ''}\n"
                 f"Platform: Supported by yt-dlp\n"
                 f"Please wait..."
        )
        
        # Create temp file path
        temp_filename = f"{hash(url) % 1000000}.mp4"
        output_path = os.path.join(os.getcwd(), temp_filename)
        
        # Download the video
        downloaded_file_path = await asyncio.to_thread(download_video, url, output_path)
        logger.info(f"Download completed: {downloaded_file_path}")
        
        # Notify user about download completion
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=waiting_message.message_id,
            text=f"✅ Download complete! Uploading to Telegram..."
        )
        
        # Check file size (Telegram limit is 50MB for bots)
        file_size = os.path.getsize(downloaded_file_path)
        if file_size > 50 * 1024 * 1024:
            await update.message.reply_text(
                "⚠️ The video is too large (>50MB) to upload to Telegram.\n"
                "Consider using a premium bot or downloading directly."
            )
            return
        
        # Send video to user
        with open(downloaded_file_path, 'rb') as video_file:
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=video_file,
                caption=title,
                read_timeout=600,
                write_timeout=600
            )
        
        logger.info("Upload completed")
        
        # Delete waiting message
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=waiting_message.message_id
        )
        
    except Exception as err:
        logger.error(f"Error processing video: {err}", exc_info=True)
        await update.message.reply_text(
            "❌ Failed to process the video. The link might be:\n"
            "- Invalid\n"
            "- Private/Restricted\n"
            "- Unsupported by yt-dlp\n\n"
            "Please try another link."
        )
        # Try to delete waiting message if it still exists
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=waiting_message.message_id
            )
        except:
            pass
    finally:
        # Cleanup downloaded file
        if downloaded_file_path and os.path.exists(downloaded_file_path):
            try:
                os.remove(downloaded_file_path)
                logger.info(f"🧹 Cleaned up file: {downloaded_file_path}")
            except Exception as cleanup_err:
                logger.error(f"Error cleaning up file: {cleanup_err}")


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the Bot
    logger.info("🚀 Telegram Bot starting...")
    asyncio.run(application.run_polling(allowed_updates=Update.ALL_TYPES))


if __name__ == '__main__':
    main()
