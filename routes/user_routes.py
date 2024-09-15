from flask import Blueprint, request, jsonify, session, render_template
from utils.db_intializer import make_connection
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from dataclasses import asdict

user_route = Blueprint('user', __name__)


# ID 중복 체크
@user_route.route('/check-id', methods=['GET'])
def check_id():
    username = request.args.get('id')
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id FROM users WHERE id = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()

            # 세션에 결과 저장
            isValid = user is None
            session['id_check'] = True if isValid else False
            return jsonify(200 if isValid else 409)
    finally:
        connection.close()


# 회원 가입 페이지 접근
@user_route.route('/signup', methods=['GET'])
def signup_page():
    # 세션 초기화
    session.pop('id_check', None)
    return render_template('user/signup.html')

# 나의 정보 페이지 접근
@user_route.route('/my-info', methods=['GET'])
def myinfo_page():
    return render_template('user/my-info.html')


# 회원 가입 API
@user_route.route('/signup', methods=['POST'])
def signup():
    d = request.json
    password = d.get('password')
    # 세션에서 ID 중복 체크 여부 확인
    if 'id_check' not in session or not session['id_check']:
        return jsonify({'error': 'ID check not passed'}), 403

    hashed_password = generate_password_hash(password)
    print('hashed_password', hashed_password)

    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (id, name, password, email, file_id, school) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (d.get('id'), d.get('name'), hashed_password,
                 d.get('email'), d.get('file_id'), d.get('school')))
            connection.commit()

            # 회원가입 성공 시 세션 초기화
            session.pop('id_check', None)
            return jsonify(200)
    finally:
        connection.close()


# 유저 프로필 조회
@user_route.route('/profile/<string:id>', methods=['GET'])
def get_profile(id):
    # 사용자 정보를 다시 조회하여 세션에 저장
    pers = User.get_by_id(id)
    dict = asdict(pers)
    dict.pop('password', None)
    return render_template('user/detail.html', pers=dict, show_back_btn=True)


# 내 정보 수정
@user_route.route('/profile', methods=['POST'])
def update_profile():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    d = request.json
    id = session['user']['id']

    fields = []
    values = []

    if 'name' in d and d['name']:
        fields.append("name = %s")
        values.append(d['name'])

    if 'email' in d and d['email']:
        fields.append("email = %s")
        values.append(d['email'])

    if 'school' in d and d['school']:
        fields.append("school = %s")
        values.append(d['school'])

    if 'file_id' in d and d['file_id']:
        fields.append("file_id = %s")
        values.append(d['file_id'])

    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            # 비밀번호를 제외한 정보 업데이트
            sql = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
            values.append(id)
            cursor.execute(sql, values)
            connection.commit()

            # 사용자 정보를 다시 조회하여 세션에 저장
            updated_user = User.get_by_id(id)
            dict = asdict(updated_user)
            dict.pop('password', None)
            session['user'] = dict

        return jsonify(200)
    finally:
        connection.close()