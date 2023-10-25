import pandas as pd
import sqlite3


def get_hash_id_db_tweets():
    # get the data from sqlite tweets db from tweets table and make a new dataframe
    conn = sqlite3.connect('tweets.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM tweets;
        """
    )

    rows = cursor.fetchall()
    df_tweets_db = pd.DataFrame(rows,
                                columns=['id', 'hash_id', 'source_name', 'title', 'url', 'url_to_image', 'content',
                                         'published_at_source', 'posted', 'posted_tweet', 'posted_at_tweet',
                                         'created_at', 'updated_at'])

    conn.close()

    #### get the hash_id from the dataframe
    articles_in_db = df_tweets_db['hash_id'].to_list()

    return articles_in_db


if __name__ == '__main__':
    get_hash_id_db_tweets()
