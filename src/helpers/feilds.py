class feilds:
    def __init__(self,embedVar):
        self.embedVar = embedVar
        
    def generate_feilds(self,name,value):
        self.embedVar.add_field(name=name, value=value, inline=False)
        
    async def clear_feilds(self,channel):
        await channel.purge()
        
    
        