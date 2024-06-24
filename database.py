import os
import pyodbc as odbc
from datetime import datetime
from dotenv import load_dotenv
from db_queries import INSERT_URL_QUERY, GET_TASK_QUERY, INSERT_TASK_QUERY, UPDATE_TASK_QUERY, CHECK_QUERY, SUBSCRIPTION_QUERY, USER_QUERY
load_dotenv()


class DatabaseManager:
    def __init__(self):

        self.connecting_string = os.getenv("CONNECTION_STRING")

        # Define the query
        self.insert_url_query = INSERT_URL_QUERY
        self.get_task_query = GET_TASK_QUERY
        self.insert_task_query = INSERT_TASK_QUERY
        self.update_task_query = UPDATE_TASK_QUERY
        self.check_query = CHECK_QUERY
        self.subscription_query = SUBSCRIPTION_QUERY
        self.user_query = USER_QUERY

    # Define a method to get a connection
    def get_connection(self):
        try:
            return odbc.connect(self.connecting_string)
        except Exception as e:
            print(f"An error occurred while connecting to the database: {e}")
            raise e

    # Define a method to curd operation
    async def insert_url(self, user_id, url):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(self.insert_url_query, (url, user_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            if conn is not None:
                conn.close()

    async def insert_task(self, user_id, subscription_start_date, subscription_end_date, response):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            date = datetime.strptime(response['published'], '%a, %d %b %Y %H:%M:%S %z')
            formated_date = date.strftime('%Y-%m-%d %H:%M:%S')
            published_date = datetime.fromisoformat(formated_date)

            # Check if the data already exists
            cursor.execute(self.check_query, (user_id, response['title'], published_date, response['link']))
            data = cursor.fetchone()

            # If the data does not exist, insert it
            if subscription_start_date < published_date < subscription_end_date:
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
                    return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
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
            return None
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
