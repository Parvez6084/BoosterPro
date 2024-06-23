from fastapi import FastAPI
import feedparser
from pydantic import BaseModel
from mail import send_email
from database import DatabaseManager

app = FastAPI()
dbContext = DatabaseManager()


class TaskModel(BaseModel):
    url: str
    userId: str


@app.post("/api/url")
async def set_url(task: TaskModel):
    response = await dbContext.insert_url(task.userId, task.url)
    if response is None:
        return {'status': 'failed'}
    else:
        return {'status': 'ok'}


async def set_task_worker(user_id: str):
    result = await dbContext.get_subscription_info(user_id)
    if result['IsSubscribed'] == 1:
        feed = feedparser.parse(result['URL'])
        response = [
            {
                "title": entry.get('title', 'No title available'),
                "link": entry.get('link', 'No link available'),
                "summary": entry.get('summary', 'No summary available'),
                "published": entry.get('published', 'No publish date available'),
            }
            for entry in feed.entries
        ] if feed.entries else []

        active_date = result['SubscribedStartDate']
        if active_date is not None:
            # Insert the task into the database
            if response:
                for item in response:
                    await dbContext.insert_task(user_id, active_date, item)


async def send_email_worker(user_id: str):
    response = await dbContext.get_all_tasks(user_id)
    if response:
        for item in response:
            send = await send_email(response['Email'], item)
            if send:
                await dbContext.update_task(item['Id'], user_id)
