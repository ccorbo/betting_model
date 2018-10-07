"""
Betting Model Website Scrape
used to scrape profootball reference and write to data
files in  data directory

@copyright Chris Corbo - 2018
"""
import pandas as pd
import requests
import json

from bs4 import BeautifulSoup

from constants.nfl_team_constants import NflTeamConstants
from constants.nfl_stadium_constants import NflStadiumConstants
from app.sdql_queries import SDQLQueries
from app.dataframes_table_util import DataframesTableUtil

class SportsDatabaseUtil:

    BASE_URL = 'http://api.sportsdatabase.com/nfl/query.json'

    def __init__(self):
        self.tables_util = DataframesTableUtil()

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
        self.tables_util._build_season_totals_table(dict_response, season_year)

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

    def _get_past_matchups(self):
        """
            Gets all matchups greater than 2010
        """
        response = self._call_sportsdatabase(f'{SDQLQueries.PAST_MATCHUP_QUERY}')
        dict_response = self._parse_response(response.text)
        self.tables_util._build_past_matchup_table(dict_response)

    def get_weeks_matchups(self, week, year):
        where_clause = f'week={str(week)} and season={str(year)}'
        response = self._call_sportsdatabase(f'{SDQLQueries.CURRENT_MATCHUP_QUERY}{where_clause}')
        dict_response = self._parse_response(response.text)
        self.tables_util._build_weeks_matchups_table(dict_response, week, year)

    