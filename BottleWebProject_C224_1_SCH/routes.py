"""
Routes and views for the bottle application.
"""

from bottle import request, route, view, static_file
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
        title='About authors',
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
    # Get 'size' from GET request, default to '9'
    size = request.GET.get('size', '9')
    try:
        # Convert size to integer and validate: must be odd, between 3 and 15
        size = int(size)
        if size % 2 == 0 or size < 3 or size > 15:
            size = 3
    except ValueError:
        size = 3

    # Create a grid of size x size filled with 0 (healthy cells)
    grid = [[0 for _ in range(size)] for _ in range(size)]

    # Return data for the template
    return dict(
        title='The model of ringworm infection spread',
        message='A simulation model exploring the spread of ringworm infection.',
        year=datetime.now().year,
        initial_size=size,
        grid=grid
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
