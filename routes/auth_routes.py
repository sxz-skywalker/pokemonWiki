from flask import Blueprint, request, jsonify, session, render_template
from werkzeug.security import check_password_hash
from models.user import User
from dataclasses import asdict

auth_route = Blueprint('auth', __name__)

# 로그인
@auth_route.route('/login', methods=['POST'])
def login():
    data = request.json
    id = data.get('id')
    password = data.get('password')

    print('userrr', password)
    user = User.get_by_id(id)
    print('user2', user)

    # 유저 정보 여부와 패스워드 일치 여부 체크
    if user and check_password_hash(user.password, password):
        # 비밀번호 제외 후 세션에 유저 정보 딕셔너리로 변환하여 저장
        dict = asdict(user)
        dict.pop('password', None)
        session['user'] = dict
        return jsonify(200)
    else:
        return jsonify(401)


# 로그아웃
@auth_route.route('/logout', methods=['POST'])
def logout():
    session.clear()  # 세션 초기화
    return jsonify(200)

# 로그인 페이지 렌더링
@auth_route.route('/login', methods=['GET'])
def login_page():
    return render_template('login/index.html')  # login.html 템플릿을 렌더링