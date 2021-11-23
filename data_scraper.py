import requests
from bs4 import BeautifulSoup
import random
import pandas as pd
from json import JSONDecodeError
import re


def translate(query):
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ta&dt=t&q=' + query
    resp = requests.get(url)
    return resp.json()[0][0][0]


def get_movie(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    crews = soup.find_all('span', attrs={'class': 'crew-set'})
    for crew in crews:
        if 'Direction' in crew.text:
            director = translate(crew.text.split(':')[-1].strip())
            break
    else:
        director = ''

    review = ' '.join([_.text.strip() for _ in soup.find('div', attrs={
        'class': 'two_col_box top_margin_10 col_708_box float left_margin_15'}).find_all('p')]).split(
        'BEHINDWOODS REVIEW BOARD')[0].strip().replace('\xa0', '')
    try:
        movie = re.search("'(.+?)'", review).group(1)
    except AttributeError:
        movie = translate(soup.h1.text.split('(')[0].strip())
    date_published = soup.find('span', {'itemprop': 'datePublished'})['datetime']

    verdict = soup.find('div', attrs={'class': 'top_margin_15 lightblackfont_15'}).text.split('Verdict:')[-1].strip()
    try:
        b_rating = soup.find('meta', attrs={'property': 'reviewRating'}).parent.text.split()[0]
    except:
        b_rating = ''
    try:
        resp_iframe = requests.get('https://www.behindwoods.com/tamil-movies/' + url.split('/')[4] + '/review.html')
        p_rating = BeautifulSoup(resp_iframe.content, 'html.parser').span.text.strip()
    except:
        p_rating = ''
    return [director, movie, review, date_published, verdict, b_rating, p_rating]


# collect the review url to scrape
resp = requests.get('https://www.behindwoods.com/tamil-movies/tamil-movie-reviews-a-to-z.html')
soup = BeautifulSoup(resp.content, 'html.parser')
all = [_['href'] for _ in soup.find_all('a')]
tamil_movie_link = [_ for _ in all if '-tamil-review' in _]
movie_links = tamil_movie_link
df_url = pd.DataFrame(movie_links, columns=['URL'])
df_url.to_csv('corpus/review_urls.csv', index=False)

data = []
for i in range(0, 20):
    print(i, end=',')
    tmp = get_movie(movie_links[i])
    data.append(tmp)

df = pd.DataFrame(data, columns=['director', 'movie', 'review', 'date_published', 'verdict', 'b_rating', 'p_rating'])
df.to_csv('corpus/behindwoods_data.csv', index=False)
