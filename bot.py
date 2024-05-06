# This example requires the 'message_content' intent.
from share import *
import Football
import reaction_role
import F1
import counterstrike
import loop
import Ufc
load_dotenv() 
discord_token = os.getenv("discord_token")
intents.message_content = True


@client.command() 
async def CS(ctx):
    await counterstrike.scrape_matches()
    
@client.command()
async def football(ctx):
  await Football.scrape_matches()

@client.event
async def on_ready():
   await loop.start_counterstrike_loop()
   await loop.start_football_loop()
@client.command()
async def f1(ctx):
    await F1.scrape_matches()
    
@client.command()
async def ufc(ctx):
    await Ufc.scrape_matches()


@client.command()
async def clear(ctx, amount = 50):
    await ctx.channel.purge(limit=amount)
            
def main():

    client.run(discord_token)
if __name__=="__main__": 
    main() 
