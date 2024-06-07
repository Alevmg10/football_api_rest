import scrapy
import json
from datetime import datetime, timedelta
from ..items import BplscraperTable, BplscraperGames
from ..items import LigascraperTable, LigascraperGames
from ..items import BrasilascraperTable, BrasilascraperNextMatches


class BplTable(scrapy.Spider):
    name = "bpl_table"
    allowed_domains = ["fotmob.com/"]
    start_urls = ["https://www.fotmob.com/api/leagues?id=47&ccode3=VEN"]

    # custom_settings = {
    #     'FEEDS': { './bplscraper/spiders/data/tabla_posiciones.json': { 'format': 'json', 'overwrite': True},
    #                 './bplscraper/spiders/data/tabla_posiciones.csv': {'format': 'csv', 'overwrite': True},
    #                 }
    #     }
    
    def parse(self, response):
        data = json.loads(response.body)
        table_data = data["table"]
        season = data['details']['selectedSeason']

        for team in table_data:
            team_data = team["data"]  # Accediendo al diccionario de datos del equipo

            for elemento in team_data["table"]["all"]:
                elementos = BplscraperTable(
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


class BplGames(scrapy.Spider):
    name = 'bpl_games'
    allowed_domains = ["fotmob.com/"]
    #start_urls = ["https://www.fotmob.com/api/leagues?id=47&ccode3=VEN"]


    # custom_settings = {
    #     'FEEDS': { './bplscraper/spiders/data/todas_las_jornadas.json': { 'format': 'json', 'overwrite': True},
    #                 './bplscraper/spiders/data/todas_las_jornadas.csv': {'format': 'csv', 'overwrite': True},
    #                 }
    #     }
    
    def start_requests(self):
        urls = [
            'https://www.fotmob.com/api/leagues?id=47&ccode3=VEN',
            'https://www.fotmob.com/api/leagues?id=47&ccode3=VEN&season=2022%2F2023',
            'https://www.fotmob.com/api/leagues?id=47&ccode3=VEN&season=2021%2F2022',
            'https://www.fotmob.com/api/leagues?id=47&ccode3=VEN&season=2020%2F2021',
            'https://www.fotmob.com/api/leagues?id=47&ccode3=VEN&season=2019%2F2020',
            'https://www.fotmob.com/api/leagues?id=47&ccode3=VEN&season=2018%2F2019',
            'https://www.fotmob.com/api/leagues?id=47&ccode3=VEN&season=2017%2F2018',
            'https://www.fotmob.com/api/leagues?id=47&ccode3=VEN&season=2016%2F2017',
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        matches = data['matches']
        seasons = data['details']['selectedSeason']
        for rounds in matches['allMatches']:
            calendario_items = BplscraperGames()
            calendario_items['temporada'] = seasons
            calendario_items['fecha'] = rounds['status']['utcTime']
            calendario_items['ronda'] = rounds['round']
            calendario_items['local'] = rounds['home']['name']
            calendario_items['visitante'] = rounds['away']['name']

            if rounds["status"].get("finished") or rounds["status"].get("scoreStr"):
                calendario_items['marcador'] = rounds['status'].get('scoreStr', 'Sin Jugar')
            else:
                calendario_items['marcador'] = 'Sin Jugar'

            yield calendario_items


class LaligaTable(scrapy.Spider):
    name = "laliga_table"
    allowed_domains = ["fotmob.com/"]
    start_urls = ["https://www.fotmob.com/api/leagues?id=87&ccode3=VEN"]

    # custom_settings = {
    #     'FEEDS': { './laligascraper/spiders/data/tabla_posiciones.json': { 'format': 'json', 'overwrite': True},
    #                 './laligascraper/spiders/data/tabla_posiciones.csv': {'format': 'csv', 'overwrite': True},
    #                 }
    #     }
    
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
        seasons = data['details']['selectedSeason']
        for rounds in matches['allMatches']:
            calendario_items = LigascraperGames()
            calendario_items['temporada'] = seasons
            calendario_items['fecha'] = rounds['status']['utcTime']
            calendario_items['ronda'] = rounds['round']
            calendario_items['local'] = rounds['home']['name']
            calendario_items['visitante'] = rounds['away']['name']

            if rounds["status"].get("finished") or rounds["status"].get("scoreStr"):
                calendario_items['marcador'] = rounds['status'].get('scoreStr', 'Sin Jugar')
            else:
                calendario_items['marcador'] = 'Sin Jugar'

            yield calendario_items


class BrasilATable(scrapy.Spider):
    name = "brasila_table"
    allowed_domains = ["fotmob.com/"]
    start_urls = ["https://www.fotmob.com/api/leagues?id=268&ccode3=VEN"]

    def parse(self, response):
        data = json.loads(response.body)
        table_data = data["table"]
        season = data['details']['selectedSeason']

        for team in table_data:
            team_data = team["data"]  # Accediendo al diccionario de datos del equipo

            for elemento in team_data["table"]["all"]:
                elementos = BrasilascraperTable(
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


class BrasilANextMatches(scrapy.Spider):
    name = "brasila_next_matches"
    allowed_domains = ["fotmob.com/"]
    start_urls = ["https://www.fotmob.com/api/leagues?id=268&ccode3=VEN"]
        
    def parse(self, response):
        data = json.loads(response.body)
        matches = data['matches']['allMatches']
        seasons = data['details']['selectedSeason']
        today = datetime.now()
        end_date = today + timedelta(days=6)

        for match in matches:
            match_date = datetime.strptime(match['status']['utcTime'], '%Y-%m-%dT%H:%M:%SZ')
            if today <= match_date <= end_date:
                item = BrasilascraperNextMatches()
                item['temporada'] = seasons
                item['fecha'] = match['status']['utcTime']
                item['ronda'] = match['round']
                item['local'] = match['home']['name']
                item['visitante'] = match['away']['name']
                item['marcador'] = match['status'].get('scoreStr', 'Sin Jugar')
                yield item