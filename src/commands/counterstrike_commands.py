from share import *
import src.sports.esport.counterstrike.vani_link_chekcer as link_checker
import src.sports.esport.counterstrike.GetPlayerInfo.cs2_match_stats as cs2_match_stats
from src.get_settings import read_settings_file as settings
from discord import app_commands

@client.tree.command(name="csstats", description="Get information about cs2 players")
@app_commands.describe(player_id="Players id")
async def csstats(interaction: discord.Interaction, player_id: str):
    normal_player_settings = settings("cs")
    allowed_channel_id = normal_player_settings["playerLookUpID"]
    
    
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

async def get_numbers_of_ID(accounts,interaction):
    if(len(accounts)>10):
        await interaction.response.send_message("You can´t have that many id´s", ephemeral=True)
        return False
    else:
        return True

