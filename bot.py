from share import *
import Football
import reaction_role
import F1
from loop import *
import ufc
load_dotenv() 
discord_token = os.getenv("discord_token")
intents.message_content = True

@client.command()
async def football(ctx):
  await Football.scrape_matches()

   
@client.command()
async def cs(ctx):
    await CounterStrike.scrape_matches()  
@client.command()
async def f1(ctx):
    await F1.scrape_matches()

        
@client.command()
async def UFC(ctx):
    await ufc.scrape_matches()


@client.command()
async def clear(ctx, amount = 50):
    await ctx.channel.purge(limit=amount)
    
    
def wait_until_ready():
    start_football_loop.before_loop(client.wait_until_ready)
    start_f1_loop.before_loop(client.wait_until_ready)
    start_Ufc_loop.before_loop(client.wait_until_ready)
    start_counterstrike_loop.before_loop(client.wait_until_ready)
    twitch_loop.before_loop(client.wait_until_ready)

def loop_start():
    start_football_loop.start()
    start_Ufc_loop.start()
    start_f1_loop.start()
    start_counterstrike_loop.start()
    twitch_loop.start()
    
    
@client.event
async def on_ready():
    wait_until_ready()
    loop_start()
   
            
def main():

    client.run(discord_token)
if __name__=="__main__": 
    main() 
