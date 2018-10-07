"""
Main Runner file

@copyright Chris Corbo - 2018
"""
import click

from app.sports_database_util import SportsDatabaseUtil

@click.command()
@click.option("--year", default=2018, help="year to evaluate statistics")
def run(year):
    try:
        print(f"Generating for {year}")
        sports_db = SportsDatabaseUtil()
        #sports_db.get_season_totals_stats(year)
        #sports_db.get_season_wins_total(year)
        sports_db._get_past_matchups()
    except Exception as e:
        print(e.message)

if __name__ == '__main__':
    run()