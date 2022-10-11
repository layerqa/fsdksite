from curses.panel import top_panel
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import config
from database import Engine


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

db = Engine(config=config)


@app.on_event(event_type='startup')
async def startup_event():
    await db.create_pool()

@app.on_event(event_type='shutdown')
async def shutdown_event():
    await db.close_pool()


@app.get(path='/stats', response_class=HTMLResponse)
@app.get(path='/', response_class=HTMLResponse)
async def main_page(request: Request) -> HTMLResponse:
    context = {'request': request}
    return templates.TemplateResponse(name='stats.html', context=context)


@app.get(path='/bans', response_class=HTMLResponse)
async def bans_page(request: Request) -> HTMLResponse:
    context = {'request': request}
    return templates.TemplateResponse(name='bans.html', context=context)


@app.get(path='/api/stats', response_class=JSONResponse)
async def stats_api(request: Request) -> JSONResponse:
    top_players = await db.get_top_players()
    return {
        'top_kill': await db.get_top_kills(),
        'top_skill': await db.get_top_skill(),
        'top_damage': await db.get_top_damage(),
        'top_players': db.set_skill_to_players(players=top_players)
    }


@app.post(path='/search_stats')
async def search_stats(search_stats_form: str = Form(...)):
    print(search_stats_form)
    return {"1": 1}