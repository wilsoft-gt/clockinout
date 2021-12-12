import sqlite3
from datetime import datetime
import hashlib
from .helpers import USER_INDEXES

def encrypt(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest() 

class Database:
    """Database class handler to manage all the users info, etc."""
    def __init__(self, database_name = "database.db"):
        self.database_name = database_name
        self.database = sqlite3.connect(self.database_name)
        self.cursor = self.database.cursor()
    
    #create a table if not exist
    def create_table(self, name, fields):
        """Create a table with the given name.
            [Arguments]
            name: The name for the table
            fields: an object with the field name and type ex:
                    {"id": "INT", "name": "TEXT", "phone": "TEXT"}
        """
        try:
            fields_str = [] 
            for field in fields.keys():
                fields_str.append(f"{field} {fields[field]}")
            query = f"CREATE TABLE IF NOT EXISTS {name} ({(',').join(fields_str)});"
            self.cursor.execute(query)
            result = self.cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{name}';").fetchone()
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
            self.cursor.execute("DROP TABLE IF EXISTS {name};")
            result = self.cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name = '{name}';").fetchone()
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
            fields_string = []
            for key in fields.keys():
                fields_string.append(f"{key} {fields[key]}")

            query = f"""CREATE TABLE IF NOT EXISTS {name} (
            {','.join(fields_string)}, 
            FOREIGN KEY ({field_id}) REFERENCES {parent_name} ({parent_field})
            ON DELETE CASCADE
            );"""
            self.cursor.execute(query)
            result = self.cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{name}';").fetchone()
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
            data[3] = encrypt(data[3]) #encrypt password
            fields = ["first_name", "last_name", "eid", "password", "clock_in_time", "clock_out_time", "is_admin"]
            query = f"INSERT INTO users ({','.join(fields)}) VALUES ({str(data)[1:-1]});"
            self.cursor.execute(query)
            self.database.commit()
            result = self.cursor.execute(f"SELECT * FROM users WHERE first_name = '{data[0]}' AND last_name = '{data[1]}' AND eid = '{data[2]}';").fetchone()
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
            column_set = []
            for column in fields.keys():
                column_set.append(f"{column} = '{fields[column]}'")
            query = f"UPDATE users SET {','.join(column_set)} WHERE id = {id};"
            self.cursor.execute(query)
            self.database.commit()
            result = self.cursor.execute(f"SELECT * FROM users WHERE id = '{id}';").fetchone()
            return result
        
        except sqlite3.DatabaseError as e:
            er = f"ERROR: unable to update user {e}"
            print(e)
            return er

    def get_user(self, eid):
        """Return a user record.
            [Attributes]
            eid: a string with the user EID
        """
        try:
            result = self.cursor.execute(f"SELECT * FROM users WHERE eid='{eid}'").fetchone()
            return result
        except sqlite3.DatabaseError as e:
            er=f"ERROR: user not found {e}"
            print(er)
            return er

    def get_all_users(self):
        """Return all the users in the database"""
        try:
            result = self.cursor.execute("SELECT id, first_name, last_name, eid, clock_in_time, clock_out_time, is_admin FROM users;").fetchall()
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
            date = datetime.today().strftime("%m/%d/%Y")
            data.insert(0, str(date))
            fields = ["date", "clock_in", "clock_out", "late", "too_early", "exception", "exception_description", "user"]
            query = f"INSERT INTO timestamp ({','.join(fields)}) VALUES ({str(data)[1:-1]});"
            self.cursor.execute(query)
            self.database.commit()
            result =  self.cursor.execute(f"SELECT * FROM timestamp WHERE date='{date}' and user={data[-1]}").fetchone()
            return result

        except sqlite3.DatabaseError as e:
            er = f"ERROR: unable to create timestamp {e}"
            print(er)
            return er

    def get_all_timestamps_form_user(self, user_id):
        """Returns all the timestamps from the given user"""
        try:
            result = self.cursor.execute(f"SELECT * FROM timestamp WHERE user='{user_id}'").fetchall()
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
            query = f"SELECT * FROM timestamp WHERE date='{date}' and user='{eid}'"
            result = self.cursor.execute(query).fetchone()
            return result
        
        except sqlite3.DatabaseError as e:
            er = f"ERROR: unable to retrieve the timestamp {e}"
            print(er)
            return er

    #Update a timestamp
    def update_timestamp(self, user_id, fields, date=datetime.today().strftime("%m/%d/%Y")):
        """Update a timestamp with the given data and user id
            [Arguments]
            id: an integer with the user id
        """
        try:
            column_set = []
            for column in fields.keys():
                column_set.append(f"{column} = '{fields[column]}'")
            query = f"UPDATE timestamp SET {','.join(column_set)} WHERE date='{date}' AND user={user_id};" 
            self.cursor.execute(query)
            self.database.commit()
            result =  self.cursor.execute(f"SELECT * FROM timestamp WHERE date='{date}' AND user={user_id};").fetchone()
            print(result)
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
            user = self.cursor.execute(f"SELECT * FROM users WHERE eid='{credentials['eid']}';").fetchone()
            print(credentials)
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

    #close the database connection
    def close(self):
        """Close the database connection"""
        try:
           self.cursor.close()
           self.database.close()
        except sqlite3.DatabaseError as e:
            er = f"ERROR: Unable to close database {e}"
            print(er)
            return er

    def initial_setup(self):
        """Initialize the database with the default name and create the initial tables"""
        try:
            self.create_table("users", {"id": "INTEGER PRIMARY KEY", "first_name": "TEXT", "last_name": "TEXT", "eid": "TEXT", "password": "TEXT", "is_admin": "INT", "clock_in_time": "TEXT", "clock_out_time": "TEXT"})
            self.create_child_table("timestamp", {"id": "INTEGER PRIMARY KEY", "date": "TEXT", "clock_in": "STRING", "clock_out": "STRING", "late": "INT", "too_early": "INT", "exception": "INT", "exception_description": "TEXT", "user": "INT"}, "user", "users", "id")
            self.close()
        except sqlite3.DatabaseError as e:
            er = f"ERROR: Unable to initialize the database {e}"
            print(er)
            return er

if __name__ == '__main__':
    db = Database()
    #res = db.create_table("users", {"id": "INTEGER PRIMARY KEY", "first_name": "TEXT", "last_name": "TEXT", "eid": "TEXT", "password": "TEXT", "is_admin": "INT", "clock_in_time": "TEXT", "clock_out_time": "TEXT"})
    #print(f"Create table: \n {res}")
    #res = db.create_child_table("timestamp", {"id": "INTEGER PRIMARY KEY", "date": "TEXT", "clock_in": "STRING", "clock_out": "STRING", "late": "INT", "too_early": "INT", "exception": "INT", "exception_description": "TEXT", "user": "INT"}, "user", "users", "id")
    #print(f"Create child table: \n {res}")
    #res = db.create_user(["Wilson", "Romero", "EID123456", "Wilson4291", "10:50AM", "19:00PM", 1])
    #print(f"Create user: \n{res}")
    #db.create_user(["Alejandra", "Alvarez", "EID123457", "alejandra0193", "10:00AM", "18:30PM", 0])
    #db.create_user(["Alison", "Romero", "EID123458", "alison2018", "10:00AM", "18:30PM", 0])
    #db.create_user(["Samuel", "Romero", "EID123459", "samuel2020", "9:00AM", "17:30PM", 0])
    #res = db.create_timestamp(["", "", 0, 0, 0, "", 1])
    #print(f"Create timestamp: \n{res}")
    #res = db.update_user(1,{"is_admin": 0})
    #print(f"Update user: \n{res}")
    #res = db.update_user(1,{"is_admin": 1})
    #print(f"Updated user again: \n {res}")
    #res = db.update_timestamp(1, {"clock_in": "10:50AM"})
    #print(f"Updated timestamp: \n {res}")
    
    res = db.login({"eid": "EID123457", "password": "alejandra0193"})
    print(res)
    res = db.login({"eid": "EID123459", "password": "samuel2020"})
    print(res)
    res = db.login({"eid": "EID123987", "password": "alison123123"})
    print(res)
