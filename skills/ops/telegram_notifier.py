#!/usr/bin/env python3
"""
Telegram notification helper for ops monitoring skill.
Reads credentials from environment variables:
- TELEGRAM_BOT_TOKEN: Your bot token from @BotFather
- TELEGRAM_CHAT_ID: Your chat ID (can get from @userinfobot)
"""
import os
import sys
import requests
from typing import Optional

def send_telegram_message(message: str) -> bool:
    """
    Send a message via Telegram bot.
    Returns True if successful, False otherwise.
    """
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')

    if not bot_token or not chat_id:
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to send Telegram message: {e}", file=sys.stderr)
        return False

def is_telegram_configured() -> bool:
    """Check if Telegram credentials are configured."""
    return bool(os.environ.get('TELEGRAM_BOT_TOKEN') and os.environ.get('TELEGRAM_CHAT_ID'))

if __name__ == "__main__":
    # Test mode
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        if send_telegram_message(message):
            print("Message sent successfully!")
        else:
            print("Failed to send message. Check your environment variables.")
    else:
        if is_telegram_configured():
            print("Telegram is configured and ready!")
        else:
            print("Telegram not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
