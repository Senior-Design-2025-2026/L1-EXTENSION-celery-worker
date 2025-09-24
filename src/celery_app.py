from celery import Celery
import os
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import Session
from pathlib import Path

SOCK    = os.getenv("SOCK")
DB_PATH = os.getenv("DB_PATH")

print(f"CURRENT PATH {Path.cwd()}")

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

@celery_app.task(name="insert_record")
def insert_record(sensor_id, timestamp, temperature_c):
    print("CELERY ADDING TO POSTGRES", sensor_id, timestamp, temperature_c)
    # engine = create_engine(f"sqlite:///..{DB_PATH}")
    # reading = Temperature(sensor_id=sensor_id, timestamp=timestamp, temperature_c=temperature_c)
    # with Session(engine) as session:
    #     session.add(reading)
    #     session.commit()


# def send_emails(temperature):
#     # TODO
#     # pull from the user list
#     engine = create_engine(f"sqlite:///{DB_PATH}")
#     with Session(engine) as session:
#         users = session.execute(
#                 select(User).where(User.email_addr)
#             )
#         
#         # parse the Result as a dictionary
#         for user in users.to_dict():
#             message = f"Recorded 4 consecutive {temperature} readings"
#             email_addr = user.get("email_addr")
#             send_email(email_addr, message)


# @celery_app.task()
# def send_email(addr: str, message: str):
#     # todo
#     print("sending email")
