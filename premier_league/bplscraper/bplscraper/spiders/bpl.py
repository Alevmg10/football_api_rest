import scrapy
import json
from urllib.parse import quote
from ..items import BplscraperTable, BplscraperMatches, BplscraperMatchesLasted


class BplTable(scrapy.Spider):
    name = "bpl_table"
    allowed_domains = ["fotmob.com/"]
    start_urls = ["https://www.fotmob.com/api/leagues?id=47&ccode3=VEN"]

    custom_settings = {
        'FEEDS': { './bplscraper/spiders/data/tabla_posiciones.json': { 'format': 'json', 'overwrite': True},
                    './bplscraper/spiders/data/tabla_posiciones.csv': {'format': 'csv', 'overwrite': True},
                    }
        }
    
    def parse(self, response):
        data = json.loads(response.body)
        table_data = data["table"]
        
        for team in table_data:
            team_data = team["data"]  # Accediendo al diccionario de datos del equipo
        
        elementos = BplscraperTable()
        for elemento in team_data["table"]["all"]:
            elementos['posicion'] = elemento["idx"]
            elementos['equipo'] = elemento["name"]  
            elementos['puntos'] = elemento["pts"]
            elementos['jugados'] = elemento["played"]
            elementos['ganados'] = elemento["wins"]
            elementos['perdidos'] = elemento["losses"]
            elementos['empates'] = elemento["draws"]
            yield elementos


class BplMatches(scrapy.Spider):
    name = 'bpl_matches'
    allowed_domains = ["fotmob.com/"]
    start_urls = ['https://www.fotmob.com/api/leagues?id=47&ccode3=VEN']

    custom_settings = {
        'FEEDS': { './bplscraper/spiders/data/calendario_y_resultados.json': { 'format': 'json', 'overwrite': True},
                    './bplscraper/spiders/data/calendario_y_resultados.csv': {'format': 'csv', 'overwrite': True},
                    }
        }

    def parse(self, response):
        data = json.loads(response.body)
        matches = data['matches']
        season = data['details']['selectedSeason']

        calendario_items = BplscraperMatches()

        for rounds in matches['allMatches']:
            if not rounds["status"]["cancelled"]:
                try:
                    calendario_items['temporada'] = season
                    calendario_items['ronda'] = rounds['round']
                    calendario_items['local'] = rounds['home']['shortName']
                    calendario_items['marcador'] = rounds['status']['scoreStr']
                    calendario_items['visitante'] = rounds['away']['shortName']
                    yield calendario_items
                except KeyError:
                    pass
            else:
                calendario_items['temporada'] = season
                calendario_items['ronda'] = rounds['round']
                calendario_items['local'] = rounds['home']['shortName']
                calendario_items['marcador'] = 'Pospuesto'
                calendario_items['visitante'] = rounds['away']['shortName']
                yield calendario_items


class BplMatchesLastedSeason(scrapy.Spider):
    name = 'bpl_matches_lasted'
    allowed_domains = ["fotmob.com/"]
    start_urls = ['https://www.fotmob.com/api/leagues?id=47&ccode3=VEN&season=2016%2F2017']

    custom_settings = {
            'FEEDS': { f'./bplscraper/spiders/data/2016_2017_calendario_y_resultados.json': { 'format': 'json', 'overwrite': True}
                }
            }
    
    def parse(self, response):
        data = json.loads(response.body)
        matches = data['matches']
        season = data['details']['selectedSeason']

        calendario_items = BplscraperMatches()

        for rounds in matches['allMatches']:
            if not rounds["status"]["cancelled"]:
                try:
                    calendario_items['temporada'] = season
                    calendario_items['ronda'] = rounds['round']
                    calendario_items['local'] = rounds['home']['shortName']
                    calendario_items['marcador'] = rounds['status']['scoreStr']
                    calendario_items['visitante'] = rounds['away']['shortName']
                    yield calendario_items
                except KeyError:
                    pass
            else:
                calendario_items['temporada'] = season
                calendario_items['ronda'] = rounds['round']
                calendario_items['local'] = rounds['home']['shortName']
                calendario_items['marcador'] = 'Pospuesto'
                calendario_items['visitante'] = rounds['away']['shortName']
                yield calendario_items
        


class BplPlayerStats(scrapy.Spider):
    pass