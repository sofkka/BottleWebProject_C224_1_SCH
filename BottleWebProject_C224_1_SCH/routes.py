# -*- coding: cp1251 -*-

"""
Routes and views for the bottle application.
"""
from bottle import route, request, response, template, view, static_file
from static.controllers.module3_cells_colonies import GameOfLife
from datetime import datetime, timedelta
import json
import os
import uuid
from static.controllers.module1_wolf_island import wolf_island_controller
import random

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/contact')
@view('contact')
def contact():
    """Renders the contact page."""
    return dict(
        title='Contact',
        message='Your contact page.',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About authors',
        year=datetime.now().year
    )

@route('/wolf_island', method=['GET'])
@view('module1_wolf_island')
def wolf_island():
    action = request.query.get('action', '')
    N = request.query.get('N', '')
    M = request.query.get('M', '')
    rabbits = request.query.get('rabbits', '')
    wolves = request.query.get('wolves', '')
    she_wolves = request.query.get('she_wolves', '')
    steps = request.query.get('steps', '')
    return wolf_island_controller(action, N, M, rabbits, wolves, she_wolves, steps)

@route('/wolf_island', method=['GET'])
@view('module1_wolf_island')
def wolf_island():
    action = request.query.get('action', '')
    N = request.query.get('N', '')
    M = request.query.get('M', '')
    rabbits = request.query.get('rabbits', '')
    wolves = request.query.get('wolves', '')
    she_wolves = request.query.get('she_wolves', '')
    steps = request.query.get('steps', '')
    return wolf_island_controller(action, N, M, rabbits, wolves, she_wolves, steps)

