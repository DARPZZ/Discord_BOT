async def sendMessageForNoData(discord,channel):
    embedVar = discord.Embed( color=0x9D00FF, description="**No Data**"  )
    await channel.send(embed=embedVar)