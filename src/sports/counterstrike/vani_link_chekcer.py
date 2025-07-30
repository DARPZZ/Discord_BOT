import src.sports.counterstrike.GetPlayerInfo.steam_api_call as checker


async def check_if_link_is_64(PlayerID):
    if(PlayerID[-1] == "/"):
        PlayerID = PlayerID[:-1]
    splittede_player_id =""
    if("id/" in PlayerID):
       splittede_player_id = PlayerID.split("id/")
    elif ("profiles/" in PlayerID):
        splittede_player_id = PlayerID.split("profiles/")
    
    if(splittede_player_id):
        user_stats_data = await checker.CheckForVanityLink(splittede_player_id[1])
        link_list = user_stats_data['response']
        is_a_vanity_link = link_list.get("success")
        
        if(is_a_vanity_link == 1):
            return link_list.get("steamid")
        else:
            return splittede_player_id[1]

    