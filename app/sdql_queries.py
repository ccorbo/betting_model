"""
SDQL Query Constants

@copyright Chris Corbo - 2018
"""

class SDQLQueries:

    # Gets season total of yards scored / allowed
    SEASON_YARDS_QUERY = 'Sum(passing yards), Sum(rushing yards), Sum(receiving yards), Sum(o:passing yards), Sum(o:rushing yards), Sum(o:receiving yards) @team and season=2018'