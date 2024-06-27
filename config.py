class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'user_management_system'


    '''def get_user_by_last_name(self, last_name):
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
            return None'''