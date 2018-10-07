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

    def _call_sportsdatabase(self, query):
        payload = {
            'sdql': query,
            'output': 'json',
            'api_key': 'guest'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        }
        response = requests.get(self.BASE_URL, params=payload, headers=headers)
        return response
    
    def get_season_totals_stats(self, season_year):
        response = self._call_sportsdatabase(f'{SDQLQueries.SEASON_TOTALS_QUERY}{str(season_year)}')
        dict_response = self._parse_response(response.text)
        self._build_season_totals_table(dict_response, season_year)

    def get_season_wins_total(self, season_year):
        response = self._call_sportsdatabase(f'{SDQLQueries.WIN_TOTALS_QUERY}{str(season_year)}')
        print(response.text)
        print(response.url)

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

    def _build_season_totals_table(self, data, season_year):
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
        df['off_yards_total'] = df.off_passing_yards + df.off_rushing_yards
        df['def_yards_total'] = df.def_passing_yards + df.def_rushing_yards
        df['ypp_for'] = df.off_yards_total / df.off_plays 
        df['ypp_allowed'] = df.def_yards_total / df.plays_against
        df['net_ypp'] = df['ypp_for'] - df['ypp_allowed']
        df['net_points'] = df.points_for - df.points_allowed
        df.to_csv(f'/home/ccorbo/betting_model/test_{season_year}.csv')

    def _get_past_matchups(self):
        """
            Gets all matchups greater than 2010
        """
        response = self._call_sportsdatabase(f'{SDQLQueries.PAST_MATCHUP_QUERY}')
        dict_response = self._parse_response(response.text)
        self._build_past_matchup_table(dict_response)

    def _build_past_matchup_table(self, data):
        # file = open('testfile.txt','w') 
        # file.write(json.dumps(data))

        data_frames = []
        headers = data['headers']
        for team_data in data['groups']:
            name = team_data['sdql']
            df = pd.DataFrame(columns=headers)
            header_count = 0
            df_map = {}
            for column_data in team_data['columns']:
                df_map[headers[header_count]] = pd.Series(data=column_data)
                header_count += 1
            df = pd.DataFrame(df_map)
            data_frames.append(df)

        result = pd.concat(data_frames)
        result.to_csv(f'/home/ccorbo/betting_model/test_past_matchups.csv')