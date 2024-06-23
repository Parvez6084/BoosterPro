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
        self.insert_url_query = """UPDATE User_Information SET (URL) VALUE (?) WHERE UserId =?"""
        self.get_task_query = """SELECT * FROM Task_Information WHERE UserId = ? AND IsSendEmail = 0"""
        self.insert_task_query = """INSERT INTO Task_Information (UserId, Title, Summary, Published, Link) VALUES (?, ?, ?, ?, ?)"""
        self.update_task_query = """UPDATE Task_Information SET IsSendEmail = 1 WHERE Id = ? AND UserId = ?"""
        self.check_query = """SELECT * FROM Task_Information WHERE UserId = ? AND Title = ? AND Published = ? AND Link = ? """
        self.subscription_query = """SELECT ui.IsSubscribed, si.SubscribedStartDate, ui.URL FROM User_Information as ui
                INNER JOIN Subscribed_Information as si on ui.UserId = si.UserId WHERE UserId = ?"""
        self.user_query = """SELECT * FROM User_Information WHERE UserId = ?"""

    # Define a method to get a connection
    def get_connection(self):
        return odbc.connect(self.connecting_string)

    # Define a method to curd operation
    async def insert_url(self, user_id, url):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(self.insert_url_query, (url, user_id))
            conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        finally:
            if conn is not None:
                conn.close()

    async def insert_task(self, user_id, active_date, response):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            dt = datetime.strptime(response['published'], '%a, %d %b %Y %H:%M:%S %z')
            published_date = dt.strftime('%Y-%m-%d %H:%M:%S')

            # Check if the data already exists
            cursor.execute(self.check_query, (user_id, response['title'], published_date, response['link']))
            data = cursor.fetchone()

            # If the data does not exist, insert it
            if published_date >= active_date:
                if data is None:
                    cursor.execute(
                        self.insert_task_query, (
                            user_id,
                            response['title'],
                            response['summary'],
                            published_date,
                            response['link']
                        )
                    )
                    conn.commit()

        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        finally:
            if conn is not None:
                conn.close()

    async def update_task(self, task_id, user_id):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(self.update_task_query, task_id, user_id)
            conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        finally:
            if conn is not None:
                conn.close()

    async def get_subscription_info(self, user_id):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(self.subscription_query, user_id)
            data = cursor.fetchone()
            return data
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        finally:
            if conn is not None:
                conn.close()

    async def get_user_info(self, user_id):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(self.user_query, user_id)
            data = cursor.fetchone()
            return data
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        finally:
            if conn is not None:
                conn.close()

    async def get_all_tasks(self, user_id):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(self.get_task_query, user_id)
            data = cursor.fetchall()
            return data
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        finally:
            if conn is not None:
                conn.close()
