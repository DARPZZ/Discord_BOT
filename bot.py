# This example requires the 'message_content' intent.
from share import *
import Football
import reaction_role
import F1
from loop import *
import Counterstrike
import ufc
load_dotenv() 
discord_token = os.getenv("discord_token")
intents.message_content = True

    
@client.command()
async def football(ctx):
  await Football.scrape_matches()

   
   
@client.command()
async def f1(ctx):
    await F1.scrape_matches()

   
@client.command()
async def cs(ctx):
    matches_info = Counterstrike.hello()
    if matches_info:
        await ctx.send(f"**Live Matches:**\n\n{matches_info}")
    else:
        await ctx.send("No live matches at the moment.")
        
@client.command()
async def ufc(ctx):
    await ufc.scrape_matches()


@client.command()
async def clear(ctx, amount = 50):
    await ctx.channel.purge(limit=amount)
    
    
    
    
    
@client.event
async def on_ready():
   start_football_loop.before_loop(client.wait_until_ready)
   start_f1_loop.before_loop(client.wait_until_ready)
   start_Ufc_loop.before_loop(client.wait_until_ready)
   start_football_loop.start()
   start_Ufc_loop.start()
   start_f1_loop.start()
            
def main():

    client.run(discord_token)
if __name__=="__main__": 
    main() 
