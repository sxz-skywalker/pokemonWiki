from dataclasses import dataclass
from utils.db_intializer import make_connection
from datetime import datetime

@dataclass
class User:
    id: str
    name: str
    email: str
    school: str
    password: str
    file_name: str
    file_path: str
    file_id: int
    create_date: datetime


    # 유저 정보 조회
    @staticmethod
    def get_by_id(id):
        connection = make_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT u.*, f.name AS file_name, f.path AS file_path
                    FROM users u
                    LEFT JOIN files f ON u.file_id = f.id
                    WHERE u.id = %s
                """
                cursor.execute(sql, (id,))
                data = cursor.fetchone()

                if data:
                    return User(**data)  # dataclass로 변환하여 return
                return None
        finally:
            connection.close()