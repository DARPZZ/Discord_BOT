# This example requires the 'message_content' intent.
from dotenv import load_dotenv
from share import *
import os
import Football

load_dotenv() 
discord_token = os.getenv("discord_token")
intents.message_content = True

def main():
    client.run(discord_token)
    
  
if __name__=="__main__": 
    main() 
