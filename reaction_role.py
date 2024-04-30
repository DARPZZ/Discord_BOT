from share import *


def add_and_remove_roles(guild,payload):
    global role
    if payload.emoji.name == "F1":
        role = discord.utils.get(guild.roles, name ="F1")
    elif payload.emoji.name =="football":
        role = discord.utils.get(guild.roles, name ="football")
    else:
        role = discord.utils.get(guild.roles, name=payload.emoji.name)
    
        
        
@client.event
async def on_raw_reaction_add(payload):
    messageid = payload.message_id
    if messageid == 1234879704981307453:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        add_and_remove_roles(guild,payload)
        
        if role is not None:
            member = await guild.fetch_member(payload.user_id)
            if member is not None:
                await member.add_roles(role)
                
                
@client.event
async def on_raw_reaction_remove(payload):
    messageid = payload.message_id
    if messageid == 1234879704981307453:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        add_and_remove_roles(guild,payload)
        
        if role is not None:
            member = await guild.fetch_member(payload.user_id)
            if member is not None:
                await member.remove_roles(role)