"""
SDQL Query Constants

@copyright Chris Corbo - 2018
"""

class SDQLQueries:

    # Gets season total of yards scored / allowed
    SEASON_TOTALS_QUERY = """
        Sum(passing yards) as off_passing_yards, 
        Sum(rushing yards) as off_rushing_yards, 
        Sum(o:passing yards) as def_passing_yards, 
        Sum(o:rushing yards) as def_rushing_yards, 
        Sum(plays) as off_plays,
        Sum(o:plays) as plays_against,
        Sum(points) as points_for,
        Sum(o:points) as points_allowed,
        Average(regular season wins line) as season_wins_line
        @team and season="""

    WIN_TOTALS_QUERY = """
        team,
        regular season wins line as wins_line
        @season="""

    PAST_MATCHUP_QUERY = """
        season,
        week,
        team,
        o:team as opponent,
        points,
        o:points as points_against,
        line,
        ats margin,
        site,
        surface,
        passing yards as off_passing_yards,
        rushing yards as off_rushing_yards,
        o:passing yards as def_passing_yards,
        o:rushing yards as def_rushing_yards,
        plays as off_plays,
        o:plays as def_plays
        @team and season > 2010
    """

    CURRENT_MATCHUP_QUERY = """
        week,
        team,
        o:team as opponent,
        line,
        total,
        site,
        surface,
        start time,
        ats streak,
        division
        @"""