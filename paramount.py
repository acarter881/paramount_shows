import requests
import time
import re
import json
import pandas as pd
from bs4 import BeautifulSoup
from omdb import OMDB_KEY

"""
TODO: 
    1. [Create a PDF file with pictures of all the shows, ranked descending by IMDB rating]

"""

class Paramount:
    def __init__(self, base_folder) -> None:
        self.base_url = 'https://www.paramountplus.com'
        self.base_folder = base_folder
        self.url = 'https://www.paramountplus.com/shows/all/'
        self.show_dict = dict()
        self.show_list = list()
        self.OMDB_KEY = OMDB_KEY
        self.headers = {
            'accept': '*/*',
            'accept-encoding':'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://www.paramountplus.com',
            'referer': 'https://www.paramountplus.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        }
        self.features = 'html.parser'
        self.columns = [
            'title',
            'rated',
            'released',
            'genre',
            'actors',
            'language',
            'country',
            'rating_source',
            'rating',
            'imdbRating',
            'imdbVotes',
            'totalSeasons',
        ]

    def get_shows(self, images=False, omdb=True) -> dict:
        r = requests.get(url=self.url, headers=self.headers)

        soup = BeautifulSoup(markup=r.text, features=self.features)

        # Get each show's url, name, and jpeg
        for show in soup.find_all(name='a', attrs={'href': re.compile(pattern='\/shows\/.+')}):
            if show.text.strip() == '':
                show_url = self.base_url + show['href']
                show_name = show.find(name='img')['alt']
                show_jpeg_url = show.find(name='img')['data-src']

                if images:
                    self.get_images(show_name, show_jpeg_url)

                if omdb:
                    self.omdb_data(show_name)

                # Dictionary with show name as key and values as a list containing the show url and show jpeg url
                self.show_dict[show_name] = [show_url, show_jpeg_url]

        return self.show_dict

    def get_images(self, name_of_show, jpeg_url) -> None:
        time.sleep(0.001)

        show_image = requests.get(url=jpeg_url, headers=self.headers)

        # Download show jpeg
        with open(file=f"{self.base_folder}\\{name_of_show.replace('?', '').replace(':','')}.jpg", mode='wb') as f:
            print(f'Saving an image for {name_of_show}...')
            f.write(show_image.content)

    def omdb_data(self, name_of_show) -> list:
        name_of_show = name_of_show.replace('+', '%2B').replace('@','%40').replace('&', '%26').replace(':','%3A').replace('?', '%3F').replace('ã', '%C3%A3').replace('é','%C3%A9').replace('ú', '%C3%BA').replace(' ', '+')

        url = f'http://www.omdbapi.com/?apikey={self.OMDB_KEY}&t={name_of_show}'

        time.sleep(0.2)

        r = requests.get(url=url)

        show_json = json.loads(s=r.text)

        if show_json['Response'] == 'False':
            title, rated, released, genre, actors, language, country, rating_source, rating, imdbRating, imdbVotes, totalSeasons = 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
        else:
            title = show_json['Title']
            rated = show_json['Rated']
            released = show_json['Released']
            genre = show_json['Genre']
            actors = show_json['Actors']
            language = show_json['Language']
            country = show_json['Country']

            if show_json['Ratings']:
                rating_source = show_json['Ratings'][0]['Source']
                rating = show_json['Ratings'][0]['Value']
            else:
                rating_source, rating = 'N/A', 'N/A'

            imdbRating = show_json['imdbRating']
            imdbVotes = show_json['imdbVotes']

            try:
                totalSeasons = show_json['totalSeasons']
            except KeyError:
                totalSeasons = 'N/A'

            self.show_list.append((
                title,
                rated,
                released,
                genre,
                actors,
                language,
                country,
                rating_source,
                rating,
                imdbRating,
                imdbVotes,
                totalSeasons,
            ))

        return self.show_list

    def to_pandas(self) -> None:
        df = pd.DataFrame(data=self.show_list, index=None, columns=self.columns)

        df.to_excel(
            excel_writer=r'C:\Users\Alex\Desktop\hello\Python\paramount\Paramount.xlsx', 
            sheet_name='Paramount', 
            freeze_panes=(1,0)
            )

# Instantiate the class and run the necessary functions
if __name__ == '__main__':
    c = Paramount(base_folder=r'C:\Users\Alex\Desktop\hello\Python\paramount\pictures')
    c.get_shows(images=False, omdb=True)
    c.to_pandas()