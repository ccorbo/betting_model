"""
Betting Model Website Scrape
used to scrape profootball reference and write to data
files in  data directory

@copyright Chris Corbo - 2018
"""
import pandas as pd
import requests
import urllib.request
import urllib.parse
import json

from bs4 import BeautifulSoup
from urllib.request import urlopen

from constants.nfl_team_constants import NflTeamConstants
from app.sdql_queries import SDQLQueries

class SportsDatabaseUtil:

    BASE_URL = 'http://api.sportsdatabase.com/nfl/query.json'
    
    def get_team_stats(self):
        payload = {
            'sdql': SDQLQueries.SEASON_YARDS_QUERY,
            'output': 'json',
            'api_key': 'guest'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        }
        response = requests.get(self.BASE_URL, params=payload, headers=headers)
        dict_response = self._parse_response(response.text)
        self._build_table(dict_response)

    def get_player_stats(self):
        pass

    def _parse_response(self, response):
        """
        Kind of a hacky function to parse the response
        and get the response into a dict
        """
        raw = response.replace('json_callback(', '')
        raw = raw.replace(');\n', '')
        raw = raw.replace('\t', '')
        raw = raw.replace(' ', '')
        raw = raw.replace('\'', '\"')
        dict_response = json.loads(raw)
        return dict_response

    def _build_table(self, data):
        """
        Builds pandas table from dict of data

        Args:
            data(dict): Dict of data
        """
        headers = data['headers']
        mapped_data = {}
        for column_data in data['groups']:
            mapped_data[column_data['sdql']] = column_data['columns']

        #clean data for some reason its an array of arrays of arrays
        for key in mapped_data.keys():
            column_data = mapped_data[key]
            column_list = [data[0] for data in column_data]
            mapped_data[key] = column_list
        
        df = pd.DataFrame(columns=headers, data=list(mapped_data.values()), index=list(mapped_data.keys()))
        df['off_yards_total'] = df.off_passing_yards + df.off_rushing_yards + df.off_receiving_yards
        df['def_yards_total'] = df.def_passing_yards + df.def_rushing_yards + df.def_receiving_yards
        df['ypp_for'] = df.off_yards_total / df.off_plays 
        df['ypp_allowed'] = df.def_yards_total / df.plays_against
        df['net_ypp'] = df['ypp_for'] - df['ypp_allowed']
        df.to_csv('/home/ccorbo/betting_model/test.csv')