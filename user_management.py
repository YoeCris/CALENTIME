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
            
    def delete_user(self, username):
        try:
            sql = "DELETE FROM users WHERE username = %s"
            self.cursor.execute(sql, (username,))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def create_case(self, code, investigator_last_name, investigator_first_name, dni, reviewer, description, stage, deadline, status, urgency_level, review_file=None):
        try:
            sql = "INSERT INTO cases (code, investigator_last_name, investigator_first_name, dni, reviewer, description, stage, deadline, status, urgency_level, review_file) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (code, investigator_last_name, investigator_first_name, dni, reviewer, description, stage, deadline, status, urgency_level, review_file))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def get_case_by_id(self, case_id):
        try:
            sql = "SELECT * FROM cases WHERE id = %s"
            self.cursor.execute(sql, (case_id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def update_case(self, case_id, code, investigator_last_name, investigator_first_name, dni, reviewer, description, stage, deadline, status, urgency_level, review_file=None):
        try:
            sql = "UPDATE cases SET code = %s, investigator_last_name = %s, investigator_first_name = %s, dni = %s, reviewer = %s, description = %s, stage = %s, deadline = %s, status = %s, urgency_level = %s, review_file = %s WHERE id = %s"
            self.cursor.execute(sql, (code, investigator_last_name, investigator_first_name, dni, reviewer, description, stage, deadline, status, urgency_level, review_file, case_id))
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

    def create_case_stage(self, case_id, stage):
        try:
            sql = "INSERT INTO case_stages (case_id, stage) VALUES (%s, %s)"
            self.cursor.execute(sql, (case_id, stage))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def get_case_stages(self, case_id):
        try:
            sql = "SELECT * FROM case_stages WHERE case_id = %s"
            self.cursor.execute(sql, (case_id,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def close_connection(self):
        if self.db:
            self.db.close()
