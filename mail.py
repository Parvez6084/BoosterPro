from redmail import gmail


async def send_email(to_email, body):
    gmail.username = 'parvez.ka19@gmail.com'
    gmail.password = 'oczl iygc zlsf mhbz'
    subject = 'BoosterPro - New opportunity on Upwork!'
    html = f"""
    <!DOCTYPE html>
        <html lang="en">
        <body>
            <h3>{body['title']}</h3>
            <p><strong>Description:</strong> {body['summary']}</p>
            <p><strong>Link:</strong> {body['link']}</p>
        </body>
        </html>
    """
    gmail.send(subject=subject, receivers=[to_email], html=html)
