import datetime
import tweepy
import time
import pyAesCrypt
import sys
import random
import os

# Replace with your Twitter API v2 Bearer Token
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAAHV0QEAAAAAvqOT2Gq17%2BEt1LfrrQ68WqDcUGU%3DDR5Uznre24hXn9C5g2g38tRmMOo4OiItf7TSClMiNRFbsaxOnB'

# Set up Tweepy client (API v2)
client = tweepy.Client(bearer_token=bearer_token)

def FirePayload(filePath, encryptPass):
    print("\n⚠️ ACTIVATED PAYLOAD ⚠️")
    bufferSIZE = 64 * 1024

    try:
        # Encrypt the file
        pyAesCrypt.encryptFile(filePath, filePath + '.aes', encryptPass, bufferSIZE)
        print("🔐 File successfully encrypted.")

        # Delete the original file
        os.remove(filePath)
        print("🗑️ Original file deleted securely.")

    except Exception as e:
        print(f"❌ Error during payload execution: {e}")

    print("🔒 LOCKDOWN MODE COMPLETE. Exiting now.")
    sys.exit()

def CheckKey(username, keyword, baseDelay, filePath, encryptPass, targetTime):
    print(f"\n🔍 Monitoring @{username} for keyword '{keyword}'...\n")

    retry_delay = baseDelay
    max_backoff = 300  # 5 minutes

    while True:
        time_left = int(targetTime - time.time())

        if time_left <= 0:
            FirePayload(filePath, encryptPass)

        print(f"🕒 Time left: {time_left} seconds | Next check in: {retry_delay}s")

        try:
            # Get user ID
            user = client.get_user(username=username)
            user_id = user.data.id

            # Fetch recent tweets
            tweets = client.get_users_tweets(id=user_id, max_results=100)

            if tweets.data:
                for tweet in tweets.data:
                    if keyword.lower() in tweet.text.lower():
                        print("✅ Deadswitch De-Activated — Safe Mode Engaged.")
                        sys.exit()

            # No keyword found — reset retry delay
            print("❌ Keyword not found — waiting before next check...\n")
            retry_delay = baseDelay
            time.sleep(retry_delay)

        except tweepy.TooManyRequests as e:
            reset_time = int(e.response.headers.get("x-rate-limit-reset", time.time() + 900))
            wait_time = reset_time - int(time.time())
            wait_time = max(wait_time, retry_delay)

            if time.time() + wait_time >= targetTime:
                print("🚨 Rate limit wait would exceed switch deadline — triggering payload.")
                FirePayload(filePath, encryptPass)

            print(f"🚦 Rate limit hit. Backing off for {wait_time} seconds...\n")
            time.sleep(wait_time + random.randint(1, 10))
            retry_delay = min(retry_delay * 2, max_backoff)

        except tweepy.TweepyException as e:
            print(f"⚠️ Twitter error: {e}")
            retry_delay = min(retry_delay * 2, max_backoff)
            print(f"⏳ Retrying in {retry_delay} seconds...\n")
            time.sleep(retry_delay)

def GetTargets():
    while True:
        startTime = input("📅 Date to start searching from (YYYY-MM-DD):\n> ").strip()
        try:
            datetime.datetime.strptime(startTime, '%Y-%m-%d')
            break
        except ValueError:
            print("❗ Invalid date format. Try again.")

    keyword = input("🔑 Keyphrase to disarm switch?\n> ").strip()
    username = input("👤 Twitter account to monitor?\n> ").strip()
    baseDelay = int(input("⏱️ Time (in seconds) between checks? (Recommended: ≥ 60)\n> "))
    filePath = input("📄 Path to file that will be encrypted?\n> ").strip()
    encryptPass = input("🔐 Password to encrypt file?\n> ").strip()
    minutes = int(input("⏳ How many minutes before firing the switch?\n> "))
    targetTime = time.time() + (minutes * 60)

    print("\n✅ Setup complete. Monitoring started...\n")
    CheckKey(username, keyword, baseDelay, filePath, encryptPass, targetTime)

GetTargets()
