from typing import Dict, List, Optional, Union

from .base import Base
from config.models import Settings

from humanize import precisedelta, i18n, naturaltime


class Engine(Base):
    def __init__(self, config: Settings) -> None:
        super().__init__(config)
        _t = i18n.activate("ru_RU")
    
    async def get_top_kills(self, limit: Optional[int] = 3, offset: Optional[int] = 0) -> List[Dict]:
        '''Get top 3 players sorted by kills'''
        query = 'SELECT * FROM csstats ORDER BY kills DESC LIMIT %s OFFSET %s'
        return await self.fetchall(query=query, params=[limit, offset])
    
    async def get_top_skill(self, limit: Optional[int] = 3, offset: Optional[int] = 0) -> List[Dict]:
        '''Get top 3 players sorted by skill'''
        query = 'SELECT * FROM csstats ORDER BY skill DESC LIMIT %s OFFSET %s'
        return await self.fetchall(query=query, params=[limit, offset])
    
    async def get_top_damage(self, limit: Optional[int] = 3, offset: Optional[int] = 0) -> List[Dict]:
        '''Get top 3 players sorted by damage'''
        query = 'SELECT * FROM csstats ORDER BY dmg DESC LIMIT %s OFFSET %s'
        return await self.fetchall(query=query, params=[limit, offset])
    
    async def get_top_players(self, limit: Optional[int] = 15, offset: Optional[int] = 0) -> List[Dict]:
        '''Get player stats by id'''
        query = "SELECT * FROM csstats ORDER BY skill DESC LIMIT %s OFFSET %s"
        return await self.fetchall(query=query, params=[limit, offset])
    
    async def get_player(self, player_id: int) -> Union[Dict, None]:
        '''Get player stats by id'''
        query = 'SELECT * FROM csstats WHERE id = %s'
        return await self.fetchone(query=query, params=[player_id])
    
    def set_skill_to_players(self, players: List[Dict]) -> List[Dict]:
        for player in players:
            skill = self._calculate_skill(skill=player['skill'])
            player['skill_text'] = f"{skill} ({player['skill']})"
        return players
    
    def _calculate_skill(self, skill: Union[int, float]) -> str:
        '''Calculate skill (L LS L+)'''
        if skill < 60:
            return f'L-'
        elif skill >= 60 and skill < 75:
            return f'LS'
        elif skill >= 75 and skill < 85:
            return f'L+'
        elif skill >= 85 and skill < 100:
            return f'M-'
        elif skill >= 100 and skill < 115:
            return f'MS'
        elif skill >= 115 and skill < 130:
            return f'M+'
        elif skill >= 130 and skill < 140:
            return f'H-'
        elif skill >= 140 and skill < 150:
            return f'HS'
        elif skill >= 150 and skill < 165:
            return f'H+'
        elif skill >= 165 and skill < 180:
            return f'P-'
        elif skill >= 180 and skill < 195:
            return f'PS'
        elif skill >= 195 and skill < 210:
            return f'P+'
        elif skill >= 210:
            return f'G'
        else:
            return 'MEGA GOOD'