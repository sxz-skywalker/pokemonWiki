from models.pokemon_type import PokemonType
from typing import Optional
from dataclasses import dataclass
from utils.db_intializer import make_connection


@dataclass
class Pokemon:
    id: int
    name: str
    type1: PokemonType
    total: int
    hp: int
    attack: int
    defense: int
    speed: int
    sp_atk: int
    sp_def: int
    generation: int
    type2: Optional[PokemonType] = None
    description: Optional[str] = None


# list_pokemon 함수
def get_pokemons():
    connection = make_connection()
    pokemons = []
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM pokemon"
            cursor.execute(sql)
            result = cursor.fetchall()

            # pokemon 객체로 변환
            pokemons = [
                Pokemon(**{
                    **row,
                    "type1": PokemonType(row["type1"]),
                    "type2": PokemonType(row["type2"]) if row["type2"] else None
                })
                for row in result
            ]
    finally:
        connection.close()
    return pokemons
