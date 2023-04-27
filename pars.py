import aiohttp,asyncio
import ssl
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from pyshorteners import Shortener
import requests 

HEADERS = {"User-Agent": UserAgent().random}

async def mine(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS, ssl=False) as response:
            r = await response.content.read()
            soup = BS(r, 'html.parser')
            items = soup.find_all('a', {'class': 'mainlink'})
            shortener = Shortener(timeout=5)
            for item in items:
                title = item.find('span').text.split()
                link = item['href']              
                print(f'TITLE:{title}            |                {link}')

async def main():
    tasks = []
    for i in range(1, 11):
        url = f"https://gidonline.io/page/{i}"
        task = asyncio.ensure_future(mine(url))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
