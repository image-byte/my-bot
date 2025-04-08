import requests
import re
import time

# Config
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
GUILD_ID = "YOUR_SERVER_ID_HERE"
CHANNEL_IDS = []  # Optional: Restrict to specific channels

headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}

def fetch_messages(channel_id):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=100"
    response = requests.get(url, headers=headers)
    return response.json()

def delete_message(channel_id, message_id):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}"
    requests.delete(url, headers=headers)

def block_links():
    while True:
        try:
            # Get all channels in the server
            channels = requests.get(
                f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels",
                headers=headers
            ).json()

            for channel in channels:
                if CHANNEL_IDS and channel["id"] not in CHANNEL_IDS:
                    continue  # Skip if channel not in allowlist

                messages = fetch_messages(channel["id"])
                for msg in messages:
                    if msg["author"]["bot"]:
                        continue  # Ignore bots

                    # Block ANY link (HTTP/HTTPS/WWW/DOMAINS)
                    if re.search(
                        r'(https?://|www\.|\.(com|net|org|gg|xyz|io))',
                        msg["content"],
                        re.IGNORECASE
                    ):
                        delete_message(channel["id"], msg["id"])
                        print(f"Deleted link from {msg['author']['username']}")

        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    block_links()
