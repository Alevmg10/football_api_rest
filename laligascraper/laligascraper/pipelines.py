# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from la_liga.models import LaligaMatch, LaligaTable
from .items import LigascraperMatches, LigascraperStats, LigascraperTable
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

        if isinstance(item, LigascraperMatches):
            match = await sync_to_async(LaligaMatch.objects.create)(
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