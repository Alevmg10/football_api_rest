# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from premier_league.models import BplGames, BplTable, BplTeamsGoalsData
from .items import BplscraperGames, BplscraperStats, BplscraperTable
from asgiref.sync import sync_to_async
from scrapy.exceptions import DropItem


class BplscraperPipeline:
    async def process_item(self, item, spider):
        if isinstance(item, BplscraperTable):
            table, _ = await sync_to_async(BplTable.objects.get_or_create)(
                season=item['temporada'],
                position=item['posicion'],
                team=item['equipo'],
                points=item['puntos'],
                played=item['jugados'],
                wins=item['ganados'],
                draw=item['empates'],
                losses=item['perdidos'],
                goal_diff=item['gol_dif'],
            )
            # Si el equipo no esta creado, lo guarda
            return {
                'table': self.model_to_dict(table)  # Convierte la tabla en un diccionario
            }
        
        if isinstance(item, BplscraperGames):
            # Split the 'marcador' field
            home_score, away_score = map(int, item['marcador'].split('-'))
        
            # Create or update the BplGames object
            match_instance, _ = await sync_to_async(BplGames.objects.get_or_create)(
                season=item['temporada'],
                round_number=item['ronda'],
                home_team=item['local'],
                away_team=item['visitante'],
                defaults={
                    'home_score': home_score,
                    'away_score': away_score,
                }
            )
            return {
                'match_instance': self.model_to_dict(match_instance)
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


# class BplTeamsGoalsPipeline:
#     def process_item(self, item, spider):
#         # Extract data from the scraped item
#         local = item['local']
#         visitante = item['visitante']
#         marcador = item['marcador']

        # # Calculate goals scored and conceded
        # goles_local, goles_visitante = map(int, marcador.split('-'))

        # # Update BplTeamsGoalsData model
        # local_team, _ = BplTeamsGoalsData.objects.get_or_create(nombre=local)
        # local_team.goles_anotados += goles_local
        # local_team.goles_recibidos += goles_visitante
        # local_team.save()

#         visitante_team, _ = BplTeamsGoalsData.objects.get_or_create(nombre=visitante)
#         visitante_team.goles_anotados += goles_visitante
#         visitante_team.goles_recibidos += goles_local
#         visitante_team.save()

#         return item













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
