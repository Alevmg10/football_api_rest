# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from premier_league.models import Team, Match, Player, GoalScorer
from items import BplscraperMatches, BplscraperStats, BplscraperTable

class DjangoPipeline:
    def process_item(self, item, spider):
        if isinstance(item, BplscraperTable):
            team, _ = Team.objects.get_or_create(name=item['equipo'])
            # Save the team if it doesn't exist already

        if isinstance(item, BplscraperMatches):
            match = Match.objects.create(
                temporada=item['temporada'],
                round_number=item['ronda'],
                home_team=item['local'],
                score=item['marcador'],
                away_team=item['visitante']
            )
            return match

        # if isinstance(item, BplscraperStats):
        #     player, _ = Player.objects.get_or_create(name=item['nombre_jugador'], team=team)
        #     # Save the player if it doesn't exist already
        #     goalscorer = GoalScorer.objects.create(player=player, goals=item['goles'])
        #     return goalscorer


# class BplscraperPipeline:
#     def process_item(self, item, spider):
#         return item
