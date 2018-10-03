"""
SDQL Query Constants

@copyright Chris Corbo - 2018
"""

class SDQLQueries:

    # Gets season total of yards scored / allowed
    SEASON_YARDS_QUERY = """
        Sum(passing yards) as off_passing_yards, 
        Sum(rushing yards) as off_rushing_yards, 
        Sum(receiving yards) as off_receiving_yards, 
        Sum(o:passing yards) as def_passing_yards, 
        Sum(o:rushing yards) as def_rushing_yards, 
        Sum(o:receiving yards) as def_receiving_yards,
        Sum(plays) as off_plays,
        Sum(o:plays) as plays_against
        @team and season=2018
    """