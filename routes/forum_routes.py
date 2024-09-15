from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from utils.db_intializer import make_connection
from models.document_type import DocumentType, convert

forum_route = Blueprint('forum', __name__)
forum_private_id = 'forum_private_id'

# 포럼 메인 페이지
@forum_route.route('/')
def main_forum():
    return render_template('forum/index.html')


# 포럼 상세 조회 페이지
@forum_route.route('/<int:id>', defaults={'type': None})
@forum_route.route('/create', defaults={'type': 'create', 'id': None})
@forum_route.route('/<string:type>/<int:id>')
def detail_forum(type, id):
    connection = make_connection()
    doc_type = convert(DocumentType, type)
    item = {}
    try:
        with connection.cursor() as cursor:
            # 파일 테이블과 조인
            sql = """
                SELECT f.id, f.name, f.user_id, f.title, f.category, f.content,
                    CASE WHEN f.password IS NOT NULL AND f.password != '' THEN 1 ELSE 0 END AS has_password, 
                    f.file_id, f.create_date, f.update_date, ff.name as file_name, ff.path 
                FROM forum f 
                LEFT JOIN files ff ON f.file_id = ff.id
                WHERE f.id = %s
            """
            cursor.execute(sql, (id,))
            item = cursor.fetchone()
            # 비밀글 접근 권한 체크
            if item is not None and item.get('has_password') == 1:
                if session.get(forum_private_id) is None or session.get(forum_private_id) != id:
                    return redirect(url_for('forum.main_forum'))
            return render_template('forum/detail.html',
               item=item,
               doc_type=doc_type if doc_type is not None else DocumentType.READ,
               show_back_btn=True)
    finally:
        connection.close()


# 비밀글 접근 권한 체크 페이지
@forum_route.route('/password/<int:id>')
def password_page(id):
    # 세션에 있는 비밀글 접근 권한 정보 만료
    session.pop(forum_private_id, None)
    return render_template('forum/password.html', id=id)


# 포럼 목록 조회 API
@forum_route.route('/list', methods=['GET'])
def get_forum_list():
    # 세션에 있는 비밀글 접근 권한 정보 만료
    session.pop(forum_private_id, None)

    query = request.args.get('query', '')
    search_type = request.args.get('type', '')

    # 페이징
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    size = int(request.args.get('size', 5))
    offset = (page - 1) * size

    connection = make_connection()

    try:
        with connection.cursor() as cursor:
            # 파일 테이블과 조인
            base_sql = """
                SELECT 
                    id, user_id, name, title, category, 
                    CASE WHEN password IS NOT NULL AND password != '' THEN 1 ELSE 0 END AS has_password, 
                    file_id, create_date, update_date, content 
                FROM forum
            """
            count_sql = "SELECT COUNT(*) FROM forum"

            # 검색 쿼리가 있는 경우
            if query:
                if search_type:
                    filter_sql = f" WHERE {search_type} LIKE %s"
                    filter_params = ('%' + query + '%',)
                else:
                    filter_sql = f" WHERE title LIKE %s OR content LIKE %s"
                    filter_params = ('%' + query + '%', '%' + query + '%')
                base_sql += filter_sql
                count_sql += filter_sql
            else:
                filter_params = ()

            # 페이징을 위한 LIMIT와 OFFSET 추가
            list_sql = f"{base_sql} ORDER BY create_date DESC LIMIT %s OFFSET %s"
            cursor.execute(list_sql, filter_params + (size, offset))
            list = cursor.fetchall()

            # 카운트 조회
            cursor.execute(count_sql, filter_params)
            cnt = cursor.fetchone()['COUNT(*)']  # 전체 게시글 수

        return jsonify({
                'list': list,
                'cnt': cnt,
                'page': page,
                'size': size,
                'total_pages': (cnt + size - 1) // size # 전체 페이지 수
            })
    finally:
        connection.close()


# 게시글 생성/수정
@forum_route.route('/', methods=['POST'])
def update_forum():
    d = request.json
    user_id = session['user']['id']
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            # id가 있으면 update
            if 'id' in d:
                sql = """
                UPDATE forum SET name=%s, user_id=%s, category=%s, title=%s, file_id=%s, password=%s, content=%s, update_date=CURRENT_TIMESTAMP WHERE id=%s
                """
                cursor.execute(sql, (d.get('name'), user_id, d.get('category'), d.get('title'), d.get('file_id'), d.get('password'), d.get('content'), d.get('id')))
            else:
                sql = """
                INSERT INTO forum (name, user_id, category, title, file_id, password, content) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (d.get('name'), user_id, d.get('category'), d.get('title'), d.get('file_id'), d.get('password'), d.get('content')))
        connection.commit()
        return jsonify(200)
    finally:
        connection.close()


# 게시글 삭제
@forum_route.route('/<int:id>', methods=['DELETE'])
def delete_forum(id):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM forum WHERE id = %s"
            cursor.execute(sql, (id,))
        connection.commit()
        return jsonify(200)
    finally:
        connection.close()


# 게시글의 비밀번호 확인
@forum_route.route('/check-password/<int:id>', methods=['POST'])
def check_forum_password(id):
    data = request.json
    check_password = data.get('password')
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            # 게시글의 비밀번호 조회
            sql = "SELECT password FROM forum WHERE id = %s AND password IS NOT NULL"
            cursor.execute(sql, (id,))
            forum = cursor.fetchone()

            # 비밀번호 확인
            if forum['password'] != check_password:
                return jsonify(403)
        session[forum_private_id] = id
        return jsonify(200)
    finally:
        connection.close()