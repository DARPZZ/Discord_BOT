# This example requires the 'message_content' intent.
from share import *
import Football
import reaction_role
import F1
load_dotenv() 
discord_token = os.getenv("discord_token")
intents.message_content = True

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
def main():
    client.run(discord_token)
    reaction_role
    Football
    F1
if __name__=="__main__": 
    main() 
