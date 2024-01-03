"""
This module contains the crawler for the derstandard.at website.
"""

import asyncio
import aiohttp
import xml.etree.ElementTree as ET
from typing import AsyncGenerator, Coroutine, List, Dict, Optional, Generator
from tqdm import tqdm



BUDGET_REQUESTS_PER_MINUTE = 60



class DerStandardCrawler:
    """
    This class implements a crawler for a website.
    """
    
    # Fields
    site_url: str
    sitemap_resource: str
    rpm: int
    session: Optional[aiohttp.ClientSession] = None


    # Constructor
    def __init__(self, site_url: str, sitemap_resource: str = "/sitemap.xml", budget_requests_per_minute: int = BUDGET_REQUESTS_PER_MINUTE):
        self.site_url = site_url
        self.sitemap_resource = sitemap_resource
        self.rpm = budget_requests_per_minute

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    async def __aexit__(self, exception_type, exception, traceback):
        await self.close()


    # methods
    async def close(self):
        """
        This method closes the aiohttp session.
        """
        await self.session.close()

    async def get_all_urls(self) -> AsyncGenerator[Dict[str, object], None]:
        """
        This method returns all urls from the website.
        :return: A coroutine that yields all urls from the website
        """
        
        sitemaps = [ self.site_url + self.sitemap_resource ]
        while len(sitemaps) > 0:
            sitemap = sitemaps.pop()
            async for it in self.parse_sitemap(sitemap, self.session):
                if it['type'] == 'sitemap':
                    sitemaps.append(it['loc'])
                
                elif it['type'] == 'url':
                    yield {
                        'loc': it['loc'],
                        'lastmod': it['lastmod']
                    }

    
    async def parse_sitemap(self, url: str, session: Optional[aiohttp.ClientSession]) -> AsyncGenerator[Dict[str, object], None]:
        """
        This function fetches all the sitemap urls a commulated sitemap file.
        example: https://www.derstandard.at/sitemaps/sitemap.xml
        :param url: The url of the sitemap file
        :param session: The aiohttp session to use for the request
        :yield: Yields each sitemap URL
        """

        got_session = False if not session else True
        if not got_session: session = aiohttp.ClientSession()
        try:
            # Fetch content from url and parse it
            # Description: sitemapindex (root) -> List[sitemap] -> { loc, lastmod }
            xml_content = await (await session.get(url)).text()
            xml_tree = ET.fromstring(xml_content)
            
            # get all sitemap urls
            namespace_map = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            type_map = [ 'sitemap', 'url' ]

            for t in type_map:
                elements = xml_tree.findall(f"sm:{t}", namespaces=namespace_map)
                for sitemap in elements:
                    yield {
                        'type': t,
                        'loc': sitemap.find('sm:loc', namespaces=namespace_map).text,
                        'lastmod': sitemap.find('sm:lastmod', namespaces=namespace_map).text
                    }
        
        finally:
            if not got_session: await session.close()

