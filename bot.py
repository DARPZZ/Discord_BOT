from share import *
import reaction_role
from loop import *
import src.commands.counterstrike_commands as counterstrike_commands
import src.commands.essentials as essentials
import src.commands.loop_commands as loop_commands
load_dotenv() 
discord_token = os.getenv("discord_token")
intents.message_content = True
intents.members = True
import logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
@client.event
async def on_ready():
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands to test guild.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    await loop_start()
    
    
@client.event
async def on_member_join(member): 
  role = discord.utils.get(member.guild.roles, name="Medlem")
  await member.add_roles(role)
    
async def loop_start():
    await asyncio.gather(
        start_football_loop.start(),
        start_Ufc_loop.start(),
        start_f1_loop.start(),
        start_f1_driver_team_loop.start(),
        start_counterstrike_loop.start(),
        twitch_loop.start(),
        start_valorant_loop.start(),
        start_counterstrike_tournament_loop.start(),
        start_football_premierleague_table.start(),
        start_nfl_loop.start(),
    )
            
def main():
    client.run(discord_token,log_handler=handler, log_level=logging.ERROR)
    
if __name__=="__main__": 
    main() 
