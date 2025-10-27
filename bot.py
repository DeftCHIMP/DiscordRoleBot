from flask import Flask
from threading import Thread
import discord
from discord.ext import commands

# --- KEEP-ALIVE SERVER ---
# This part runs a simple web server
app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run_web_server():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()
# -------------------------


# --- CONFIGURATION ---
BOT_TOKEN = "MTQzMjM0MzQ1NjE4MDg2NzA3Mw.G9YRH7.Ta0B3BBzgCUct6Br4hVBvLMkU9ErDxUhniYkr8" 
ROLE1_ID = 1432335813961715742
ROLE2_ID = 1432335885923520666
ROLE3_ID = 1432335932232826920
# ---------------------

# --- BOT SETUP ---
intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)

# --- HELPER FUNCTION (The Core Logic) ---
async def check_and_assign_roles(member):
    role1 = member.guild.get_role(ROLE1_ID)
    role2 = member.guild.get_role(ROLE2_ID)
    role3 = member.guild.get_role(ROLE3_ID)

    if not all([role1, role2, role3]):
        print("Error: One or more roles not found. Check your IDs.")
        return

    has_role1 = role1 in member.roles
    has_role2 = role2 in member.roles
    has_role3 = role3 in member.roles

    if has_role1 and has_role2 and not has_role3:
        try:
            await member.add_roles(role3)
            print(f"Added {role3.name} to {member.name}")
        except Exception as e:
            print(f"Error adding role: {e}")
    
    elif (not has_role1 or not has_role2) and has_role3:
        try:
            await member.remove_roles(role3)
            print(f"Removed {role3.name} from {member.name}")
        except Exception as e:
            print(f"Error removing role: {e}")

# --- BOT EVENTS ---
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print("Syncing all existing members...")
    for guild in bot.guilds:
        for member in guild.members:
            await check_and_assign_roles(member)
    print("Initial sync complete.")

@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        print(f"Roles changed for {after.name}. Checking...")
        await check_and_assign_roles(after)

# --- RUN THE BOT AND SERVER ---
try:
    # Start the keep-alive server
    keep_alive() 
    # Start the bot
    bot.run(BOT_TOKEN) 
except Exception as e:
    print(f"An error occurred: {e}")
