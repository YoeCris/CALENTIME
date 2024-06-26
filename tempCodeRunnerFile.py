import mysql.connector
from config import Config

class UserManagement:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.db = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB
            )
            self.cursor = self.db.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Error al conectar con la base de datos: {err}")

    def create_user(self, username, password, role):
        try:
            sql = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (username, password, role))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error al crear usuario: {err}")

    def create_default_superusers(self):
        superusers = [
            ('sadmin1', 'sadmin1pas', 'superuser'),
            ('sadmin2', 'sadmin2pas', 'superuser')
        ]

        for user in superusers:
            username, password, role = user
            existing_user = self.get_user_by_username(username)
            if existing_user:
                continue
        
            try:
                self.create_user(username, password, role)
            except mysql.connector.IntegrityError as e:
                print(f"Error al insertar superusuario {username}: {str(e)}")

    def get_users(self):
        try:
            self.cursor.execute("SELECT * FROM users")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener usuarios: {err}")
            return []

    def get_user_by_username(self, username):
        try:
            self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener usuario por nombre de usuario: {err}")
            return None

    def delete_user(self, user_id):
        try:
            self.cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error al eliminar usuario: {err}")

    def is_superuser(self, username):
        user = self.get_user_by_username(username)
        return user and user['role'] == 'superuser'

    def close_connection(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")

    def __del__(self):
        self.close_connection()
