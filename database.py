import pyodbc as odbc
from datetime import datetime
from database_credentials import (CONNECTION_STRING, INSERT_URL_QUERY, GET_TASK_QUERY,
                                  INSERT_TASK_QUERY, UPDATE_TASK_QUERY,
                                  CHECK_QUERY, SUBSCRIPTION_QUERY)


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connection_string = CONNECTION_STRING
        self.connection = odbc.connect(self.connection_string)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
            self.connection = None

    async def insert_url(self, user_id, url):
        try:
            cursor = self.connection.cursor()
            cursor.execute(INSERT_URL_QUERY, (url, user_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    async def insert_task(self, user_id, subscription_start_date, subscription_end_date, response):
        try:
            cursor = self.connection.cursor()
            date = datetime.strptime(response['published'], '%a, %d %b %Y %H:%M:%S %z')
            formated_date = date.strftime('%Y-%m-%d %H:%M:%S')
            published_date = datetime.fromisoformat(formated_date)

            cursor.execute(CHECK_QUERY, (user_id, response['title'], published_date, response['link']))
            data = cursor.fetchone()

            if subscription_start_date < published_date < subscription_end_date:
                if data is None:
                    cursor.execute(
                        INSERT_TASK_QUERY, (
                            user_id,
                            response['title'],
                            response['summary'],
                            published_date,
                            response['link']
                        )
                    )
                    self.connection.commit()
                    return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    async def update_task(self, task_id, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(UPDATE_TASK_QUERY, task_id, user_id)
            self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e

    async def get_subscription_info(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(SUBSCRIPTION_QUERY, user_id)
            data = cursor.fetchone()
            return data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    async def get_all_tasks(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(GET_TASK_QUERY, user_id)
            data = cursor.fetchall()
            return data
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
