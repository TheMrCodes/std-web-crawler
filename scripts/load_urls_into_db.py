import asyncio
import logging
import dotenv
import os
import pandas as pd
from tqdm import tqdm, trange
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from std_web_crawler.db.base import BaseModel
from std_web_crawler.db.job import Job, JobStatus
from std_web_crawler.db.url import Url
from std_web_crawler.error import error
dotenv.load_dotenv()


OUTPUT_DIR = os.getenv("APP_OUTPUT_DIR") or error("APP_OUTPUT_DIR not set!")
INPUT_FILE = 'urls.parquet'


async def main():
    # Connect and create database
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/std_web_crawler')

    # create all model tables
    metadata = BaseModel.metadata
    logging.info("Creating following tables:")
    for t in metadata.sorted_tables:
        logging.debug(t.name)
    metadata.create_all(engine, checkfirst=True)

    # Read parquet file from disk
    logging.info('Reading parquet file...')
    df = pd.read_parquet(OUTPUT_DIR +'/'+ INPUT_FILE)

    # Prepare data
    logging.info('Preparing data for database...')

    df.rename(columns={'loc': 'url'}, inplace=True)
    df['lastmod'] = pd.to_datetime(df['lastmod'], format='ISO8601', utc=True)
    df = df.groupby('url').agg({'lastmod': 'max'}).reset_index()
    df['created_at'] = pd.Timestamp.now()

    # Insert into database
    logging.info('Inserting data into database...')
    chunck_size = 100_000
    for i in trange(0, len(df), chunck_size, desc='Inserting chuncks into database'):
        chunck = df[i:i+chunck_size]
        chunck.to_sql(Url.__tablename__, engine, if_exists='append', index=False, method='multi')
    logging.info('Done inserting data into database...')
    
    exit(0)

    # Mapping data
    logging.info('Mapping data...')
    #data = df['loc'].drop_duplicates().apply(lambda x: Job(url=x, status=JobStatus.CREATED, created_at=pd.Timestamp.now()))

    data = []
    for i, row in tqdm(df.iterrows(), total=len(df), desc='Mapping data', miniters=10000, maxinterval=2):
        data.append(Url(url=row['loc'], lastmod=row['lastmod'], created_at=pd.Timestamp.now()))

    # Insert into database
    logging.info('Inserting data into database...')
    chunck_size = 100_000
    with Session(engine) as session:
        for i in trange(0, len(data), chunck_size, desc='Inserting chuncks into database'):
            chunck = data[i:i+chunck_size]
            session.add_all(chunck)
        logging.info('Committing...')
        session.bulk_insert_mappings(Url, df.iterrows())
    logging.info('Done inserting data into database...')



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()