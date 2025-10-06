from loop import *
from share import *
from src.helpers.is_owner import has_owner_role

@client.tree.command(name="football", description="Scrape football matches")
async def football(interaction: discord.Interaction):
    if not has_owner_role(interaction):
        return
    await interaction.response.send_message("Scraping football matches...")
    await start_football_loop.start()
    

@client.tree.command(name="cs", description="Scrape Counter-Strike matches")
async def cs(interaction: discord.Interaction):
    if not has_owner_role(interaction):
        return
    await interaction.response.send_message("Scrape Counter-Strike matches...")
    await start_counterstrike_loop.start()
    
@client.tree.command(name="f1", description="Scrape F1 matches")
async def f1(interaction: discord.Interaction):
    if not has_owner_role(interaction):
        return
    await interaction.response.send_message("Scraping F1 matches...")
    await start_f1_loop.start()