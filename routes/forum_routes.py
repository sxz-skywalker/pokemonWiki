from flask import Blueprint, render_template, request, jsonify
from utils.db_intializer import make_connection
from models.document_type import DocumentType, convert

forum_route = Blueprint('forum', __name__)


@forum_route.route('/')
def main_forum():
    return render_template('forum.html')


@forum_route.route('/<int:id>', defaults={'type': None})
@forum_route.route('/create', defaults={'type': 'create', 'id': None})
@forum_route.route('/<string:type>/<int:id>')
def detail_forum(type, id):
    connection = make_connection()
    print('type!!', type)
    doc_type = convert(DocumentType, type)
    item = {}
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM forum WHERE id = %s"
            cursor.execute(sql, (id,))
            item = cursor.fetchone()
    finally:
        connection.close()
        return render_template('forum_detail.html',
                               item=item,
                               doc_type=doc_type if doc_type is not None else DocumentType.READ,
                               show_back_btn=True)


# 게시글 목록 조회
@forum_route.route('/list', methods=['GET'])
def get_forum_list():

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
            # 리스트 조회
            base_sql = "SELECT * FROM forum"
            count_sql = "SELECT COUNT(*) FROM forum"

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
    data = request.json
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            # id가 있으면 update
            if 'id' in data:
                sql = """
                UPDATE forum SET name=%s, category=%s, title=%s, content=%s, update_date=CURRENT_TIMESTAMP WHERE id=%s
                """
                cursor.execute(sql, (data['name'], data['category'], data['title'], data['content'], data['id']))
            else:
                sql = """
                INSERT INTO forum (name, category, title, content) VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (data['name'], data['category'], data['title'], data['content']))
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