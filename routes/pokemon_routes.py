from flask import Blueprint, render_template
from models.pokemon import Pokemon

pokemon_route = Blueprint('pokemon', __name__)


@pokemon_route.route('/')
def list_pokemon():
    pokemons = Pokemon.query.all()
    return render_template('pokemon.html', pokemons=pokemons)
