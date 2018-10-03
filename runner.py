"""
Main Runner file

@copyright Chris Corbo - 2018
"""
from app.sports_database_util import SportsDatabaseUtil


scraper = SportsDatabaseUtil()
scraper.get_team_stats()