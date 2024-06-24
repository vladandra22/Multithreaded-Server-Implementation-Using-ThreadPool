import time
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

from threading import Lock

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('webserver.log', maxBytes=2048000, backupCount=5)
    ]
)
logging.Formatter.converter = time.gmtime

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

# webserver.task_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.job_counter = 1

# Lock folosit pentru a sincroniza variabila job counter,
# deoarece este o resursa impartita de thread-uri multiple.
webserver.job_id_lock = Lock()

from app import routes
