import os
from flask import Blueprint, request, jsonify, send_from_directory
from config import config
from utils.db_intializer import make_connection

file_route = Blueprint('file', __name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', config.UPLOAD_FOLDER)
UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'static', config.UPLOAD_FOLDER)

# 파일 업로드
@file_route.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    name = file.filename
    path = os.path.join(config.UPLOAD_FOLDER, name)

    # 업로드 폴더 생성
    if not os.path.exists(config.UPLOAD_FOLDER):
        os.makedirs(config.UPLOAD_FOLDER)

    # 파일 추가 후 DB에 저장
    file.save(path)
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO files (name, path) VALUES (%s, %s)"
            cursor.execute(sql, (name, path))
            connection.commit()
            file_id = cursor.lastrowid  # 파일 ID 조회
    finally:
        connection.close()

    return jsonify({'file_id': file_id}), 200   # 파일 ID 리턴



# 파일 다운로드
@file_route.route('/download/<int:id>', methods=['GET'])
def download_file(id):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            # 파일 경로를 DB에서 조회
            sql = "SELECT name, path FROM files WHERE id = %s"
            cursor.execute(sql, (id,))
            file_data = cursor.fetchone()

            if not file_data:
                return jsonify({'error': 'File not found'}), 404

            name = file_data['name']
            file_path = file_data['path']  # 파일 경로

            # 파일 존재 여부 확인
            if not os.path.exists(file_path):
                return jsonify({'error': 'File not found on server'}), 404

            # 파일이 있는 디렉토리에서 파일을 다운로드로 보냄
            return send_from_directory(directory=os.path.dirname(file_path), path=name, as_attachment=True)

    finally:
        connection.close()



# 파일 다운로드 및 브라우저에 이미지로 표시
@file_route.route('/image/<int:id>', methods=['GET'])
def get_image(id):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            # 파일 경로를 DB에서 조회
            sql = "SELECT name, path FROM files WHERE id = %s"
            cursor.execute(sql, (id,))
            file_data = cursor.fetchone()

            if not file_data:
                return jsonify({'error': 'File not found'}), 404

            name = file_data['name']
            file_path = file_data['path']  # 파일 경로

            # 파일 존재 여부 확인
            if not os.path.exists(file_path):
                return jsonify({'error': 'File not found on server'}), 404

            # 이미지를 inline으로 브라우저에 표시
            return send_from_directory(directory=os.path.dirname(file_path), filename=name, as_attachment=False)

    finally:
        connection.close()