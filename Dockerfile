
FROM python:3.11-slim

WORKDIR /usr/src/app

# Install yt-dlp dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code
COPY . .

CMD ["python", "bot.py"]