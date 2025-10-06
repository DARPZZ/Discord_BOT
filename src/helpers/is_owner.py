from share import *
def has_owner_role(interaction: discord.Interaction) -> bool:
    return any(role.name.lower() == "owner" for role in interaction.user.roles)