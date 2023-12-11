import sqlite3
from datetime import datetime
from get_news import get_news
from get_db_tweets import get_hash_id_db_tweets


# get the data from news api
df_news_api_to_inset_db = get_news('2023-11-24', '2023-12-11')

# get the hash_id from the dataframe
articles_in_db = get_hash_id_db_tweets()

for row in df_news_api_to_inset_db.itertuples():
    if row.hash_id not in articles_in_db:
        # insert the data to sqlite tweets db
        conn = sqlite3.connect('tweets.db')
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO tweets (hash_id, source_name, title, url, url_to_image, content, published_at_source, posted, 
            posted_tweet, posted_at_tweet, created_at, updated_at) 
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (row.hash_id, row.source_name, row.title, row.url, row.url_to_image, row.content,
                  row.published_at_source, row.posted, row.posted_tweet, row.posted_at_tweet, row.created_at,
                  row.updated_at)
        )

        conn.commit()
        conn.close()

        print(f'inserted {row.hash_id} to db')

    else:
        print(f'{row.hash_id} already in db')

print('done')
