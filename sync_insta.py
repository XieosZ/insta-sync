import os
import shutil
import time
import random
import re
import logging
from instaloader import Instaloader, Profile
from instagrapi import Client
from config import TARGET_USER, MY_USER, MY_PASS, DUMMY_USER, DUMMY_PASS

# Set up logging
logging.basicConfig(
    filename='insta_sync.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# File to track posted shortcodes
POSTED_IDS_FILE = 'posted_ids.txt'
SESSION_FILE = 'session.json'

def load_posted_ids():
    if os.path.exists(POSTED_IDS_FILE):
        with open(POSTED_IDS_FILE, 'r') as f:
            return set(line.strip() for line in f)
    return set()

def save_posted_ids(posted_ids):
    with open(POSTED_IDS_FILE, 'w') as f:
        for shortcode in posted_ids:
            f.write(shortcode + '\n')

def login_to_account(client, username, password):
    if os.path.exists(SESSION_FILE):
        client.load_settings(SESSION_FILE)
        try:
            client.get_timeline_feed()  # Test if session is still valid
            print("Session loaded from file.")
        except Exception:
            print("Session expired. Logging in again...")
            client.login(username, password)
            client.dump_settings(SESSION_FILE)
    else:
        client.login(username, password)
        client.dump_settings(SESSION_FILE)

def main():
    logging.info("Starting Instagram sync script")
    # Load already posted shortcodes
    posted_ids = load_posted_ids()

    # Initialize Instaloader
    loader = Instaloader()

    try:
        # Get target profile (with retry logic)
        profile = None
        try:
            profile = Profile.from_username(loader.context, TARGET_USER)
        except Exception as e:
            print(f"Failed to fetch profile anonymously: {e}")
            if DUMMY_USER and DUMMY_PASS:
                print("Trying with dummy account...")
                loader.login(DUMMY_USER, DUMMY_PASS)
                profile = Profile.from_username(loader.context, TARGET_USER)
            else:
                print("No dummy account configured. Retrying in 60 seconds...")
                time.sleep(60)
                profile = Profile.from_username(loader.context, TARGET_USER)

        # Get latest 3 posts (limit volume to prevent shadow-bans)
        posts = list(profile.get_posts())[:3]

        # Initialize Instagrapi client
        client = Client()
        login_to_account(client, MY_USER, MY_PASS)

        for post in posts:
            shortcode = post.shortcode
            if shortcode in posted_ids:
                continue

            print(f"Processing new post: {shortcode}")

            # Download the post
            loader.download_post(post, target=profile.username)

            # Path to downloaded folder
            download_dir = os.path.join(profile.username, shortcode)

            try:
                # Read caption from .txt file
                caption_file = os.path.join(download_dir, f"{shortcode}.txt")
                if os.path.exists(caption_file):
                    with open(caption_file, 'r', encoding='utf-8') as f:
                        caption = f.read().strip()
                    # Sanitize caption: replace mentions of target account with uploader account
                    caption = re.sub(r'@' + re.escape(TARGET_USER), f'@{MY_USER}', caption, flags=re.IGNORECASE)
                    # Add unique elements to avoid duplicate content filters
                    emojis = ['❤️', '🔥', '✨', '🌟', '💫', '🎉', '😊', '👍', '👏', '💯']
                    random_emoji = random.choice(emojis)
                    caption += f"\n\nCredit: @{TARGET_USER} {random_emoji}"
                else:
                    caption = ""

                # Find media file
                media_path = None
                for file in os.listdir(download_dir):
                    if file.endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov')):
                        media_path = os.path.join(download_dir, file)
                        break

                if media_path is None:
                    print(f"No media found for {shortcode}")
                    continue

                # Upload based on type
                if media_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                    client.photo_upload(media_path, caption)
                elif media_path.lower().endswith(('.mp4', '.mov')):
                    # Use reels_upload for videos to ensure they appear in Reels tab
                    client.reels_upload(media_path, caption)
                else:
                    print(f"Unsupported media type for {shortcode}")
                    continue

                print(f"Successfully uploaded {shortcode}")
                logging.info(f"Successfully uploaded {shortcode}")

                # Add to posted ids
                posted_ids.add(shortcode)
                save_posted_ids(posted_ids)

            except Exception as e:
                print(f"Failed to upload {shortcode}: {e}")
                logging.error(f"Failed to upload {shortcode}: {e}")

            finally:
                # Ensure cleanup happens regardless of success or failure
                if os.path.exists(download_dir):
                    shutil.rmtree(download_dir)
                    logging.info(f"Cleaned up temporary files for {shortcode}")

            # Add random delay between posts to appear more human
            time.sleep(random.uniform(30, 60))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
