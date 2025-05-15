"""
Routes and views for the bottle application.
"""

from bottle import route, view, static_file
from datetime import datetime

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
        title='About',
        message='Your application description page.',
        year=datetime.now().year
    )

@route('/wolf_island')
@view('module1_wolf_island')
def module1_wolf_island():
    """Renders the module1_wolf_island page."""
    return dict(
        title='The model of death and reproduction',
        message='A simulation model exploring death and reproduction dynamics on Wolf Island.',
        year=datetime.now().year
    )

@route('/infection_spread')
@view('module2_infection_spread')
def module2_infection_spread():
    """Renders the module2_infection_spread page."""
    from controllers.module2_infection_spread import get_initial_data
    initial_data = get_initial_data()
    return dict(
        title='The model of ringworm infection spread',
        message='A simulation model exploring the spread of ringworm infection.',
        year=datetime.now().year,
        initial_size=initial_data.get('size', 9),
        grid=initial_data.get('grid', [[0]])
    )

@route('/cells_colonies')
@view('module3_cells_colonies')
def module3_cells_colonies():
    """Renders the module3_cells_colonies page."""
    return dict(
        title='Colonies of living cells',
        message='A simulation of growth and interaction in colonies of living cells.',
        year=datetime.now().year
    )

# Статическая обработка для JavaScript и CSS
@route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='D:/SOF/UP2/BottleWebProject_C224_1_SCH/BottleWebProject_C224_1_SCH/static')