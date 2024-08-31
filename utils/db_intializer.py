from flask_migrate import Migrate
from models import db, Pokemon
import os
import json
import time
import pymysql
from config import config

# MySQL 서버가 준비될 때까지 재시도
def wait_for_db():
    while True:
        try:
            connection = pymysql.connect(
                host = config.DATABASE_HOST,
                user = config.DATABASE_USER,
                password = config.DATABASE_PASSWORD,
                database = config.DATABASE_SCHEMA
            )

            connection.close()
            break
        except pymysql.err.OperationalError:
            print("Waiting for MySQL server to start...")
            time.sleep(2)


# 도커 컨테이너 실행 시 JSON 데이터를 데이터베이스에 삽입
def load_data():
    data_file = os.path.join(os.path.dirname(__file__), '../data', 'poke.json')
    if os.path.exists(data_file):
        with open(data_file) as f:
            pokemons = json.load(f)
            for pokemon_data in pokemons:
                if pokemon_data['type2'] == '':
                    pokemon_data['type2'] = None
                pokemon = Pokemon(**pokemon_data)
                db.session.merge(pokemon)
            db.session.commit()


# DB 초기화
def run(app):
    wait_for_db()
    db.init_app(app)
    Migrate(app, db)
    db.create_all()
    load_data()
