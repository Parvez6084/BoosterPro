# from fastapi import FastAPI
# import feedparser
# from mail import send_email
# from database import DatabaseManager
# from model.request_model import TaskModel
# from model.response_model import TaskResponseModel
#
# app = FastAPI()
#
#
# @app.post("/api/url")
# async def set_url(task: TaskModel):
#     with DatabaseManager() as dbContext:
#         response = await dbContext.insert_url(task.userId, task.url)
#         if response is True:
#             await set_task_worker(task.userId)
#             return {'status': 'URL inserted successfully'}
#         else:
#             return {'status': 'failed'}
#
#
# async def set_task_worker(user_id: str):
#     with DatabaseManager() as dbContext:
#         result = await dbContext.get_subscription_info(user_id)
#         is_subscribed = result[0]
#         get_url = result[1]
#         if is_subscribed is True:
#             feed = feedparser.parse(get_url)
#             response = [
#                 {
#                     "title": entry.get('title', 'No title available'),
#                     "link": entry.get('link', 'No link available'),
#                     "summary": entry.get('summary', 'No summary available'),
#                     "published": entry.get('published', 'No publish date available'),
#                 }
#                 for entry in feed.entries
#             ] if feed.entries else []
#             if response:
#                 for item in response:
#                     result = await dbContext.insert_task(user_id, item)
#                     if result is True:
#                         await send_email_worker(user_id)
#
#
# async def send_email_worker(user_id: str):
#     with DatabaseManager() as dbContext:
#         response = await dbContext.get_all_tasks(user_id)
#         if response:
#             for item in response:
#                 task = TaskResponseModel(
#                     id=item[0],
#                     user_id=item[1],
#                     is_email_send=item[2],
#                     title=item[3],
#                     summary=item[4],
#                     published=item[5],
#                     link=item[6],
#                     email=item[7]
#                 )
#                 send = await send_email(task)
#                 if send:
#                     await dbContext.update_task(task.id, user_id)
