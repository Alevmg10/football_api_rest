import scrapy
import json
from ..items import LigascraperTable, LigascraperMatches, LigascraperMatchesLasted

class LaligaTable(scrapy.Spider):
    name = "laliga_table"
    allowed_domains = ["fotmob.com/"]
    start_urls = ["https://www.fotmob.com/api/leagues?id=87&ccode3=VEN"]

    custom_settings = {
        'FEEDS': { './laligascraper/spiders/data/tabla_posiciones.json': { 'format': 'json', 'overwrite': True},
                    './laligascraper/spiders/data/tabla_posiciones.csv': {'format': 'csv', 'overwrite': True},
                    }
        }
    
    def parse(self, response):
        data = json.loads(response.body)
        table_data = data["table"]
        season = data['details']['selectedSeason']

        for team in table_data:
            team_data = team["data"]  # Accediendo al diccionario de datos del equipo

            for elemento in team_data["table"]["all"]:
                elementos = LigascraperTable(
                temporada=season,
                posicion=elemento["idx"],
                equipo=elemento["name"],
                puntos=elemento["pts"],
                jugados=elemento["played"],
                ganados=elemento["wins"],
                empates=elemento["draws"],
                perdidos=elemento["losses"],
                gol_dif=elemento["goalConDiff"]
            )
                yield elementos


class LaligaMatches(scrapy.Spider):
    name = 'laliga_matches'
    allowed_domains = ["fotmob.com/"]
    start_urls = ['https://www.fotmob.com/api/leagues?id=87&ccode3=VEN']

    custom_settings = {
        'FEEDS': { './laligascraper/spiders/data/2023_2024_calendario_y_resultados.json': { 'format': 'json', 'overwrite': True},
                    './laligascraper/spiders/data/2023_2024_calendario_y_resultados.csv': {'format': 'csv', 'overwrite': True},
                    }
        }

    def parse(self, response):
        data = json.loads(response.body)
        matches = data['matches']
        season = data['details']['selectedSeason']

        for rounds in matches['allMatches']:
            calendario_items = LigascraperMatches()
            if not rounds["status"]["cancelled"]:
                try:
                    calendario_items['temporada'] = season
                    calendario_items['ronda'] = rounds['round']
                    calendario_items['local'] = rounds['home']['name']
                    calendario_items['marcador'] = rounds['status']['scoreStr']
                    calendario_items['visitante'] = rounds['away']['name']
                    yield calendario_items
                except KeyError:
                    pass
            else:
                calendario_items['temporada'] = season
                calendario_items['ronda'] = rounds['round']
                calendario_items['local'] = rounds['home']['name']
                calendario_items['marcador'] = 'Pospuesto'
                calendario_items['visitante'] = rounds['away']['name']
                yield calendario_items


class BplMatchesLastedSeason(scrapy.Spider):
    name = 'laliga_matches_lasted'
    allowed_domains = ["fotmob.com/"]
    start_urls = ['https://www.fotmob.com/api/leagues?id=87&ccode3=VEN&season=2018%2F2019']

    custom_settings = {
            'FEEDS': { './laligascraper/spiders/data/2018_2019_calendario_y_resultados.json': { 'format': 'json', 'overwrite': True}
                }
            }
    
    def parse(self, response):
        data = json.loads(response.body)
        matches = data['matches']
        season = data['details']['selectedSeason']

        calendario_items = LigascraperMatchesLasted()

        for rounds in matches['allMatches']:
            if not rounds["status"]["cancelled"]:
                try:
                    calendario_items['temporada'] = season
                    calendario_items['ronda'] = rounds['round']
                    calendario_items['local'] = rounds['home']['name']
                    calendario_items['marcador'] = rounds['status']['scoreStr']
                    calendario_items['visitante'] = rounds['away']['name']
                    yield calendario_items
                except KeyError:
                    pass
            else:
                calendario_items['temporada'] = season
                calendario_items['ronda'] = rounds['round']
                calendario_items['local'] = rounds['home']['name']
                calendario_items['marcador'] = 'Pospuesto'
                calendario_items['visitante'] = rounds['away']['name']
                yield calendario_items