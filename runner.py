"""
Main Runner file

@copyright Chris Corbo - 2018
"""
import click

from app.sports_database_util import SportsDatabaseUtil

@click.command()
@click.option("--year", default=2018, help="year to evaluate statistics", type=int)
@click.option("--week", default=None, help="get current NFL week matchup", type=int)
def run(year, week):
    try:
        print(f"Generating for {year}")
        sports_db = SportsDatabaseUtil()
        sports_db.get_season_totals_stats(year)
        sports_db._get_past_matchups()
        if week:
            sports_db.get_weeks_matchups(week, year)
        print("FINISHED, Check resultant CSV files")
    except Exception as e:
        print(e.message)

if __name__ == '__main__':
    run()