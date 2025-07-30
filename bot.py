from share import *
from src.sports.football import football
import reaction_role
from discord import app_commands
from loop import *
import src.sports.counterstrike.vani_link_chekcer as link_checker
import src.sports.counterstrike.GetPlayerInfo.cs2_match_stats as cs2_match_stats
import src.sports.f1.f1 as formula1
from src.logs import get_logs
from src.get_settings import read_settings_file as settings
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
   

#region sportsCommands
def has_owner_role(interaction: discord.Interaction) -> bool:
    return any(role.name.lower() == "owner" for role in interaction.user.roles)

@client.tree.command(name="football", description="Scrape football matches")
async def football(interaction: discord.Interaction):
    if not has_owner_role(interaction):
        return
    await interaction.response.send_message("Scraping football matches...")
    await Football.scrape_matches()


@client.tree.command(name="cs", description="Scrape Counter-Strike matches")
async def cs(interaction: discord.Interaction):
    if not has_owner_role(interaction):
        return
    await interaction.response.send_message("Scrape Counter-Strike matches...")
    await counter_strike.show_info()

@client.tree.command(name="f1", description="Scrape F1 matches")
async def f1(interaction: discord.Interaction):
    if not has_owner_role(interaction):
        return
    await interaction.response.send_message("Scraping F1 matches...")
    await formula1.scrape_matches()

@client.tree.command(name="clear", description="Clear a number of messages from the channel")
@app_commands.describe(amount="Number of messages to delete (default 50)")
async def clear(interaction: discord.Interaction, amount: int = 50):
    if not has_owner_role(interaction):
        return
    await interaction.response.send_message(f"Clearing {amount} messages...")
    await interaction.channel.purge(limit=amount)

@client.tree.command(name="logs", description="Get logs")

async def logs(interaction: discord.Interaction):
    if not has_owner_role(interaction):
        return
    allowed_channel_id = settings("logsID")  
    if interaction.channel.id != allowed_channel_id:
        await interaction.response.send_message(
            "❌", 
            ephemeral=True
        )
        return
    await interaction.response.send_message(f"getting logs",delete_after=1)
    await get_logs()
    
async def get_numbers_of_ID(accounts,interaction):
    if(len(accounts)>10):
        await interaction.response.send_message("You can´t have that many id´s", ephemeral=True)
        return False
    else:
        return True
    

@client.tree.command(name="csstats", description="Get information about cs2 players")
@app_commands.describe(player_id="Players id")
async def csstats(interaction: discord.Interaction, player_id: str):
    allowed_channel_id = settings("playerLookUpID")  
    
    if interaction.channel.id != allowed_channel_id:
        await interaction.response.send_message(
            "❌ This command can only be used in the designated channel: " +"cs2-player-lookup", 
            ephemeral=True
        )
        return
    accounts =  player_id.split(" ")
    if(await get_numbers_of_ID(accounts,interaction)):
        await interaction.response.send_message("Getting data...", ephemeral=True)
        for element in accounts:
            player_id_after_vanity = await link_checker.check_if_link_is_64(element)
            if(player_id_after_vanity == None):
                await interaction.followup.send("Enter a valid steam ID",ephemeral=True)
                return
            
            data = await cs2_match_stats.get_info(player_id_after_vanity)
            await interaction.followup.send(embed=data, ephemeral=True)

    
#endregion

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
        twitch_loop.start()
    )
    
            
def main():
    client.run(discord_token,log_handler=handler, log_level=logging.ERROR)
    
if __name__=="__main__": 
    main() 
