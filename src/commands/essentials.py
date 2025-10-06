from share import *
from src.helpers.is_owner import has_owner_role
from discord import app_commands
from src.get_settings import read_settings_file as settings
from src.logs import get_logs

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