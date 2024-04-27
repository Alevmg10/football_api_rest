import scrapy
import json
from ..items import BplscraperTable, BplscraperGames


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
        season = data['details']['selectedSeason']

        for rounds in matches['allMatches']:
            calendario_items = BplscraperGames()
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
                calendario_items['marcador'] = 'Sin jugar'
                calendario_items['visitante'] = rounds['away']['name']
                yield calendario_items


class CurrentRoundMatches(scrapy.Spider):
    name = "bpl_current_matches"
    allowed_domains = ["fotmob.com/"]
    start_urls = ["https://www.fotmob.com/api/leagues?id=47&ccode3=VEN"]

    custom_settings = {
        'FEEDS': { './bplscraper/spiders/data/jornada_actual.json': { 'format': 'json', 'overwrite': True},
                    './bplscraper/spiders/data/jornada_actual.csv': {'format': 'csv', 'overwrite': True},
                    }
        }

    def parse(self, response):
        data = json.loads(response.body)
        season = data['details']['selectedSeason']
        current_round = int(data["matches"]["firstUnplayedMatch"]["firstRoundWithUnplayedMatch"])
        matches = data['matches']['allMatches']

        for match in matches:
            round_number = int(match['round'])
            items = BplscraperGames()
            if round_number == current_round:
                try:
                    items['temporada'] = season
                    items['ronda'] = round_number
                    items['local'] = match['home']['name']
                    #items['marcador'] = match['status']['scoreStr']
                    items['visitante'] = match['away']['name']
                    yield items
                except KeyError:
                    pass
            yield items
            



# class BplPlayerStats(scrapy.Spider):
#     name = 'bpl_stats'
#     allowed_domains = ["fotmob.com/"]
#     start_urls = ['https://www.fotmob.com/api/leagueseasondeepstats?id=47&season=20720&type=players&stat=goals&slug=premier-league-players']
#     custom_settings = {
#             'FEEDS': { f'./bplscraper/spiders/data/players/2023_2024_goals.json': { 'format': 'json', 'overwrite': True}
#                 }
#             }
    
#     def parse(self, response):
#         data = json.loads(response.body)
#         stats = data['statsData']

#         player_stats = BplscraperStats()
        
#         for item in stats:
#             if item['rank'] <= 10:
#                 player_stats['goleadores'] = {
#                     'rank': item['rank'],
#                     'nombre_jugador': item['name'],
#                     'goles': item['statValue']['value'],
#                     'equipo': item['teamId'],
#                 }
#                 player_stats['rank'] = item['rank']
#                 player_stats['nombre_jugador'] = item['name']
#                 player_stats['goles'] = item['statValue']['value']
#                 player_stats['equipo'] = item['teamId']
#                 yield player_stats
#             else:
#                 break