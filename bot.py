# This example requires the 'message_content' intent.
from share import *
import Football
import reaction_role
import F1
import counterstrike
import owner_commands
load_dotenv() 
discord_token = os.getenv("discord_token")
intents.message_content = True

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!football'):
         await Football.scrape_matches()
    elif message.content.startswith('!CS'):

        await counterstrike.scrape_matches_cs()
@client.event
async def on_ready():
    await Football.scrape_matches.start()
    await counterstrike.scrape_matches_cs.start()
    
def main():

    client.run(discord_token)
if __name__=="__main__": 
    main() 
