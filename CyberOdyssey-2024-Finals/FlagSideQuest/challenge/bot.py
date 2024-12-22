import os
from datetime import datetime, timedelta

import discord
import jwt
from Crypto.PublicKey import RSA
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from discord import app_commands


class DiscordBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = DiscordBot()

# Generate RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Get public key from private key
public_key = private_key.public_key()

# Convert to PEM format
PRIVATE_KEY = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')

PUBLIC_KEY = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

@client.tree.command(name="flag", description="Get the flag!")
async def flag(interaction: discord.Interaction):
    await interaction.response.send_message("nn hh")

@client.tree.command(name="start_adventure", description="Embark on a new adventure!")
async def start_adventure(interaction: discord.Interaction):
    user_data = {
        "id": interaction.user.id,
        "username": interaction.user.name,
        "type": "adventurer"
    }
    
    token = jwt.encode(
        payload={
            **user_data,
            'exp': datetime.now() + timedelta(minutes=1)
        },
        key=PRIVATE_KEY,
        algorithm='RS256'
    )
    
    await interaction.response.send_message(f"🎉 Your adventure token 🗝️: ```{token}```", ephemeral=True)

@client.tree.command(name="join_adventure", description="Join an epic quest to claim the flag!")
async def join_adventure(interaction: discord.Interaction, token: str):
    try:
        header = jwt.get_unverified_header(token)
        algorithm = header.get('alg', 'RS256')
        
        payload = jwt.decode(token, options={"verify_signature": False})
        pk = payload.get('pk')
        if pk is None:
            pk = PUBLIC_KEY
        
        # Check if the public key is valid and matches the server's key
        try:
            imported_key = RSA.import_key(pk)
            server_key = RSA.import_key(PUBLIC_KEY)
            if imported_key != server_key:
                raise Exception(f"❌ Does not match server's key!\n```{PUBLIC_KEY}```")
        except Exception as e:
            raise Exception(f"⚠️ Invalid public key - {e}")
        
        decoded = jwt.decode(token, pk, algorithms=[algorithm])
        
        msg = f"🏆 Adventure joined successfully! Welcome **{decoded['username']}** to the quest! 🌟"
        if decoded['type'] == 'master' and interaction.user.guild_permissions.administrator:
            msg += f"\n🎖️ Here is your flag: `{os.getenv('FLAG')}`"

        await interaction.response.send_message(msg, ephemeral=True)
    except jwt.ExpiredSignatureError:
        await interaction.response.send_message("⏳ Oops! Your token has expired!", ephemeral=True)
    except jwt.InvalidTokenError:
        await interaction.response.send_message("🚫 Invalid token! Try again!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"⚔️ An error occurred: {e}", ephemeral=True)

client.run(os.getenv("DISCORD_TOKEN"))
