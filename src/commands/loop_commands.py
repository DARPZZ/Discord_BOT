from loop import *
from share import *
from src.helpers.is_owner import has_owner_role

@client.tree.command(name="football", description="Scrape football matches")
async def football(interaction: discord.Interaction):
    if not has_owner_role(interaction):
        return
    await interaction.response.send_message("Scrapeing football matches...")
    await start_football_loop.start()
    

@client.tree.command(name="cs", description="Scrapeing Counter-Strike matches")
async def cs(interaction: discord.Interaction):
    if not has_owner_role(interaction):
        return
    await interaction.response.send_message("Scrapeing Counter-Strike matches...")
    await start_counterstrike_loop.start()
    
@client.tree.command(name="f1", description="Scrapeing F1 matches")
async def f1(interaction: discord.Interaction):
    if not has_owner_role(interaction):
        return
    await interaction.response.send_message("Scrapeing F1 matches...")
    await start_f1_loop.start()
    
@client.tree.command(name="epicgames", description="Start epic games loop",)
async def epicgames(interaction: discord.Interaction):
    if not has_owner_role(interaction):
        return
    await interaction.response.send_message("Scrapeing free epic games...")
    await start_epic_games_loop.start()

@client.tree.command(name="ufc", description="Start ufc loop",)
async def epicgames(interaction: discord.Interaction):
    if not has_owner_role(interaction):
        return
    await interaction.response.send_message("Scrapeing ufc games...")
    await start_Ufc_loop.start()

    
    