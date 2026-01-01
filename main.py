# This example requires the 'message_content' intent.

import os
import discord
from twilio.rest import Client

# ------------------- Twilio Setup -------------------
account_sid = os.environ["TWILIO_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

client_twilio = Client(account_sid, auth_token)

twilio_whatsapp_number = "whatsapp:" + os.environ["TWILIO_WHATSAPP_NUMBER"]
my_whatsapp_number = "whatsapp:" + os.environ["MY_WHATSAPP_NUMBER"]

def send_whatsapp_message(msg):
    client_twilio.messages.create(
        body=msg,
        from_=twilio_whatsapp_number,
        to=my_whatsapp_number
    )

# ------------------- Discord Bot Setup -------------------
intents = discord.Intents.default()
intents.message_content = True

target_id = int(os.environ["TARGET_ID"])
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.id != int(os.environ["TARGET_ID"]):
        return

    for embed in message.embeds:
        if not embed.title or "Current Normal Stocks" not in embed.title:
            continue

        if not embed.description:
            continue

        lines = embed.description.split("\n")
        fruits = []

        for line in lines:
            if "**" in line:
                fruit = line.split("**")[1].strip()
                fruits.append(fruit)

        if not fruits:
            return

        # ---- Build single beautiful box message ----
        box_msg = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        box_msg += "🍉 *CURRENT NORMAL STOCKS* 🍉\n"
        box_msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        emoji_map = {
            "Light": "🟢",
            "Smoke": "🟤",
            "Love": "💖"
        }

        for fruit in fruits:
            emoji = emoji_map.get(fruit, "🔹")
            box_msg += f"{emoji} {fruit}\n"

        box_msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        # Add Love alert if present
        if "kitsune" in fruits:
            box_msg += "🔥 *ALERT: kitsune on stock!* 🔥\n"

        box_msg += "⏰ Stock updates live\n"
        box_msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        send_whatsapp_message(box_msg)


# ------------------- Run the bot -------------------
client.run(os.environ["DISCORD_TOKEN"])
