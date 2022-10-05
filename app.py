import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import config
from database import Engine


logger = logging.getLogger(name='FSDK-APP')

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

db = Engine(config=config)


@app.on_event(event_type='startup')
async def startup_event():
    await db.create_pool()
    logger.info(msg='Database pool created')


@app.on_event(event_type='shutdown')
async def shutdown_event():
    await db.close_pool()
    logger.info(msg='Database pool closed')


@app.get(path='/', response_class=HTMLResponse)
async def main_page(request: Request) -> HTMLResponse:
    top_kills = await db.get_top_kills()
    top_skill = await db.get_top_skill()
    top_damage = await db.get_top_damage()
    top_players = await db.get_top_skill(limit=20)
    context ={
        'request': request,
        'top_kills': db._add_badges_to_players(players=top_kills),
        'top_skill': db._add_badges_to_players(players=top_skill),
        'top_damage': db._add_badges_to_players(players=top_damage),
        'top_players': db._parse_top_players(players=top_players)
    }
    return templates.TemplateResponse(name='index.html', context=context)


@app.get(path='/player', response_class=HTMLResponse)
async def player_page(request: Request, player_id: int) -> HTMLResponse:
    try:
        player = await db.get_player_and_weapons(player_id=player_id)
        top_kills = await db.get_top_kills()
        top_skill = await db.get_top_skill()
        top_damage = await db.get_top_damage()
        context ={
            'request': request,
            'top_kills': db._add_badges_to_players(players=top_kills),
            'top_skill': db._add_badges_to_players(players=top_skill),
            'top_damage': db._add_badges_to_players(players=top_damage)
        }
        if player:
            context['weapons'] = player
            context['player'] = db._add_skill_human_to_player(player=player[0])
        else:
            only_player = await db.get_player(player_id=player_id)
            context['player'] = db._add_skill_human_to_player(player=only_player)
        return templates.TemplateResponse(name='player.html', context=context)
    except Exception as e:
        logger.error(e)
        return templates.TemplateResponse(name='404.html', context={'request': request})