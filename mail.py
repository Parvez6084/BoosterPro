from redmail import gmail

from model.response_model import TaskResponseModel


async def send_email(body):
    gmail.username = 'parvez.ka19@gmail.com'
    gmail.password = 'oczl iygc zlsf mhbz'
    subject = 'BoosterPro - New opportunity on Upwork!'
    task: TaskResponseModel = body

    html = f"""
    <!DOCTYPE html>
        <html lang="en">
        <body>
            <h3>{task.title}</h3>
            <p><strong>Description:</strong> {task.summary}</p>
            <p><strong>Link:</strong> {task.link}</p>
        </body>
        </html>
    """

    return gmail.send(subject=subject, receivers=[task.email], html=html)
