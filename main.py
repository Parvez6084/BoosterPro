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


async def set_task_worker(userId: str):
    result = await dbContext.get_subscription_info(userId)
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
                    await dbContext.insert_task(userId, active_date, item)


async def send_email_worker(userId: str):
    response = await dbContext.get_all_tasks(userId)
    if response:
        for item in response:
            send = await send_email(response['Email'], item)
            if send:
                await dbContext.update_task(item['Id'], userId)
