from scipy.stats import poisson
from la_liga.models import LaligaGames
from collections import defaultdict


class Probabilidades:

    def __init__(self, data):
        self.data = data

    def equipos(self):
        equipos = defaultdict(lambda: {'goles_anotados': 0, 'goles_recibidos': 0})

        for partido in self.data:
            equipo_local = partido.home_team
            equipo_visitante = partido.away_team
            goles_local = partido.home_score
            goles_visitante = partido.away_score
            
            equipos[equipo_local]['goles_anotados'] += goles_local
            equipos[equipo_local]['goles_recibidos'] += goles_visitante

            equipos[equipo_visitante]['goles_anotados'] += goles_visitante
            equipos[equipo_visitante]['goles_recibidos'] += goles_local

        return equipos

    def conteo_partidos(self):
        conteo_team = defaultdict(int)
        for partido in self.data:
            equipo_local = partido.home_team
            equipo_visitante = partido.away_team
            conteo_team[equipo_local] += 1
            conteo_team[equipo_visitante] += 1
        return conteo_team

    def promedios(self):
        equipos_data = self.equipos()
        conteo_team = self.conteo_partidos()
        promedios_historicos = []

        for equipo, estadisticas in equipos_data.items():
            promedio_goles_anotados = estadisticas['goles_anotados'] / conteo_team[equipo]
            promedio_goles_recibidos = estadisticas['goles_recibidos'] / conteo_team[equipo]
            promedios_historicos.append({
                "equipo": equipo,
                "promedio_goles_anotados": promedio_goles_anotados,
                "promedio_goles_recibidos": promedio_goles_recibidos
            })
        return promedios_historicos

    def probabilidad(self, home, away):
        promedios = self.promedios()
        prom_anotados_home, prom_recibidos_home = None, None
        prom_anotados_away, prom_recibidos_away = None, None

        for promedio in promedios:
            equipo = promedio["equipo"]
            if home == equipo:
                prom_anotados_home = promedio["promedio_goles_anotados"]
                prom_recibidos_home = promedio["promedio_goles_recibidos"]
            elif away == equipo:
                prom_anotados_away = promedio["promedio_goles_anotados"]
                prom_recibidos_away = promedio["promedio_goles_recibidos"]

        if None in (prom_anotados_home, prom_recibidos_home, prom_anotados_away, prom_recibidos_away):
            return "No se encontraron datos para los equipos proporcionados"

        lambda_home = prom_anotados_home * prom_recibidos_away
        lambda_away = prom_anotados_away * prom_recibidos_home
        prob_home, prob_away, prob_draw = 0, 0, 0 

        for x in range(0, 8):
            for y in range(0, 8):
                p = poisson.pmf(x, lambda_home) * poisson.pmf(y, lambda_away)
                if x == y:
                    prob_draw += p
                elif x > y:
                    prob_home += p
                else:
                    prob_away += p

        total_prob = prob_home + prob_draw + prob_away
        prob_home_percent = prob_home * 100 / total_prob
        prob_draw_percent = prob_draw * 100 / total_prob
        prob_away_percent = prob_away * 100 / total_prob

        return f"{prob_home_percent:.2f}%  ---   {prob_draw_percent:.2f}%  ---  {prob_away_percent:.2f}%"
    
    