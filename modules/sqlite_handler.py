import sqlite3
from datetime import datetime
import hashlib
from .helpers import USER_INDEXES

def encrypt(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest() 

class SQLite:
    def __init__(self, file="database.db"):
        self.file = file
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn

    def __exit__(self, type, value, traceback):
        self.conn.close()

class Database:
    """Database class handler to manage all the users info, etc."""
    def __init__(self, name="database.db"):
        self.db_name = name

    #create a table if not exist
    def create_table(self, name, fields):
        """Create a table with the given name.
            [Arguments]
            name: The name for the table
            fields: an object with the field name and type ex:
                    {"id": "INT", "name": "TEXT", "phone": "TEXT"}
        """
        try:
            with SQLite(self.db_name) as cursor:
                fields_str = [] 
                for field in fields.keys():
                    fields_str.append(f"{field} {fields[field]}")
                query = f"CREATE TABLE IF NOT EXISTS {name} ({(',').join(fields_str)});"
                cursor.execute(query)
                result = cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{name}';").fetchone()
                return result
        except sqlite3.DatabaseError as e:
            er = f"ERROR: Unable to create table {e}"
            print(er)
            return er

    #Delete a table if exist
    def delete_table(self, name):
        """Delete the given table name.
            [Arguments]
            name: string with the table name.
        """
        try:
            with SQLite(self.db_name) as cursor:
                cursor.execute("DROP TABLE IF EXISTS ?;", [name])
                result = cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name = ?;", [name]).fetchone()
                return result
        except sqlite3.DatabaseError as e:
            er = f"ERROR: unable to delete table {e}"
            print(er)
            return er
    
    #Creates a new table with a Foreign key field to a different table
    def create_child_table(self, name, fields, field_id, parent_name, parent_field):
        """Create a child table with a ForeignKey relation
            [Arguments]
            name: a string with the table name.
            fields: an object with the fields and types,
            field_id: an object with the field to hold the relationship,
            parent_name: a string with the parent table name,
            parent_field: a string with the name of the parent 
                          table field for the reference
        """
        try:
            with SQLite(self.db_name) as cursor:
                fields_string = []
                for key in fields.keys():
                    fields_string.append(f"{key} {fields[key]}")

                query = f"""CREATE TABLE IF NOT EXISTS {name} (
                {','.join(fields_string)}, 
                FOREIGN KEY ({field_id}) REFERENCES {parent_name} ({parent_field})
                ON DELETE CASCADE
                );"""
                cursor.execute(query)
                result = cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?;", [name]).fetchone()
                return result

        except sqlite3.DatabaseError as e:
            er = f"ERROR: unable to create child table {e}"
            print(er)
            return er
            
    #create a new user
    def create_user(self, data):
        """Create a user on the user table.
            [Arguments]
            data: An array with the values in this order:
                    [first_name, last_name, eid, password, clock_in_time, clock_out_time, is_admin]
        """

        try:
            with SQLite(self.db_name) as cursor:
                data[3] = encrypt(data[3]) #encrypt password
                fields = ["first_name", "last_name", "eid", "password", "clock_in_time", "clock_out_time", "is_admin"]
                query = f"INSERT INTO users ({','.join(fields)}) VALUES ({str(data)[1:-1]});"
                cursor.execute(query)
                cursor.commit()
                result = cursor.execute(f"SELECT * FROM users WHERE first_name = ? AND last_name = ? AND eid = ?;",[data[0], data[1], data[2]]).fetchone()
                return result
        
        except sqlite3.DatabaseError as e:
            er =f"ERROR: Unable to create user {e}"
            print(er)
            return er

    #Update a user record
    def update_user(self, id, fields):
        """Update a given id user.
            [Arguments]
            id: an integer with the user ID to update
            fields: an object with the fields to update, Ex:
                    {"name": "francisco", "phone": "1223456"}
                    {"phone": "65431212"}
        """

        try:
            with SQLite(self.db_name) as cursor:
                column_set = []
                for column in fields.keys():
                    column_set.append(f"{column} = '{fields[column]}'")
                query = f"UPDATE users SET {','.join(column_set)} WHERE id = {id};"
                cursor.execute(query)
                cursor.commit()
                result = cursor.execute(f"SELECT * FROM users WHERE id = '{id}';").fetchone()
                return result
        
        except sqlite3.DatabaseError as er:
            er = f"ERROR: unable to update user {er}"
            print(er)
            return er

    def get_user(self, eid):
        """Return a user record.
            [Attributes]
            eid: a string with the user EID
        """
        try:
            with SQLite(self.db_name) as cursor:
                result = cursor.execute(f"SELECT * FROM users WHERE eid='{eid}'").fetchone()
                return result
        except sqlite3.DatabaseError as e:
            er=f"ERROR: user not found {e}"
            print(er)
            return er

    def get_all_users(self):
        """Return all the users in the database"""
        try:
            with SQLite(self.db_name) as cursor:
                result = cursor.execute("SELECT id, first_name, last_name, eid, clock_in_time, clock_out_time, is_admin FROM users;").fetchall()
                return result
        except sqlite3.DatabaseError as e:
            er = f"ERROR: {e}"
            print(er)
            return(er)

    #Create a new timestamp
    def create_timestamp(self, data):
        """Create a timestamp with the given data.
            [Arguments]
            data: An array with the values in this order:
                    [clock_in, clock_out, late, too_early, exception, exception_description, user]
        """
        try:
            with SQLite(self.db_name) as cursor:
                date = datetime.today().strftime("%m/%d/%Y")
                data.insert(0, str(date))
                fields = ["date", "clock_in", "clock_out", "late", "too_early", "exception", "exception_description", "user"]
                query = f"INSERT INTO timestamp ({','.join(fields)}) VALUES ({str(data)[1:-1]});"
                cursor.execute(query)
                cursor.commit()
                result =  cursor.execute(f"SELECT * FROM timestamp WHERE date='{date}' and user={data[-1]}").fetchone()
                return result

        except sqlite3.DatabaseError as e:
            er = f"ERROR: unable to create timestamp {e}"
            print(er)
            return er

    def get_all_timestamps_form_user(self, user_id):
        """Returns all the timestamps from the given user"""
        try:
            with SQLite(self.db_name) as cursor:
                result = cursor.execute(f"SELECT * FROM timestamp WHERE user='{user_id}'").fetchall()
                return result
        
        except sqlite3.DatabaseError as e:
            er = f"ERROR: {e}"
            print(er)
            return(er)
        
    #get a timestamp
    def get_timestamp(self, eid, date=datetime.today().strftime("%m/%d/%Y")):
        """Get a user given timestamp by EID and date
            [Arguments]
            eid: a string with the user eid
            date: the date to query [optional], return the current
                    date if no value is given
        """
        try:
            with SQLite(self.db_name) as cursor:
                query = f"SELECT * FROM timestamp WHERE date='{date}' and user='{eid}'"
                result = cursor.execute(query).fetchone()
                return result
        
        except sqlite3.DatabaseError as e:
            er = f"ERROR: unable to retrieve the timestamp {e}"
            print(er)
            return er

    #Update a timestamp
    def update_timestamp(self, user_id, fields, timestamp_id):
        """Update a timestamp with the given data and user id
            [Arguments]
            id: an integer with the user id
        """
        try:
            with SQLite(self.db_name) as cursor:
                column_set = []
                for column in fields.keys():
                    column_set.append(f"{column} = '{fields[column]}'")
                query = f"UPDATE timestamp SET {','.join(column_set)} WHERE id='{timestamp_id}' AND user={user_id};" 
                cursor.execute(query)
                cursor.commit()
                result =  cursor.execute(f"SELECT * FROM timestamp WHERE id='{timestamp_id}' AND user={user_id};").fetchone()
                return result

        except sqlite3.DatabaseError as e:
            er = f"ERROR: Unable to update the timestamp {e}"
            print(er)
            return er
        
    #Check if the EID and password are correct
    def login(self, credentials):
        """Check if the eid and password are correct
            [Arguments]
            credentials: an object that contains the username and password as follows:
                        {"eid": "EID123456", "password": "asdf123!#"}
        """
        try:
            with SQLite(self.db_name) as cursor:
                user = cursor.execute(f"SELECT * FROM users WHERE eid='{credentials['eid']}';").fetchone()
                if user:
                    if user[USER_INDEXES.PASSWORD] == encrypt(credentials['password']):
                        return {"is_loged": True, "response": user}
                    else:
                        return "Invalid password."
                else:
                    return "User not found"

        except sqlite3.DatabaseError as e:
            er = f"ERROR: An error has occurred {e}"
            print(er)
            return er

    def initial_setup(self):
        """Initialize the database with the default name and create the initial tables"""
        try:
            self.create_table("users", {"id": "INTEGER PRIMARY KEY", "first_name": "TEXT", "last_name": "TEXT", "eid": "TEXT", "password": "TEXT", "is_admin": "INT", "clock_in_time": "TEXT", "clock_out_time": "TEXT"})
            self.create_child_table("timestamp", {"id": "INTEGER PRIMARY KEY", "date": "TEXT", "clock_in": "STRING", "clock_out": "STRING", "late": "INT", "too_early": "INT", "exception": "INT", "exception_description": "TEXT", "user": "INT"}, "user", "users", "id")
            admin_exists = self.get_user('EID123456')
            if not admin_exists:
                self.create_user(["admin", "admin", "EID123456","ASDF123ASDF", "10:50am", "18:40pm", 1])
        except sqlite3.DatabaseError as e:
            er = f"ERROR: Unable to initialize the database {e}"
            print(er)
            return er

if __name__ == '__main__':
    db = Database()

