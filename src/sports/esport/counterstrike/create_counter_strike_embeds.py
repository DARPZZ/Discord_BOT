def create_upcomming_matches_enmed(embedVar,team_name,odds,bo_type,tournament_name,tournament_price_pool):
    embedVar.add_field(name="**Teams: **",value= team_name,inline=False)
    embedVar.add_field(name="**Odds: **",value= odds,inline=True)
    embedVar.add_field(name="**BO: **",value= bo_type,inline=True)
    embedVar.add_field(name="**Torunament: **", value="",inline=False)
    embedVar.add_field(name="**Torunament name: **", value=tournament_name,inline=True)
    embedVar.add_field(name="**Torunament price: **", value=tournament_price_pool,inline=True)
    
def create_live_matches_enmed(embedVar,team_name,team1_score,team2_score,tournament_name,tournament_price_pool):
    embedVar.add_field(name="**Teams**: ",value=team_name)
    embedVar.add_field(name="**Score**: ",value=f"{team1_score} - {team2_score} ")
    embedVar.add_field(name="**Torunament INFO: **", value="",inline=False)
    embedVar.add_field(name="**Torunament name: **", value=tournament_name,inline=True)
    embedVar.add_field(name="**Torunament price: **", value=tournament_price_pool,inline=True)  
         
async def create_streams_embed(streams,embedVar):
    embedVar.add_field(name="**Streams** :",value=f" ",inline=False)
    for url, viewer_count in streams.items():
        embedVar.add_field(name=f"<{url}>", value=viewer_count,inline=False)