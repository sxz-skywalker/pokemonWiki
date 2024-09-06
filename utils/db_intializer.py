import os
import json
import time
import pymysql
from config import config

def make_connection():
    return pymysql.connect(
        host = config.DATABASE_HOST,
        user = config.DATABASE_USER,
        password = config.DATABASE_PASSWORD,
        database = config.DATABASE_SCHEMA,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
)
# MySQL 서버가 준비될 때까지 재시도
def wait_for_db():
    while True:
        try:
            connection = make_connection()
            connection.close()
            break
        except pymysql.err.OperationalError:
            print("Waiting for MySQL server to start...")
            time.sleep(2)


def initialize_db():
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            # 테이블 생성 쿼리 실행
            schema_file = os.path.join(os.path.dirname(__file__), '../sql', 'schema.sql')
            with open(schema_file, 'r') as file:
                schema_sql = file.read()
                cursor.execute(schema_sql)
            connection.commit()
            print("The tables were created successfully")
    finally:
        connection.close()


# 도커 컨테이너 실행 시 JSON 데이터를 데이터베이스에 삽입
def load_data():
    data_file = os.path.join(os.path.dirname(__file__), '../data', 'poke.json')
    if os.path.exists(data_file):
        with open(data_file) as f:
            pokemons = json.load(f)
            merge_data(pokemons)


def merge_data(pokemons):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            for pokemon_data in pokemons:
                # type2가 빈 문자열일 경우 None으로 변경
                if pokemon_data['type2'] == '':
                    pokemon_data['type2'] = None

                # sql 생성을 위한 string 값 생성
                columns = ', '.join(pokemon_data.keys())
                placeholders = ', '.join(['%s'] * len(pokemon_data))
                updates = ', '.join([f"{key}=VALUES({key})" for key in pokemon_data])

                # INSERT 또는 UPDATE 쿼리 작성 (MERGE와 유사한 동작)
                sql = f"""
                    INSERT INTO pokemon ({columns})
                    VALUES ({placeholders})
                    ON DUPLICATE KEY UPDATE {updates}
                """

                # 쿼리 실행
                cursor.execute(sql, tuple(pokemon_data.values()))

        # 변경 사항 커밋
        connection.commit()
    finally:
        connection.close()


# DB 초기화
def run(app):
    wait_for_db()   # DB 커넥션 기다리기
    initialize_db()     # 테이블 생성
    load_data()     # 데이터 로드
