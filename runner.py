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
        #sports_db.get_season_net_yard_per_play_stats(2017)
        sports_db.get_season_wins_total(year)
    except Exception as e:
        print(e.message)

if __name__ == '__main__':
    run()