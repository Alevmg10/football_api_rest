# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import pytz
from premier_league.models import BplTable, BplMatchesAll
from brasil_a.models import BrasilATable, BrasilANextMatches
from la_liga.models import LaligaTable, LaLigaGamesAll
from .items import BplscraperGames, BplscraperTable
from .items import BrasilascraperTable, BrasilascraperNextMatches
from .items import LigascraperGames, LigascraperTable
from asgiref.sync import sync_to_async
from scrapy.exceptions import DropItem


def model_to_dict(model_instance):
    """
    Convert a Django model instance to a dictionary.
    """
    return {
        field.name: getattr(model_instance, field.name)
        for field in model_instance._meta.fields
    }


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
                'table': model_to_dict(table)  # Convierte la tabla en un diccionario
            }
        
        if isinstance(item, BplscraperGames):
            # Extrae los datos
            season = item['temporada']
            date_time_str = item['fecha']
            round_number = item['ronda']
            home_team = item['local']
            away_team = item['visitante']
            score_str = item.get('marcador', None)

            # Default score
            home_score = "Sin Jugar"
            away_score = "Sin Jugar"

            # Actualiza "score" si esta disponible
            if score_str:
                try:
                    home_score, away_score = map(int, score_str.split('-'))
                except ValueError:
                    pass  # Si "score" es un formato invalido, se usara el dafault
            
            # Convierte date_time_str para poder usarse correctamente
            utc_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%SZ')

            # Convierte tiempo UTC en timepo venezolano
            utc_zone = pytz.utc
            venezuela_zone = pytz.timezone('America/Caracas')
            utc_time = utc_zone.localize(utc_time)
            venezuela_time = utc_time.astimezone(venezuela_zone)
            venezuela_time_clean = venezuela_time.replace(tzinfo=None)           
            
            # Crea o actualiza el objeto en BplMatchesAll
            match_instance, _ = await sync_to_async(BplMatchesAll.objects.get_or_create)(
                season=season,
                round_number=round_number,
                date_time=venezuela_time_clean,
                home_team=home_team,
                away_team=away_team,
                defaults={
                    'home_score': home_score,
                    'away_score': away_score,
                }
            )
            return {
                    'match_instance': model_to_dict(match_instance)
                }

        return item

    
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
                'table': model_to_dict(table)  # Convierte la tabla en un diccionario
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
            # Si el equipo no esta creado, lo guarda
            return {
                'table': model_to_dict(table)  # Convierte la tabla en un diccionario
            }
        
        if isinstance(item, LigascraperGames):
            # Extrae los datos
            season = item['temporada']
            date_time_str = item['fecha']
            round_number = item['ronda']
            home_team = item['local']
            away_team = item['visitante']
            score_str = item.get('marcador', None)

            # Default score
            home_score = "Sin Jugar"
            away_score = "Sin Jugar"

            # Actualiza "score" si esta disponible
            if score_str:
                try:
                    home_score, away_score = map(int, score_str.split('-'))
                except ValueError:
                    pass  # Si "score" es un formato invalido, se usara el dafault
            
            # Convierte date_time_str para poder usarse correctamente
            utc_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%SZ')

            # Convierte tiempo UTC en timepo venezolano
            utc_zone = pytz.utc
            venezuela_zone = pytz.timezone('America/Caracas')
            utc_time = utc_zone.localize(utc_time)
            venezuela_time = utc_time.astimezone(venezuela_zone)
            venezuela_time_clean = venezuela_time.replace(tzinfo=None)           
            
            # Crea o actualiza el objeto en BplMatchesAll
            match_instance, _ = await sync_to_async(LaLigaGamesAll.objects.get_or_create)(
                season=season,
                round_number=round_number,
                date_time=venezuela_time_clean,
                home_team=home_team,
                away_team=away_team,
                defaults={
                    'home_score': home_score,
                    'away_score': away_score,
                }
            )
            return {
                    'match_instance': model_to_dict(match_instance)
                }

        return item