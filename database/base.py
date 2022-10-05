from typing import Dict, List, Optional, Union

from aiomysql.pool import Pool, create_pool
from aiomysql.cursors import DictCursor

from config.models import Settings


class Base:
    def __init__(self, config: Settings) -> None:
        self.__config = config
        self.__pool: Pool = None
    
    async def create_pool(self) -> Pool:
        '''Create mysql pool'''
        if not self.__pool:
            self.__pool = await create_pool(
                host=self.__config.host,
                port=self.__config.port,
                user=self.__config.user,
                password=self.__config.password.get_secret_value(),
                db=self.__config.name,
                minsize=self.__config.min_pool,
                maxsize=self.__config.max_pool
            )
        return self.__pool
    
    async def close_pool(self) -> None:
        if self.__pool:
            self.__pool.close()
            await self.__pool.wait_closed()
    
    async def fetchall(self, query: str, params: Optional[List] = None) -> Union[List[Dict], None]:
        '''Execute fetchall query'''
        async with self.__pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(query, params)
                return await cursor.fetchall()
    
    async def fetchone(self, query: str, params: Optional[List] = None) -> Union[Dict, None]:
        '''Execute fetchone query'''
        async with self.__pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(query, params)
                return await cursor.fetchone()