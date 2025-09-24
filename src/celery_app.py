from celery import Celery
import os

SOCK    = os.getenv("SOCK")
DB_PATH = os.getenv("DB_PATH", "app/database/sqlite/lab1.db")


# ===================================================
#                CELERY TASK QUEUE
# ===================================================
# we are using celery to handle the sending of emails
# and saving the stream data of the thermometer
# asynchronously
celery_app = Celery(
    main=__name__,
    broker=f"redis+socket://{SOCK}",
)