# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from premier_league.models import Match, Table
from .items import BplscraperMatches, BplscraperStats, BplscraperTable
from asgiref.sync import sync_to_async
from scrapy.exceptions import DropItem


class BplscraperPipeline:
    async def process_item(self, item, spider):
        if isinstance(item, BplscraperTable):
            table, _ = await sync_to_async(Table.objects.get_or_create)(
                season=item['temporada'],
                position=item['posicion'],
                team=item['equipo'],
                points=item['puntos'],
                played=item['jugados'],
                wins=item['ganados'],
                draw=item['empates'],
                losses=item['perdidos'],
            )
            # Save the team if it doesn't exist already
            return {
                'table': self.model_to_dict(table)  # Convert the Table object to a dictionary
            }

        if isinstance(item, BplscraperMatches):
            match = await sync_to_async(Match.objects.create)(
                temporada=item['temporada'],
                round_number=item['ronda'],
                home_team=item['local'],
                score=item['marcador'],
                away_team=item['visitante']
            )
            return {
                'match': self.model_to_dict(match)  # Convert the Match object to a dictionary
            }

        # If the item type is not recognized, drop it
        raise DropItem(f"Unsupported item type: {type(item)}")

    def model_to_dict(self, model_instance):
        """
        Convert a Django model instance to a dictionary.
        """
        return {
            field.name: getattr(model_instance, field.name)
            for field in model_instance._meta.fields
        }


# class BplscraperPipeline:
#     def process_item(self, item, spider):
#         if isinstance(item, BplscraperTable):
#             team, _ = Table.objects.get_or_create(team=item['equipo'])
#             # Save the team if it doesn't exist already
#             return team

#         if isinstance(item, BplscraperMatches):
#             match = Match.objects.create(
#                 temporada=item['temporada'],
#                 round_number=item['ronda'],
#                 home_team=item['local'],
#                 score=item['marcador'],
#                 away_team=item['visitante']
#             )
#             return match

        # if isinstance(item, BplscraperStats):
        #     player, _ = Player.objects.get_or_create(name=item['nombre_jugador'], team=team)
        #     # Save the player if it doesn't exist already
        #     goalscorer = GoalScorer.objects.create(player=player, goals=item['goles'])
        #     return goalscorer

# class BplscraperPipeline:
#     def process_item(self, item, spider):
#         return item