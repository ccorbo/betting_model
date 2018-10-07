"""
Main Runner file

@copyright Chris Corbo - 2018
"""
import click

from app.sports_database_util import SportsDatabaseUtil

@click.command()
@click.option("--year", default=2018, help="year to evaluate statistics", type=int)
@click.option("--week", default=None, help="get current NFL week matchup", type=int)
@click.option("--get_past_matchups", default=False, help="If set to true, will get data for all NFL games since 2010", type=bool)
def run(year, week, get_past_matchups):
    try:
        print(f"Generating for {year}")
        sports_db = SportsDatabaseUtil()
        sports_db.get_season_totals_stats(year)
        if get_past_matchups:
            sports_db._get_past_matchups()
        if week:
            sports_db.get_weeks_matchups(week, year)
        print("FINISHED, Check resultant CSV files")
    except Exception as e:
        print(e.message)

if __name__ == '__main__':
    run()