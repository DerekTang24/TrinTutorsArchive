import sqlite3
import random

class Tutee:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "tutees"
    
    def initialize_tutees_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    email TEXT UNIQUE,
                    tuteename TEXT UNIQUE,
                    password TEXT
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()

    def exists(self, tuteename=None, id=None):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if tuteename:
                # Check if a tutee with the given tuteename exists
                query = "SELECT COUNT(*) FROM tutees WHERE tuteename = ?"
                cursor.execute(query, (tuteename,))
            elif id:
                # Check if a tutee with the given ID exists
                query = "SELECT COUNT(*) FROM tutees WHERE id = ?"
                cursor.execute(query, (id,))
            else:
                return {"result": "error", 
                        "message": "Invalid input"}

            count = cursor.fetchone()[0]
            exists = count > 0

            return {"result": "success", 
                    "message": exists}

        except sqlite3.Error as error:
            return {"result": "error", "message": str(error)}
        
        finally:
            db_connection.close()

    def create_tutee(self, tutee_details):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            tutee_id = random.randint(0, 9007199254740992)
            while self.exists(id=tutee_id)["message"]:
                tutee_id = random.randint(0, 9007199254740992)

            cursor.execute("SELECT * FROM tutees WHERE tuteename = ?;", (tutee_details["tuteename"],))
            tutee_data_tuteename = cursor.fetchone()
            cursor.execute("SELECT * FROM tutees WHERE email = ?;", (tutee_details["email"],))
            tutee_data_email = cursor.fetchone()
            if tutee_data_tuteename:
                db_connection.commit()
                return {"result": "error", "message": "tuteename already exists"}
            
            if tutee_data_email:
                db_connection.commit()
                return {"result": "error", "message": "Email already exists"}

            tutee_data = (tutee_id, tutee_details["email"], tutee_details["tuteename"], tutee_details["password"])
            if '@' not in tutee_details["email"]:
                return {"result": "error", "message": "Incorrect format: Email address must contain '@'"}
            email_parts = tutee_details["email"].split('.')
            if len(email_parts[-1]) != 3:
                return {"result": "error", "message": "Incorrect format: Email address must have a '.' three letters from the end"}
            special_characters = "!@#$%^&*()-=+[]{};:'\"<>,./?\\|"
            if any(char in special_characters for char in tutee_details["tuteename"]):               
                return {"result": "error", "message": "Invalid tuteename: Special characters are not allowed"}
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", tutee_data)
            db_connection.commit()

            return {"result": "success", "message": {
                "id": tutee_id,
                "email": tutee_details["email"],
                "tuteename": tutee_details["tuteename"],
                "password": tutee_details["password"]
            }}
        except sqlite3.Error as error:
            return {"result":"error", "message": error}
        finally:
            db_connection.close()

    def get_tutee(self, tuteename = None, id = None):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if tuteename:
                query = "SELECT COUNT(*) FROM tutees WHERE tuteename = ?"
                cursor.execute(query, (tuteename,))
                count = cursor.fetchone()[0]

                query = f"SELECT * FROM {self.table_name} WHERE tuteename = ?;"
                results = cursor.execute(query, (tuteename,))
            elif id:
                query = f"SELECT * FROM {self.table_name} WHERE id = ?;"
                results = cursor.execute(query, (id,))
            else:
                return {"result": "error", "message": "Please provide either 'tuteename' or 'id'."}

            tutee_data = results.fetchone()
            if tutee_data:
                return {"result": "success", "message": {
                    "id": tutee_data[0],
                    "email": tutee_data[1],
                    "tuteename": tutee_data[2],
                    "password": tutee_data[3]
                }}
            else:
                return {"result": "error", "message": "tutee not found"}
        except sqlite3.Error as error:
            return {"result": "error", "message": error}
        finally:
            db_connection.close()
    
    def get_tutees(self):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * FROM {self.table_name};"
            results = cursor.execute(query)
            all_tutees = []

            for tutee_data in results.fetchall():
                tutee = {
                    "id": tutee_data[0],
                    "email": tutee_data[1],
                    "tuteename": tutee_data[2],
                    "password": tutee_data[3]
                }
                all_tutees.append(tutee)

            return {
                "result": "success",
                "message": all_tutees
            }

        except sqlite3.Error as error:
            return {
                "result": "error",
                "message": str(error)
            }

        finally:
            db_connection.close()

    def remove_tutee(self, tuteename):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM tutees WHERE tuteename = ?;", (tuteename,))
            tutee_data = cursor.fetchone()
            if tutee_data:
                # Delete the tutee from the 'tutees' table
                cursor.execute("DELETE FROM tutees WHERE tuteename = ?;", (tuteename,))
                db_connection.commit()
            else:
                return {"result": "error", 
                        "message": f"tutee '{tuteename}' not found"}
        except sqlite3.Error as error:
            return {"result": "error", 
                    "message": error}
        finally:
            db_connection.close()
        return {"result": "success", 
                "message": {"id": tutee_data[0], "email": tutee_data[1], "tuteename": tutee_data[2], "password": tutee_data[3]}}
    
    def update_tutee(self, tutee_data):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE id = ?;", (tutee_data["id"],))
            count = cursor.fetchone()[0]
            if count == 0:
                return {"result": "error", "message": "tutee does not exist"}
            cursor.execute(f"UPDATE {self.table_name} SET email = ?, tuteename = ?, password = ? WHERE id = ?;", (tutee_data["email"], tutee_data["tuteename"], tutee_data["password"], tutee_data["id"]))
            db_connection.commit()
            return {"result": "success", 
                    "message": tutee_data}
        except sqlite3.Error as error:
            return {"result": "error", 
                    "message": error}
        finally:
            db_connection.close()