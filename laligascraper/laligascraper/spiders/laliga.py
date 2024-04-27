import scrapy
import json
from ..items import LigascraperTable, LigascraperGames

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


class LaligaGames(scrapy.Spider):
    name = 'laliga_games'
    allowed_domains = ["fotmob.com/"]

    custom_settings = {
        'FEEDS': { './laligascraper/spiders/data/calendario_y_resultados.json': { 'format': 'json', 'overwrite': True},
                    './laligascraper/spiders/data/calendario_y_resultados.csv': {'format': 'csv', 'overwrite': True},
                    }
        }

    def start_requests(self):
        urls = [
            'https://www.fotmob.com/api/leagues?id=87&ccode3=VEN',
            'https://www.fotmob.com/api/leagues?id=87&ccode3=VEN&season=2022%2F2023',
            'https://www.fotmob.com/api/leagues?id=87&ccode3=VEN&season=2021%2F2022',
            'https://www.fotmob.com/api/leagues?id=87&ccode3=VEN&season=2020%2F2021',
            'https://www.fotmob.com/api/leagues?id=87&ccode3=VEN&season=2019%2F2020',
            'https://www.fotmob.com/api/leagues?id=87&ccode3=VEN&season=2018%2F2019',
            'https://www.fotmob.com/api/leagues?id=87&ccode3=VEN&season=2017%2F2018',
            'https://www.fotmob.com/api/leagues?id=87&ccode3=VEN&season=2016%2F2017',   
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        matches = data['matches']
        season = data['details']['selectedSeason']

        for rounds in matches['allMatches']:
            calendario_items = LigascraperGames()
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
                calendario_items['marcador'] = 'Sin Jugar'
                calendario_items['visitante'] = rounds['away']['name']
                yield calendario_items