import requests
import json
import pandas as pd
import hashlib
from datetime import datetime


def get_news(start_date=datetime.now().strftime('%Y-%m-%d'), end_date=datetime.now().strftime('%Y-%m-%d')):
    # get the data from news api
    url = ('https://newsapi.org/v2/everything?'
           'q=technology&AND(news)'
           f'from={start_date}&'
           f'to={end_date}&'
           'sortBy=popularity&'
           'apiKey=818f91fd62bb49e28a9abd85691b55cb')

    response = requests.get(url)

    # save the response as file json format
    with open('data.json', 'w') as outfile:
        json.dump(response.json(), outfile)

    #### create a dataframe to store the data
    df_news_api = pd.DataFrame(
        columns=['hash_id', 'source_name', 'title', 'url', 'url_to_image', 'content', 'published_at_source',
                 'posted', 'posted_tweet', 'created_at', 'updated_at'])

    #### append the data to the dataframe
    for i in response.json()['articles']:
        if 'heise' not in i['source']['name'] or 'Appbank.net' not in i['source']['name']:
            # hash the data
            md5 = hashlib.md5()
            md5_to_hash = f'{i["source"]["name"]}{i["title"]}{i["url"]}{i["urlToImage"]}{i["publishedAt"]}'.encode(
                'UTF-8')
            md5.update(md5_to_hash)
            md5_digested = md5.hexdigest()

            # convert to datetime publishedAt
            published_at = datetime.strptime(i['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # append the data
            df_news_api = df_news_api._append({'hash_id': md5_digested,
                                               'source_name': i['source']['name'],
                                               'title': i['title'],
                                               'url': i['url'],
                                               'url_to_image': i['urlToImage'],
                                               'content': i['content'],
                                               'published_at_source': published_at,
                                               'posted': 0,
                                               'posted_tweet': None,
                                               'posted_at_tweet': None,
                                               'created_at': created_at,
                                               'updated_at': updated_at
                                               }, ignore_index=True)

    return df_news_api


if __name__ == '__main__':
    df = get_news()
