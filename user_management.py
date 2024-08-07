# user_management.py

import mysql.connector

# class UserManagement:
#     def __init__(self):
#         self.db = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="",  
#             database="gestion_casos"  
#         )
#         self.cursor = self.db.cursor(dictionary=True)
#         self.users = self.get_users()
#SERVER 
class UserManagement:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="62.72.8.253",
            user="odin",
            password="labodin123",  
            database="gestion_casos"
        )
        self.cursor = self.db.cursor(dictionary=True)
        self.users = self.get_users()  

    # Consultas para la tabla users
    def create_default_superusers(self):
        try:
            self.cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            result = self.cursor.fetchone()
            if not result:
                self.create_user('admin', 'admin', 'administrador', 'Admin', 'User', '946641546', '73744399')
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def create_user(self, username, password, role, first_name, last_name, number_phone, dni):
        try:
            sql = "INSERT INTO users (username, password, role, first_name, last_name, number_phone, dni) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (username, password, role, first_name, last_name, number_phone, dni)
            self.cursor.execute(sql, values)
            self.db.commit()
            self.users = self.get_users()  # Update the local cache of users
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

    def get_users(self):
        try:
            self.cursor.execute("SELECT * FROM users")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
    
    def get_user_by_id(self, user_id):
        try:
            sql = "SELECT * FROM users WHERE user_id = %s"
            self.cursor.execute(sql, (user_id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def get_user_by_username(self, username):
        try:
            sql = "SELECT * FROM users WHERE username = %s"
            self.cursor.execute(sql, (username,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def update_case_stage(self, case_id, new_stage):
        try:
            sql = "UPDATE cases SET stage = %s WHERE case_id = %s"
            self.cursor.execute(sql, (new_stage, case_id))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def finalize_case(self, case_id):
        self.update_case_stage(case_id, 'finalizado')

    def update_user(self, user_id, username, password, role, first_name, last_name, number_phone, dni):
        try:
            sql = "UPDATE users SET username = %s, password = %s, role = %s, first_name = %s, last_name = %s, number_phone = %s, dni = %s WHERE user_id = %s"
            self.cursor.execute(sql, (username, password, role, first_name, last_name, number_phone, dni, user_id))
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
        
    def delete_user_and_cases(self, user_id):
        # Obtén los casos asociados al usuario
        affected_cases = self.get_cases_by_reviewer(user_id)
        # Elimina los casos asociados
        for case in affected_cases:
            self.delete_case(case['case_id'])
        # Elimina al usuario
        self.delete_user(user_id)

    # Consultas para la tabla cases
    def create_case(self, code, investigated_last_name, investigated_first_name, dni, reviewer, created_date, deadline, stage):
        try:
            sql = "INSERT INTO cases (code, investigated_last_name, investigated_first_name, dni, reviewer, created_date, deadline, stage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (code, investigated_last_name, investigated_first_name, dni, reviewer, created_date, deadline, stage))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def get_all_cases(self):
        try:
            self.cursor.execute("SELECT * FROM cases")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def get_case(self, case_id):
        try:
            sql = "SELECT * FROM cases WHERE case_id = %s"
            self.cursor.execute(sql, (case_id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def get_case_by_code(self, code):
        try:
            sql = "SELECT * FROM cases WHERE code = %s"
            self.cursor.execute(sql, (code,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None    

    def get_cases_by_reviewer(self, reviewer):
        query = "SELECT * FROM cases WHERE reviewer = %s"
        self.cursor.execute(query, (reviewer,))
        return self.cursor.fetchall()

    def update_case(self, case_id, code, investigated_last_name, investigated_first_name, dni, reviewer, created_date, deadline, stage):
        try:
            sql = "UPDATE cases SET code = %s, investigated_last_name = %s, investigated_first_name = %s, dni = %s, reviewer = %s, created_date = %s, deadline = %s, stage = %s WHERE case_id = %s"
            values = (code, investigated_last_name, investigated_first_name, dni, reviewer, created_date, deadline, stage, case_id)
            self.cursor.execute(sql, values)
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()
    
    def update_case_status(self, case_id, new_status):
        try:
            sql = "UPDATE cases SET status = %s WHERE case_id = %s"
            self.cursor.execute(sql, (new_status, case_id))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def delete_case(self, case_id):
        try:
            sql = "DELETE FROM cases WHERE case_id = %s"
            self.cursor.execute(sql, (case_id,))
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def close_connection(self):
        if self.db:
            self.db.close()
