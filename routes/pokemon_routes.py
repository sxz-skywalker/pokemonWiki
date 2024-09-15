from flask import Blueprint, render_template
from models.pokemon import get_pokemons

pokemon_route = Blueprint('pokemon', __name__)


@pokemon_route.route('/')
def list_pokemon():
    pokemons = get_pokemons()
    return render_template('pokemon/index.html', pokemons=pokemons)
