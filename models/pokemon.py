from models.pokemon_type import PokemonType
from . import db


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type1 = db.Column(db.Enum(PokemonType), nullable=False)
    type2 = db.Column(db.Enum(PokemonType), nullable=True)
    total = db.Column(db.Integer, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    sp_atk = db.Column(db.Integer, nullable=False)
    sp_def = db.Column(db.Integer, nullable=False)
    generation = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)