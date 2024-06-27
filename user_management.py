import mysql.connector

class UserManagement:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="gestion_casos"  
        )
        self.cursor = self.db.cursor(dictionary=True)
        self.users = self.get_users()


#consultas para la tabla users

    def create_default_superusers(self):
        try:
            self.cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            result = self.cursor.fetchone()
            if not result:
                self.create_user('admin', 'admin', 'administrador', 'Admin', 'User', '12345678')
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def create_user(self, username, password, role, first_name, last_name, dni):
        try:
            sql = "INSERT INTO users (username, password, role, first_name, last_name, dni) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (username, password, role, first_name, last_name, dni))
            self.db.commit()
            self.users = self.get_users()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def update_user_password(self, username, new_password):
        try:
            sql = "UPDATE users SET password = %s WHERE username = %s"
            self.cursor.execute(sql, (new_password, username))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def get_user_by_username(self, username):
        try:
            sql = "SELECT * FROM users WHERE username = %s"
            self.cursor.execute(sql, (username,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def get_user_by_last_name(self, last_name):
        try:
            sql = "SELECT * FROM users WHERE last_name = %s"
            self.cursor.execute(sql, (last_name,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        
    def get_user_by_first_name(self, first_name):
        try:
            sql = "SELECT * FROM users WHERE first_name = %s"
            self.cursor.execute(sql, (first_name,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        
    def get_users(self):
        try:
            self.cursor.execute("SELECT * FROM users")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def update_user_role(self, username, role):
        try:
            sql = "UPDATE users SET role = %s WHERE username = %s"
            self.cursor.execute(sql, (role, username))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def update_user(self, username, password, role, first_name, last_name, dni):
        # Actualiza un usuario existente
        for user in self.users:
            if user['username'] == username:
                user['password'] = password
                user['role'] = role
                user['first_name'] = first_name
                user['last_name'] = last_name
                user['dni'] = dni
                break
        try:
            sql = "UPDATE users SET password = %s, role = %s, first_name = %s, last_name = %s, dni = %s WHERE username = %s"
            self.cursor.execute(sql, (password, role, first_name, last_name, dni, username))
            self.db.commit()
            self.users = self.get_users()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

            
    def delete_user(self, username):
        try:
            sql = "DELETE FROM users WHERE username = %s"
            self.cursor.execute(sql, (username,))
            self.db.commit()
            self.users = self.get_users()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

#consultas para la tabla cases:

    def create_case(self, code, investigated_last_name, investigated_first_name, dni, reviewer, stage):
        try:
            sql = "INSERT INTO cases (code, investigated_last_name, investigated_first_name, dni, reviewer, stage) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (code, investigated_last_name, investigated_first_name, dni, reviewer, stage))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def get_case(self, search_value, criterion='id'):
        try:
            sql = f"SELECT * FROM cases WHERE {criterion} = %s"
        
            self.cursor.execute(sql, (search_value,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def get_cases_by_reviewer(self, reviewer):
        try:
            sql = "SELECT * FROM cases WHERE reviewer = %s"
            self.cursor.execute(sql, (reviewer,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def get_cases_by_dni(self, dni):
        try:
            sql = "SELECT * FROM cases WHERE dni = %s"
            self.cursor.execute(sql, (dni,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def update_case(self, case_id, code, investigator_last_name, investigator_first_name, dni, reviewer, stage):
        try:
            sql = "UPDATE cases SET code = %s, investigator_last_name = %s, investigator_first_name = %s, dni = %s, reviewer = %s, stage = %s WHERE id = %s"
            self.cursor.execute(sql, (code, investigator_last_name, investigator_first_name, dni, reviewer, stage, case_id))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def delete_case(self, case_id):
        try:
            sql = "DELETE FROM cases WHERE id = %s"
            self.cursor.execute(sql, (case_id,))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def close_connection(self):
        if self.db:
            self.db.close()
