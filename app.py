from flask import Flask
from routes.pokemon_routes import pokemon_route
from routes.forum_routes import forum_route
from routes.main_routes import main_route
from config import config
from utils import db_intializer

app = Flask(__name__)

# 환경설정 적용
app.config.from_object(config)


with app.app_context():
    # DB 초기화
    db_intializer.run(app)


# 개별 선언한 route들을 BluePrint 등록
app.register_blueprint(main_route)
app.register_blueprint(pokemon_route, url_prefix='/pokemons')
app.register_blueprint(forum_route, url_prefix='/forums')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
