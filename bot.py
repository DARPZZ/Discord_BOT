from share import *
from src.Sports.Football import Football
import reaction_role
from loop import *
import src.Sports.Ufc.ufc as ufc
load_dotenv() 
discord_token = os.getenv("discord_token")
intents.message_content = True

@client.command()
async def football(ctx):
  await Football.Football.scrape_matches()

   
@client.command()
async def cs(ctx):
    await CounterStrike.scrape_matches()  
@client.command()
async def f1(ctx):
    await F1.F1.scrape_matches()

        
@client.command()
async def UFC(ctx):
    await UFC.scrape_matches()


@client.command()
async def clear(ctx, amount = 50):
    await ctx.channel.purge(limit=amount)
    

async def loop_start():
    await asyncio.gather(
        start_football_loop.start(),
        start_Ufc_loop.start(),
        start_f1_loop.start(),
        start_f1_driver_team_loop.start(),
        start_counterstrike_loop.start(),
        twitch_loop.start()
    )
    
    
@client.event
async def on_ready():
   await loop_start()
   
            
def main():
    client.run(discord_token)
    
if __name__=="__main__": 
    main() 
