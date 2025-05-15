"""
Routes and views for the bottle application.
"""

from bottle import route, view
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
@view('module1WolfIsland')
def module1WolfIsland():
    """Renders the module1WolfIsland page."""
    return dict(
        title='The model of death and reproduction',
        message='A simulation model exploring death and reproduction dynamics on Wolf Island.',
        year=datetime.now().year
    )

@route('/infection_spread')
@view('module2InfectionSpread')
def module2InfectionSpread():
    """Renders the module2InfectionSpread page."""
    return dict(
        title='The spread of infection',
        message='A model simulating the dynamics of infection spread in a population.',
        year=datetime.now().year
    )

@route('/cells_colonies')
@view('module3_cells_colonies')
def module3_cells_coloniesÿ():
    """Renders the module3_cells_colonies page."""
    return dict(
        title='Colonies of living cells',
        message='A simulation of growth and interaction in colonies of living cells.',
        year=datetime.now().year,
        current_page='cells_colonies',
        width=3,  
        height=3,  
        initial_cells=[(0,0), (0,1), (1,1), (2,0)] 
    )