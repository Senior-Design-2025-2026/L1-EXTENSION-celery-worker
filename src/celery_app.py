from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from pathlib import Path
import os
import redis

from .db_orm import Temperature, User, Base

SOCK   = os.getenv("SOCK")
DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL, echo=True)
Base.metadata.create_all(engine)

# ===================================================
#                REDIS STREAM + CACHE
# ===================================================
red = redis.Redis(
    unix_socket_path=SOCK,
    decode_responses=True
)

# ===================================================
#                CELERY TASK QUEUE
# ===================================================
# building one engine (db conn) per worker. this is running with a pi4 
# so this entire setup is definitely overkill... it is possible that 
# we stick with the http sending of data from our temperature sensor 
# and use a more capable machine to reap the benefits of celery, task queues,
# database storage, and quicker analytics.
#
# the purpose of the initializer setup (and more importantly using sessionmaker)
# is to reduce the tcp handshaking required for making an engine connection. 
# The sessionmaker is a factory bound to the engine connection. This allows each task
# to simply borrow connections from the pool, perfom the insertion, and return the 
# connection to the pool
celery_app = Celery(
    main=__name__,
    broker=f"redis+socket://{SOCK}",
)

_engine = None
_Session = None

@worker_process_init.connect
def initialize_new_worker(**kwargs):    
    global _engine, _Session                                    
    _engine = create_engine(DB_URL, echo=False)
    # Base.metadata.create_all(_engine)                             # @team: keep commented; only run if tables arent already created or the db gets nuked
    _Session = sessionmaker(bind=_engine, expire_on_commit=False)

@celery_app.task(name="insert_record")
def insert_record(sensor_id, timestamp, temperature_c):
    session = _Session()
    try:
        reading = Temperature(sensor_id=sensor_id, timestamp=timestamp, temperature_c=temperature_c)
        session.add(reading)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

@celery_app.task()
def send_email(addr: str, message: str):
    # if not red.exists("emails"):
    #     emails = get_mailing_list()
    #     red.set("emails", json.dumps(emails))
    # else:
    #     emails = json.loads(red.get("emails"))

    print("sending emails now...")

@worker_process_shutdown.connect
def safely_destroy_worker(**_):
    _engine.dispose()