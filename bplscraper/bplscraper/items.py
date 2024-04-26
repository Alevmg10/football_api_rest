# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BplscraperTable(scrapy.Item):
    temporada = scrapy.Field()
    posicion = scrapy.Field()
    equipo = scrapy.Field()
    puntos = scrapy.Field()
    jugados = scrapy.Field()
    ganados = scrapy.Field()
    empates = scrapy.Field()
    perdidos = scrapy.Field()
    gol_dif = scrapy.Field() 
    

class BplscraperGames(scrapy.Item):
    temporada = scrapy.Field()
    ronda = scrapy.Field()
    local = scrapy.Field()
    marcador = scrapy.Field()
    visitante = scrapy.Field()


class BplscraperStats(scrapy.Item):
    goleadores = scrapy.Field()
    rank = scrapy.Field()
    nombre_jugador = scrapy.Field()
    goles = scrapy.Field()
    equipo = scrapy.Field()