from celery import Celery
import os
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import Session
from pathlib import Path
from .db_orm import Temperature, User, Base

SOCK   = os.getenv("SOCK")
DB_URL = os.getenv("DB_URL")

# ensure that tables are created 
engine = create_engine(DB_URL, echo=True)
Base.metadata.create_all(engine)

# ===================================================
#                CELERY TASK QUEUE
# ===================================================
celery_app = Celery(
    main=__name__,
    broker=f"redis+socket://{SOCK}",
)

# ===================================================
#                REDIS STREAM 
# ===================================================
# red = redis.Redis(
#     unix_socket_path=SOCK,
#     decode_responses=True
# )

# # i want my main thread to be able to listen to the stream data every 1 second upload to the postgres
# while True:
#     data = red.xrevrange(name="readings", count=300)
#     df = (process_stream(data))
#     red.set("current_df", df.to_json())
#     first_row = df.iloc[[-1]]

#     stamp = int(first_row.iloc[0]["date"])
#     t1 = first_row.iloc[0]["Sensor 1"]
#     t2 = first_row.iloc[0]["Sensor 2"]
    
#     insert_record(sensor_id=1, timestamp=stamp, temperature_c=t1)
#     insert_record(sensor_id=2, timestamp=stamp, temperature_c=t2)

@celery_app.task(name="insert_record")
def insert_record(sensor_id, timestamp, temperature_c):
    reading = Temperature(sensor_id=sensor_id, timestamp=timestamp, temperature_c=temperature_c)
    print("READING", reading)
    engine = create_engine(DB_URL, echo=True)
    print("ENGINE IS CREATED")
    reading = Temperature(sensor_id=sensor_id, timestamp=timestamp, temperature_c=temperature_c)
    with Session(engine) as session:
        session.add(reading)
        session.commit()

# def send_emails(temperature):
#     # TODO
#     # pull from the user list
#     engine = create_engine(f"sqlite:///{DB_URL}")
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
