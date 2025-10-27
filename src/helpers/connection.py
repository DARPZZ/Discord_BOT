
class  connection:
    def __init__(self,aiohttp,BeautifulSoup):
        self.aiohttp = aiohttp
        self.BeautifulSoup = BeautifulSoup
        
    async def create_connection(self,url,headers=None):
        
        async with self.aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                text = await response.text()
        soup = self.BeautifulSoup(text, 'html.parser')
        return soup
    