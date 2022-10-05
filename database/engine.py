from typing import Dict, List, Optional, Union

from .base import Base
from config.models import Settings

from humanize import precisedelta, i18n


class Engine(Base):
    def __init__(self, config: Settings) -> None:
        super().__init__(config)
        _t = i18n.activate("ru_RU")
    
    async def get_top_kills(self, limit: Optional[int] = 3) -> List[Dict]:
        '''Get top 3 players sorted by kills'''
        query = 'SELECT * FROM csstats ORDER BY kills DESC LIMIT %s'
        return await self.fetchall(query=query, params=[limit])
    
    async def get_top_skill(self, limit: Optional[int] = 3) -> List[Dict]:
        '''Get top 3 players sorted by skill'''
        query = 'SELECT * FROM csstats ORDER BY skill DESC LIMIT %s'
        return await self.fetchall(query=query, params=[limit])
    
    async def get_top_damage(self, limit: Optional[int] = 3) -> List[Dict]:
        '''Get top 3 players sorted by damage'''
        query = 'SELECT * FROM csstats ORDER BY dmg DESC LIMIT %s'
        return await self.fetchall(query=query, params=[limit])
    
    async def get_player_and_weapons(self, player_id: int) -> Union[List[Dict], None]:
        '''Get player stats by id'''
        query = """
        SELECT
            csstats.*, 
            csstats_weapons.weapon, 
            csstats_weapons.kills AS weapon_kills, 
            csstats_weapons.shots AS weapon_shots, 
            csstats_weapons.hs AS weapon_hs, 
            csstats_weapons.dmg AS weapon_dmg, 
            csstats_weapons.hits AS weapon_hits
        FROM
            csstats
            INNER JOIN
            csstats_weapons
            ON 
                csstats.id = csstats_weapons.player_id
        WHERE
            csstats.id = %s AND
            csstats_weapons.shots IS NOT NULL AND
            csstats_weapons.kills IS NOT NULL
        ORDER BY
            weapon_kills DESC
        """
        return await self.fetchall(query=query, params=[player_id])
    
    async def get_player(self, player_id: int) -> Union[Dict, None]:
        '''Get player stats by id'''
        query = 'SELECT * FROM csstats WHERE id = %s'
        return await self.fetchone(query=query, params=[player_id])
    
    def _calculate_skill(self, skill: Union[int, float]) -> str:
        '''Calculate skill (L LS L+)'''
        if skill < 60:
            return f'L- ({skill})'
        elif skill >= 60 and skill < 75:
            return f'LS ({skill})'
        elif skill >= 75 and skill < 85:
            return f'L+ ({skill})'
        elif skill >= 85 and skill < 100:
            return f'M- ({skill})'
        elif skill >= 100 and skill < 115:
            return f'MS ({skill})'
        elif skill >= 115 and skill < 130:
            return f'M+ ({skill})'
        elif skill >= 130 and skill < 140:
            return f'H- ({skill})'
        elif skill >= 140 and skill < 150:
            return f'HS ({skill})'
        elif skill >= 150 and skill < 165:
            return f'H+ ({skill})'
        elif skill >= 165 and skill < 180:
            return f'P- ({skill})'
        elif skill >= 180 and skill < 195:
            return f'PS ({skill})'
        elif skill >= 195 and skill < 210:
            return f'P+ ({skill})'
        elif skill >= 210:
            return f'G ({skill})'
        else:
            return 'MEGA GOOD'
    
    def _add_skill_human_to_player(self, player: Dict) -> Dict:
        '''Add human skill to player'''
        player['human_skill'] = self._calculate_skill(skill=player['skill'])
        return player

    def _add_badges_to_players(self, players: List[Dict]) -> List[Dict]:
        '''Add cups to player top'''
        cup_number = 1
        players_response = []
        for player in players:
            player['cup'] = f'cup{cup_number}'
            player['human_skill'] = self._calculate_skill(
                skill=player['skill']
            )
            players_response.append(player)
            cup_number += 1
        return players_response
    
    def _parse_top_players(self, players: List[Dict]) -> List[Dict]:
        '''Add player number'''
        player_number = 1
        players_response = []
        for player in players:
            player['player_number'] = player_number
            player['human_time'] = precisedelta(
                value=player['connection_time'],
                minimum_unit='minutes', format='%0.0f'
            )
            player['human_skill'] = self._calculate_skill(
                skill=player['skill']
            )
            players_response.append(player)
            player_number += 1
        return players_response
