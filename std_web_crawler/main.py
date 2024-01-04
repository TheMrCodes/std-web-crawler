import dotenv
import os
import asyncio
import pandas as pd
from std_web_crawler.crawler.derstandard import DerStandardCrawler


# load environment variables
ret = dotenv.load_dotenv()

OUTPUT_DIR = os.getenv('APP_OUTPUT_DIR')



async def main():
    async with DerStandardCrawler(
        'https://www.derstandard.at',
        '/sitemaps/sitemap.xml'
    ) as crawler:
        print('Fetching urls...')
        urls = []
        count = 0
        async for url in crawler.get_all_urls():
            urls.append(url)
            count += 1
            if count % 100_000 == 0:
                print(f'Fetched {count} urls.')

        # pandas
        urls_df = pd.DataFrame(urls)
        urls_df.to_csv(OUTPUT_DIR + '/urls.csv', index=False, header=True, sep=';', encoding='utf-8', quoting=1, quotechar='"')


if __name__ == '__main__':
    asyncio.run(main())