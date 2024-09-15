from flask import Blueprint, request, jsonify, session, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User
from dataclasses import asdict
from utils.db_intializer import make_connection
import random
import string
import smtplib

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
    return render_template('login/index.html')

# 비밀번호 찾기 페이지 렌더링
@auth_route.route('/find-pw', methods=['GET'])
def find_pw_page():
    return render_template('login/pw.html')

# ID 찾기 페이지 렌더링
@auth_route.route('/find-id', methods=['GET'])
def find_id_page():
    return render_template('login/id.html')



# 임시 비밀번호 생성 함수
def generate_temporary_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 이메일 전송 함수 (간단한 예시, 실제로는 이메일 전송 설정 필요)
def send_email(to_address, subject, message):
    try:
        smtp_server = 'smtp.example.com'  # SMTP 서버 주소
        smtp_port = 587
        smtp_user = 'your-email@example.com'
        smtp_password = 'your-email-password'

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            email_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(smtp_user, to_address, email_message)

        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# 아이디 찾기 (이메일로 아이디 전송)
@auth_route.route('/find-id', methods=['POST'])
def find_id():
    email = request.json.get('email')
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()

            if user:
                # 이메일로 아이디 전송
                send_email(email, "---ID---", f"{user['id']}")
                return jsonify(200)
    finally:
        connection.close()

# 비밀번호 찾기 (이메일로 임시 비밀번호 전송)
@auth_route.route('/find-pw', methods=['POST'])
def find_password():
    id = request.json.get('id')
    email = request.json.get('email')
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT email FROM users WHERE id = %s and email = %s"
            cursor.execute(sql, (id, email,))
            user = cursor.fetchone()

            if user:
                # 임시 비밀번호 생성 및 저장
                temporary_password = generate_temporary_password()
                hashed_password = generate_password_hash(temporary_password)
                sql = "UPDATE users SET password = %s WHERE id = %s"
                cursor.execute(sql, (hashed_password, email))
                connection.commit()

                # 임시 비밀번호를 이메일로 전송
                send_email(email, "---Email---", f"{temporary_password}")
                return jsonify(200)
    finally:
        connection.close()