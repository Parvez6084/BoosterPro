import feedparser
from mail import send_email
from database import DatabaseManager
from model.request_model import UserReqModel
from model.response_model import TaskResponseModel
from fastapi import Depends, FastAPI

app = FastAPI()


async def create_user(user: UserReqModel, db=Depends(DatabaseManager)):
    try:
        response = await db.insert_user(user.userId, user.fullName, user.email, user.password)
        if response is True:
            return {'status': 'User inserted successfully'}
        else:
            return {'status': 'failed'}
    except Exception as e:
        return {'status': 'failed', 'error': str(e)}


@app.post("/api/url")
async def set_url(user: UserReqModel, db=Depends(DatabaseManager)):
    try:
        response = await db.insert_url(user.userId, user.url)
        if response is True:
            #await set_task_worker(user.userId)
            return {'status': 'URL inserted successfully'}
        else:
            return {'status': 'failed'}
    except Exception as e:
        return {'status': 'failed', 'error': str(e)}


async def set_task_worker(user_id: str, dbContext=Depends(DatabaseManager)):
    try:
        result = dbContext.get_subscription_info(user_id)
        is_subscribed = result[0]
        subscription_start_date = result[1]
        subscription_end_date = result[2]
        get_url = result[3]

        if is_subscribed is True:
            feed = feedparser.parse(get_url)
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
            if subscription_start_date and subscription_end_date is not None:
                if response:
                    for item in response:
                        result = await dbContext.insert_task(
                            user_id,
                            subscription_start_date,
                            subscription_end_date,
                            item
                        )
                    if result is True:
                        await send_email_worker(user_id)
    except Exception as e:
        print(f"Error in set_task_worker: {str(e)}")


async def send_email_worker(user_id: str, dbContext=Depends(DatabaseManager)):
    try:
        tasks = await dbContext.get_all_tasks(user_id)
        for task in tasks:
            task_model = TaskResponseModel(
                id=task[0],
                user_id=task[1],
                is_email_send=task[2],
                title=task[3],
                summary=task[4],
                published=task[5],
                link=task[6],
                email=task[7]
            )
            send = await send_email(task_model)
            if send:
                await dbContext.update_task(task_model.id, user_id)
    except Exception as e:
        print(f"Error in send_email_worker: {str(e)}")
