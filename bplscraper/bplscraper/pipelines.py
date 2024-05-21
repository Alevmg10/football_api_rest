# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from premier_league.models import BplGames, BplTable, BplMatches, BplMatchesTestAll
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
             # Extract the match data
            season = item['temporada']
            round_number = item['ronda']
            home_team = item['local']
            away_team = item['visitante']
            score_str = item.get('marcador', None)

            # Set default scores
            home_score = "Sin Jugar"
            away_score = "Sin Jugar"

            # Update scores if available
            if score_str:
                try:
                    home_score, away_score = map(int, score_str.split('-'))
                except ValueError:
                    pass  # Score format is invalid, defaults will be used

            # Create or update the BplMatchesTest object
            match_instance, _ = await sync_to_async(BplMatchesTestAll.objects.get_or_create)(
                season=season,
                round_number=round_number,
                home_team=home_team,
                away_team=away_team,
                defaults={
                    'home_score': home_score,
                    'away_score': away_score,
                }
            )

            return {
                    'match_instance': self.model_to_dict(match_instance)
                }

        return item


            # try:
            #     # Separar campo 'marcador'
            #     home_score, away_score = map(int, item['marcador'].split('-'))
        
            #     # Create or update the BplGames object
            #     match_instance, _ = await sync_to_async(BplMatchesTestAll.objects.get_or_create)(
            #         season=item['temporada'],
            #         round_number=item['ronda'],
            #         home_team=item['local'],
            #         away_team=item['visitante'],
            #         defaults={
            #             'home_score': home_score,
            #             'away_score': away_score,
            #         }
            #     )
                # return {
                #     'match_instance': self.model_to_dict(match_instance)
                # }
            # except ValueError:
            #     # Create or update the BplGames object
            #     match_instance, _ = await sync_to_async(BplMatchesTestAll.objects.get_or_create)(
            #         season=item['temporada'],
            #         round_number=item['ronda'],
            #         home_team=item['local'],
            #         away_team=item['visitante'],
            #         defaults={
            #             'home_score': "Sin Jugar",
            #             'away_score': "Sin Jugar",
            #         }
            #     )
            #     return {
            #         'match_instance': self.model_to_dict(match_instance)
            #     }

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
