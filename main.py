from fastapi import FastAPI
import feedparser
from pydantic import BaseModel
from mail import send_email
from database import DatabaseManager

app = FastAPI()
dbContext = DatabaseManager()


class TaskIModel(BaseModel):
    url: str
    userId: str


@app.post("/api/url")
async def main(task: TaskIModel):
    feed = feedparser.parse(task.url)
    response = [
        {
            "title": entry.get('title', 'No title available'),
            "link": entry.get('link', 'No link available'),
            "summary": entry.get('summary', 'No summary available'),
            "published": entry.get('published', 'No publish date available'),
        }
        for entry in feed.entries
    ] if feed.entries else []

    # Insert the task into the database
    if response:
        for item in response:
            await dbContext.insert_task(task.userId, item)

    # for item in response:
    #     await send_email("rozarioux@gmail.com", item)

    return {str(response)}

async def subscriptionInfo(userId: str):
    return await dbContext.get_subscription_info(userId)
