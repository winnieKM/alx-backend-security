from celery import shared_task

@shared_task
def send_test_email():
    print("Test email sent successfully!")
    return "Email sent"
@shared_task
def debug_task():
    print("Debug task executed!")
    return "Debug task executed!"