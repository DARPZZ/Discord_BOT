from share import *
from src.Sports.Football import Football
import reaction_role
from discord import app_commands
from loop import *
import src.Sports.CounterStrike.GetPlayerInfo.cs2_match_stats as cs2_match_stats
load_dotenv() 
discord_token = os.getenv("discord_token")
intents.message_content = True
intents.members = True



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
    await CounterStrike.scrape_matches()

@client.tree.command(name="f1", description="Scrape F1 matches")
async def f1(interaction: discord.Interaction):
    if not has_owner_role(interaction):
        return

    await interaction.response.send_message("Scraping F1 matches...")
    await F1.F1.scrape_matches()

@client.tree.command(name="clear", description="Clear a number of messages from the channel")
@app_commands.describe(amount="Number of messages to delete (default 50)")
async def clear(interaction: discord.Interaction, amount: int = 50):
    if not has_owner_role(interaction):
        return
    await interaction.response.send_message(f"Clearing {amount} messages...")
    await interaction.channel.purge(limit=amount)
    
    
@client.tree.command(name="csstats", description="Get information about cs2 players")
@app_commands.describe(player_id="Players id")
async def csstats(interaction: discord.Interaction, player_id: str):

    await interaction.response.send_message(f"Getting data...",ephemeral=True)
    data = await cs2_match_stats.get_info(player_id)
    await interaction.followup.send(embed=data,ephemeral=True)
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
    client.run(discord_token)
    
if __name__=="__main__": 
    main() 
