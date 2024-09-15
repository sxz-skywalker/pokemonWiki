from flask import Flask, session, request, redirect, url_for
from routes.pokemon_routes import pokemon_route
from routes.forum_routes import forum_route
from routes.main_routes import main_route
from routes.user_routes import user_route
from routes.file_routes import file_route
from routes.auth_routes import auth_route
from config import config
from utils import db_intializer

app = Flask(__name__)

# 환경설정 적용
app.config.from_object(config)


with app.app_context():
    # DB 초기화
    db_intializer.run()


# 개별 선언한 route들을 BluePrint 등록
app.register_blueprint(main_route)
app.register_blueprint(pokemon_route, url_prefix='/pokemons')
app.register_blueprint(forum_route, url_prefix='/forums')
app.register_blueprint(user_route, url_prefix='/users')
app.register_blueprint(file_route, url_prefix='/files')
app.register_blueprint(auth_route, url_prefix='/auth')
@app.context_processor
def inject_user():
    return {'user': session.get('user')}
@app.before_request
def check_login():
    # 세션에 유저 정보 없을 경우 로그인 페이지로 이동
    if 'user' not in session and request.path.startswith('/forums'):
        return redirect(url_for('auth.login_page'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
