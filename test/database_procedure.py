# import os
# import pyodbc as odbc
# from datetime import datetime
# from dotenv import load_dotenv
# from db_queries import INSERT_URL_QUERY, GET_TASK_QUERY, INSERT_TASK_QUERY, UPDATE_TASK_QUERY, CHECK_QUERY, \
#     SUBSCRIPTION_QUERY, USER_QUERY
#
# load_dotenv()
#
#
# class DatabaseManager:
#     def __init__(self):
#         self.connecting_string = os.getenv("CONNECTION_STRING")
#         self.insert_url_query = INSERT_URL_QUERY
#         self.get_task_query = GET_TASK_QUERY
#         self.update_task_query = UPDATE_TASK_QUERY
#         self.user_query = USER_QUERY
#         self.connection = None
#
#     def __enter__(self):
#         self.connection = odbc.connect(self.connecting_string)
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if self.connection:
#             self.connection.close()
#             self.connection = None
#
#     async def insert_url(self, user_id, url):
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute(self.insert_url_query, (url, user_id))
#             self.connection.commit()
#             return True
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return False
#
#     async def insert_task(self, user_id, response):
#         try:
#             cursor = self.connection.cursor()
#             date = datetime.strptime(response['published'], '%a, %d %b %Y %H:%M:%S %z')
#             formated_date = date.strftime('%Y-%m-%d %H:%M:%S')
#             published_date = datetime.fromisoformat(formated_date)
#             cursor.execute("EXEC InsertTaskInfo ?, ?, ?, ?, ?",
#                            user_id, response['title'],
#                            response['summary'], response['link'],
#                            published_date)
#             self.connection.commit()
#             return True
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return False
#
#     async def update_task(self, task_id, user_id):
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute(self.update_task_query, task_id, user_id)
#             self.connection.commit()
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             raise e
#
#     async def get_subscription_info(self, user_id):
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute("EXEC GetSubscriptionInfo ?", user_id)
#             data = cursor.fetchone()
#             return data
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return None
#
#     async def get_all_tasks(self, user_id):
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute(self.get_task_query, user_id)
#             data = cursor.fetchall()
#             return data
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             raise e
#
#     async def get_user_info(self, user_id):
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute(self.user_query, user_id)
#             data = cursor.fetchone()
#             return data
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             raise e
