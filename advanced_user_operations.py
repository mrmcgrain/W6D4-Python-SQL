import sqlite3
 
class AdvancedUserOperations:
    def __init__(self):
        self.conn = sqlite3.connect('user_database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                                user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                name TEXT NOT NULL UNIQUE,
                                email TEXT NOT NULL UNIQUE,
                                password TEXT,
                                age INTEGER,
                                gender TEXT, 
                                address TEXT
                            );''')
        
        self.conn.commit()
 
    def create_user_with_profile(self, name, email, password, age=None, gender=None, address=None):
        insert_sql = '''INSERT INTO user (name, email, password, age, gender, address) VALUES (?, ?, ?, ?, ?, ?);'''
        self.cursor.execute(insert_sql, (name, email, password, age, gender, address))
        self.conn.commit()
        return f'User {name} created successfully.'
        
    def retrieve_users_by_criteria(self, min_age=None, max_age=None, gender=None):
        sql_query = "SELECT * FROM user WHERE 1=1"
        parameters = []
        if min_age is not None:
            sql_query += " AND age >= ?"
            parameters.append(min_age)
        if max_age is not None:
            sql_query += " AND age <= ?"
            parameters.append(max_age)
        if gender is not None:
            sql_query += " AND gender = ?"
            parameters.append(gender)
        self.cursor.execute(sql_query, parameters)
        
        users = self.cursor.fetchall()
        return users
    
    def update_user_profile(self, email, age=None, gender=None, address=None):
        update_sql = "UPDATE user SET "
        parameters = []
        if age is not None:
            update_sql += "age = ?, "
            parameters.append(age)
        if gender is not None:
            update_sql += "gender = ?, "
            parameters.append(gender)
        if address is not None:
            update_sql += "address = ?, "
            parameters.append(address)
        if not parameters:
            print("No update available--No profile data provided.")
        update_sql = update_sql.rstrip(', ')
        update_sql += " WHERE email = ?;"
        parameters.append(email)
        try:
            self.cursor.execute(update_sql, parameters)
            self.conn.commit()
            return f'User profile {email} updated successfully.'
            
        except sqlite3.Error as e:
            return f'An error occurred: {e}'
 
    def delete_users_by_criteria(self, gender=None):
        delete_sql = "DELETE FROM user WHERE 1=1"
        parameters = []
        if gender is not None:
            delete_sql += " AND gender = ?"
            parameters.append(gender)
        try:
            self.cursor.execute(delete_sql, parameters)
            self.conn.commit()
            rows_removed = self.cursor.rowcount
            return f'{rows_removed} user(s) deleted successfully.'
        except sqlite3.Error as e:
            return f'An error occurred while deleting users: {e}'
 
    def __del__(self):
        self.conn.close()