import scrapy
import json
from ..items import BplscraperTable, BplscraperMatches, BplscraperMatchesLasted, BplscraperStats 


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

        for rounds in matches['allMatches']:
            calendario_items = BplscraperMatches()
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
    name = 'bpl_matches_lasted'
    allowed_domains = ["fotmob.com/"]
    start_urls = ['https://www.fotmob.com/api/leagues?id=47&ccode3=VEN&season=2022%2F2023']

    custom_settings = {
            'FEEDS': { './bplscraper/spiders/data/2022_2023_calendario_y_resultados.json': { 'format': 'json', 'overwrite': True}
                }
            }
    
    def parse(self, response):
        data = json.loads(response.body)
        matches = data['matches']
        season = data['details']['selectedSeason']

        calendario_items = BplscraperMatchesLasted()

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
        


class BplPlayerStats(scrapy.Spider):
    name = 'bpl_stats'
    allowed_domains = ["fotmob.com/"]
    start_urls = ['https://www.fotmob.com/api/leagueseasondeepstats?id=47&season=20720&type=players&stat=goals&slug=premier-league-players']
    custom_settings = {
            'FEEDS': { f'./bplscraper/spiders/data/players/2023_2024_goals.json': { 'format': 'json', 'overwrite': True}
                }
            }
    
    def parse(self, response):
        data = json.loads(response.body)
        stats = data['statsData']

        player_stats = BplscraperStats()
        
        for item in stats:
            if item['rank'] <= 10:
                player_stats['goleadores'] = {
                    'rank': item['rank'],
                    'nombre_jugador': item['name'],
                    'goles': item['statValue']['value'],
                    'equipo': item['teamId'],
                }
                # player_stats['rank'] = item['rank']
                # player_stats['nombre_jugador'] = item['name']
                # player_stats['goles'] = item['statValue']['value']
                # player_stats['equipo'] = item['teamId']
                yield player_stats
            else:
                break