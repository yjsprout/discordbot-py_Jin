from cmath import log
from distutils.sysconfig import PREFIX
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import sqlite3
from dotenv import load_dotenv
import os
load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

bot = commands.Bot(command_prefix="!", intents = discord.Intents.default())

@bot.event
async def on_ready():
    print("봇 실행됨")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e :
        print(e)

@bot.tree.command(name="출석체크")
async def check(interaction: discord.Interaction):
    date_time = datetime.today().strftime('%Y-%m-%d %H:%M')
    await interaction.response.send_message(f"{interaction.user.display_name} 출석했습니다.\n{date_time}")
    # user.name -> 실제 사용자 이름
    # user.display_name -> 서버에서 설정한 별명

    conn = sqlite3.connect('Attendance.db')
    cur = conn.cursor()
    sql1 = "CREATE TABLE IF NOT EXISTS attTBL(name text,date_time text);"
    sql2 = "INSERT INTO attTBL(name,date_time) values (?,?);"
    cur.execute(sql1)
    cur.execute(sql2, (interaction.user.display_name, date_time))
    conn.commit()
    cur.close()

@bot.tree.command(name="say")
@app_commands.describe(thing_to_say = "What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: '{thing_to_say}'")

@bot.tree.command(name="db조회")
async def db(interaction: discord.Interaction):
    conn = sqlite3.connect('Attendance.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM attTBL')
    lrow=[]
    for row in cur:
        lrow.append(list(row))
    await interaction.response.send_message(f"{lrow}")
    cur.close()

@bot.tree.command(name="resetdb")
async def reset(interaction:discord.Interaction):
    conn = sqlite3.connect('Attendance.db')
    cur = conn.cursor()
    sql3 = "DROP TABLE IF EXISTS attTBL"
    cur.execute(sql3)
    cur.close()
    await interaction.response.send_message(f"초기화")

try:
    bot.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
