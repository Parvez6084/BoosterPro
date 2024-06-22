import pyodbc as odbc
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        # Define the connection string
        self.DRIVER_NAME = "SQL Server"
        self.SERVER_NAME = "L3T2167"
        self.DATABASE_NAME = "BoosterPro"
        self.uid = "sa"
        self.pwd = "Admin0011##"

        self.connecting_string = f"""
            DRIVER={{{self.DRIVER_NAME}}};
            SERVER={self.SERVER_NAME};
            DATABASE={self.DATABASE_NAME};
            Trusted_Connection=yes;
            uid={self.uid};
            pwd={self.pwd};
            """

        # Define the query
        self.insert_query = f"""
            INSERT INTO Task (UserId, Title, Summary, Published, Link)
            VALUES (?, ?, ?, ?, ?)
            """
        self.check_query = f"""
            SELECT * FROM Task WHERE UserId = ? AND Title = ? AND Published = ? AND Link = ?
            """

    # Define a method to get a connection
    def get_connection(self):
        return odbc.connect(self.connecting_string)

    # Define a method to insert a task
    async def insert_task(self, user_id, response):
        with self.get_connection() as conn:
            try:
                cursor = conn.cursor()
                dt = datetime.strptime(response['published'], '%a, %d %b %Y %H:%M:%S %z')
                formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S')

                # Check if the data already exists
                cursor.execute(self.check_query, (user_id, response['title'], formatted_dt, response['link']))
                data = cursor.fetchone()

                # If the data does not exist, insert it
                if data is None:
                   cursor.execute(self.insert_query, (user_id, response['title'], response['summary'], formatted_dt, response['link']))
                   conn.commit()

            except Exception as e:
                print(f"An error occurred: {e}")
                raise e
            
            finally:
                if conn is not None:
                    conn.close()