# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from la_liga.models import LaligaGames, LaligaTable
from .items import LigascraperGames, LigascraperStats, LigascraperTable
from asgiref.sync import sync_to_async
from scrapy.exceptions import DropItem


class LaligascraperPipeline:
    async def process_item(self, item, spider):
        if isinstance(item, LigascraperTable):
            table, _ = await sync_to_async(LaligaTable.objects.get_or_create)(
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
            # Save the team if it doesn't exist already
            return {
                'table': self.model_to_dict(table)  # Convert the Table object to a dictionary
            }

        if isinstance(item, LigascraperGames):
            # Separar campo 'marcador'
            home_score, away_score = map(int, item['marcador'].split('-'))
        
            # Create or update the BplGames object
            match_instance, _ = await sync_to_async(LaligaGames.objects.get_or_create)(
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