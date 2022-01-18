from tinydb import TinyDB, Query
import json
import asyncio
import time
import logging

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

class ProcessingService:

    def __init__(self):
        self.db = TinyDB('/home/pi/app/database/database/db.sensedata', create_dirs=True)

    def process_sense_event(self, event):
        logging.info(f"Inserting {str(event)}")
        sense_oject = json.loads(event)
        self.db.insert(sense_oject)
            