@route('/infection_spread')
@view('module2_infection_spread')
def module2_infection_spread():
    # РР·РІР»РµРєР°РµС‚СЃСЏ РїР°СЂР°РјРµС‚СЂ 'size' РёР· GET-Р·Р°РїСЂРѕСЃР°, Р·Р°РґР°СЋС‰РёР№ СЂР°Р·РјРµСЂ СЃРµС‚РєРё. Р•СЃР»Рё РїР°СЂР°РјРµС‚СЂ РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚ - 9
    size = request.GET.get('size', '9')

    # РР·РІР»РµРєР°РµС‚СЃСЏ РїР°СЂР°РјРµС‚СЂ 'continue_from', СЃРѕРґРµСЂР¶Р°С‰РёР№ JSON-РїСЂРµРґСЃС‚Р°РІР»РµРЅРёРµ СЃРµС‚РєРё РґР»СЏ РїСЂРѕРґРѕР»Р¶РµРЅРёСЏ СЃРёРјСѓР»СЏС†РёРё.
    # Р•СЃР»Рё РїР°СЂР°РјРµС‚СЂ РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚ - None.
    continue_from = request.GET.get('continue_from')

    # РџСЂРѕРІРµСЂСЏРµС‚СЃСЏ РїР°СЂР°РјРµС‚СЂ 'save', РѕРїСЂРµРґРµР»СЏСЋС‰РёР№, РЅСѓР¶РЅРѕ Р»Рё СЃРѕС…СЂР°РЅРёС‚СЊ СЃРѕСЃС‚РѕСЏРЅРёРµ СЃРµС‚РєРё РІ JSON.
    # Р—РЅР°С‡РµРЅРёРµ 'true' РІ Р·Р°РїСЂРѕСЃРµ РїСЂРµРѕР±СЂР°Р·СѓРµС‚СЃСЏ РІ Р±СѓР»РµРІРѕ True, РёРЅР°С‡Рµ False.
    save = request.GET.get('save', 'false') == 'true'

    # РР·РІР»РµРєР°РµС‚СЃСЏ РїР°СЂР°РјРµС‚СЂ 'step', СѓРєР°Р·С‹РІР°СЋС‰РёР№ С‚РµРєСѓС‰РёР№ С€Р°Рі СЃРёРјСѓР»СЏС†РёРё. Р•СЃР»Рё РїР°СЂР°РјРµС‚СЂ РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚, РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ 0.
    step = int(request.GET.get('step', '0'))

    # РџСЂРѕРІРµСЂСЏРµС‚СЃСЏ РєРѕСЂСЂРµРєС‚РЅРѕСЃС‚СЊ РїР°СЂР°РјРµС‚СЂР° size Рё РїСЂРµРѕР±СЂР°Р·СѓРµС‚СЃСЏ РІ С†РµР»РѕРµ С‡РёСЃР»Рѕ.
    try:
        # РџР°СЂР°РјРµС‚СЂ size РїСЂРµРѕР±СЂР°Р·СѓРµС‚СЃСЏ РІ С†РµР»РѕРµ С‡РёСЃР»Рѕ.
        size = int(size)

        # Р•СЃР»Рё size СЏРІР»СЏРµС‚СЃСЏ С‡С‘С‚РЅС‹Рј С‡РёСЃР»РѕРј РёР»Рё РІС‹С…РѕРґРёС‚ Р·Р° РґРѕРїСѓСЃС‚РёРјС‹Р№ РґРёР°РїР°Р·РѕРЅ (3вЂ“15) - size = 9.
        if size % 2 == 0 or size < 3 or size > 15:
            size = 9

    # РћР±СЂР°Р±РѕС‚РєР° РёСЃРєР»СЋС‡РµРЅРёСЏ ValueError, РІРѕР·РЅРёРєР°СЋС‰РµРµ РїСЂРё РЅРµРєРѕСЂСЂРµРєС‚РЅРѕРј С„РѕСЂРјР°С‚Рµ size.
    except ValueError:
        size = 9

    # РћР±СЂР°Р±РѕС‚РєР° Р·Р°РїСЂРѕСЃР° РЅР° СЃРѕС…СЂР°РЅРµРЅРёРµ
    if save:
        try:
            grid = json.loads(continue_from)
            success, message = save_to_json(grid, size, step, step)
            return json.dumps({'success': success, 'message': message})
        except Exception as e:
            return json.dumps({'success': False, 'message': str(e)})

    # Р—Р°РіСЂСѓР¶Р°РµС‚СЃСЏ СЃРµС‚РєР° РґР»СЏ СЃРёРјСѓР»СЏС†РёРё: Р»РёР±Рѕ РїСЂРѕРґРѕР»Р¶Р°РµС‚СЃСЏ РёР· РїРµСЂРµРґР°РЅРЅРѕРіРѕ СЃРѕСЃС‚РѕСЏРЅРёСЏ, Р»РёР±Рѕ СЃРѕР·РґР°С‘С‚СЃСЏ РЅРѕРІР°СЏ.
    if continue_from:
        # РџСЂРѕРІРµСЂСЏРµС‚СЃСЏ РІРѕР·РјРѕР¶РЅРѕСЃС‚СЊ РїСЂРѕРґРѕР»Р¶РµРЅРёСЏ СЃРёРјСѓР»СЏС†РёРё РёР· РїРµСЂРµРґР°РЅРЅРѕРіРѕ СЃРѕСЃС‚РѕСЏРЅРёСЏ.
        try:
            # РџР°СЂР°РјРµС‚СЂ continue_from РґРµРєРѕРґРёСЂСѓРµС‚СЃСЏ РёР· JSON РІ РґРІСѓРјРµСЂРЅС‹Р№ СЃРїРёСЃРѕРє (СЃРµС‚РєСѓ).
            continue_grid = json.loads(continue_from)

        # РћР±СЂР°Р±РѕС‚РєР° РёСЃРєР»СЋС‡РµРЅРёСЏ JSONDecodeError, РІРѕР·РЅРёРєР°СЋС‰РµРіРѕ РїСЂРё РЅРµРєРѕСЂСЂРµРєС‚РЅРѕРј С„РѕСЂРјР°С‚Рµ continue_from.
        except json.JSONDecodeError:
            # Р•СЃР»Рё РґРµРєРѕРґРёСЂРѕРІР°РЅРёРµ РЅРµ СѓРґР°Р»РѕСЃСЊ, СЃРѕР·РґР°С‘С‚СЃСЏ РЅРѕРІР°СЏ СЃРµС‚РєР° СЂР°Р·РјРµСЂРѕРј size.
            grid = initialize_grid(size)
    else:
        # Р•СЃР»Рё continue_from РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚, СЃРѕР·РґР°С‘С‚СЃСЏ РЅРѕРІР°СЏ СЃРµС‚РєР° СЂР°Р·РјРµСЂРѕРј size.
        grid = initialize_grid(size)

    # РџРѕРґРіРѕС‚РѕРІРєР° РґР°РЅРЅС‹С… РґР»СЏ РїРµСЂРµРґР°С‡Рё РІ С€Р°Р±Р»РѕРЅ module2_infection_spread.tpl.

    # Р—Р°РїСѓСЃРєР°РµС‚СЃСЏ СЃРёРјСѓР»СЏС†РёСЏ СЂР°СЃРїСЂРѕСЃС‚СЂР°РЅРµРЅРёСЏ РёРЅС„РµРєС†РёРё.
    simulation_steps, final_grid, all_healthy = simulate_all_steps(grid, size)

    # РџСЂРµРѕР±СЂР°Р·СѓРµС‚СЃСЏ РєР°Р¶РґС‹Р№ С€Р°Рі СЃРёРјСѓР»СЏС†РёРё РІ JSON-СЃРѕРІРјРµСЃС‚РёРјС‹Р№ С„РѕСЂРјР°С‚.
    simulation_steps_json = [grid_to_json(step) for step in simulation_steps]

    # РџСЂРµРѕР±СЂР°Р·СѓРµС‚СЃСЏ РєРѕРЅРµС‡РЅР°СЏ СЃРµС‚РєР° РІ JSON-СЃРѕРІРјРµСЃС‚РёРјС‹Р№ С„РѕСЂРјР°С‚.
    final_grid_json = grid_to_json(final_grid)

    # РЎР»РѕРІР°СЂСЊ РґР»СЏ РїРµСЂРµРґР°С‡Рё.
    return dict(
        title='The model of ringworm infection spread',
        message='A simulation model exploring the spread of ringworm infection.',
        year=datetime.now().year,
        # РџРµСЂРµРґР°С‘С‚СЃСЏ РЅР°С‡Р°Р»СЊРЅС‹Р№ СЂР°Р·РјРµСЂ СЃРµС‚РєРё.
        initial_size=size,

        # РџРµСЂРµРґР°С‘С‚СЃСЏ СЃРїРёСЃРѕРє С€Р°РіРѕРІ СЃРёРјСѓР»СЏС†РёРё РІ JSON-С„РѕСЂРјР°С‚Рµ РґР»СЏ РѕС‚РѕР±СЂР°Р¶РµРЅРёСЏ РІ JavaScript.
        simulation_steps_json=simulation_steps_json,

        # РџРµСЂРµРґР°С‘С‚СЃСЏ РєРѕРЅРµС‡РЅР°СЏ СЃРµС‚РєР° РІ JSON-С„РѕСЂРјР°С‚Рµ РґР»СЏ РїСЂРѕРґРѕР»Р¶РµРЅРёСЏ РёР»Рё РѕС‚РѕР±СЂР°Р¶РµРЅРёСЏ.
        final_grid_json=final_grid_json,

        # РџРµСЂРµРґР°С‘С‚СЃСЏ С„Р»Р°Рі, СѓРєР°Р·С‹РІР°СЋС‰РёР№, СЏРІР»СЏСЋС‚СЃСЏ Р»Рё РІСЃРµ СЏС‡РµР№РєРё Р·РґРѕСЂРѕРІС‹РјРё.
        all_healthy=all_healthy
    )



@route('/cells_colonies')
@view('module3_cells_colonies')
def module3_cells_colonies():
    """Render the 'cells_colonies' page."""
    global game
    game = GameOfLife(3, 3)
    return dict(
        title='Colonies of living cells',
        message='A simulation of growth and interaction in colonies of living cells.',
        year=datetime.now().year
    )