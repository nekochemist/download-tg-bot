# XInstDL

A fast and elegant Telegram bot for downloading media from multiple platforms. Simply send a link and get the video delivered straight to your Telegram chat!

## Features

- **Multi-platform support**: Download from YouTube, Instagram, X (Twitter), TikTok, Facebook, and [many more platforms](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
- **Fast downloads**: Powered by `yt-dlp` for efficient media extraction
- **Easy to use**: Just send a link to the bot
- **Clean**: Automatically cleans up temporary files after upload
- **Rich metadata**: Includes video titles in the response
- **Error handling**: Graceful handling of private, invalid, or unsupported links
- **File size check**: Warns if video exceeds Telegram's 50MB limit

## Quick Start

### Prerequisites

- Python 3.8 or higher
- ffmpeg (for video processing)
- A Telegram Bot Token (get one from [@BotFather](https://t.me/botfather))

### Installation

1. Clone the repository:

```bash
git clone https://github.com/sra0ne/xinstdl.git
cd xinstdl
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your Telegram Bot Token:

```env
BOT_TOKEN=your_telegram_bot_token_here
```

4. Start the bot:

```bash
python bot.py
```

### Docker Deployment

Alternatively, you can run the bot using Docker:

```bash
docker build -t xinstdl .
docker run -e BOT_TOKEN=your_telegram_bot_token_here xinstdl
```

## Usage

1. Start a chat with your bot on Telegram
2. Send any supported platform link (YouTube, Instagram, X/Twitter, TikTok, etc.)
3. Wait for the bot to process and download the media
4. Receive the video directly in your chat!

### Supported Platforms

This bot uses yt-dlp, which supports **1800+ sites**, including:

- **YouTube**: Videos, Shorts, Playlists
- **Instagram**: Posts, Reels, Stories, IGTV
- **X (Twitter)**: Tweets with videos
- **TikTok**: Videos
- **Facebook**: Public videos
- **Vimeo**: Videos
- **Dailymotion**: Videos
- **Reddit**: Videos
- And many more! See the full list at [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

### Dependencies

- [**python-telegram-bot**](https://github.com/python-telegram-bot/python-telegram-bot): Modern Telegram Bot API framework
- [**yt-dlp**](https://github.com/yt-dlp/yt-dlp): Feature-rich command-line program to download videos
- **ffmpeg**: For video processing and format conversion

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This bot is for educational and personal use only. Please respect the terms of service of the platforms when using this tool. The authors are not responsible for any misuse of this software.

## Demo

<img width="600" height="600" alt="image" src="image.png" />

Made with ❤️ by [sra0ne](https://github.com/sra0ne)
