# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
from premier_league.models import BplGames, BplTable, BplMatches, BplMatchesTestAll
from brasil_a.models import BrasilATable, BrasilANextMatches
from .items import BplscraperGames, BplscraperStats, BplscraperTable, BrasilascraperTable, BrasilascraperNextMatches
from .items import LigascraperGames, LigascraperStats, LigascraperTable
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
    
    def model_to_dict(self, model_instance):
        """
        Convert a Django model instance to a dictionary.
        """
        return {
            field.name: getattr(model_instance, field.name)
            for field in model_instance._meta.fields
        }
    
class BrasilascraperPipeline:
    async def process_item(self, item, spider):
        if isinstance(item, BrasilascraperTable):
            table, _ = await sync_to_async(BrasilATable.objects.get_or_create)(
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
        
        if isinstance(item, BrasilascraperNextMatches):
            try:
                # Parse the date_time field
                date_time = datetime.strptime(item['fecha'], '%Y-%m-%dT%H:%M:%SZ')

                # Parse the marcador field if available
                if item['marcador'] != 'Sin Jugar':
                    home_score, away_score = map(int, item['marcador'].split('-'))
                else:
                    home_score, away_score = None, None

                # Create or update the BrasilANextMatches object
                match_instance, created = await sync_to_async(BrasilANextMatches.objects.get_or_create)(
                    season=item['temporada'],
                    date_time=date_time,
                    round_number=item['ronda'],
                    home_team=item['local'],
                    away_team=item['visitante'],
                    defaults={
                        'home_score': home_score,
                        'away_score': away_score,
                    }
                )

                if not created:
                    # Update the existing match instance if it wasn't created
                    match_instance.home_score = home_score
                    match_instance.away_score = away_score
                    await sync_to_async(match_instance.save)()

                return item

            except ValueError as e:
                spider.logger.error(f"ValueError: {e}")
                raise DropItem(f"Invalid data format: {item}")

        return item

    def model_to_dict(self, model_instance):
        """
        Convert a Django model instance to a dictionary.
        """
        return {
            field.name: getattr(model_instance, field.name)
            for field in model_instance._meta.fields
        }