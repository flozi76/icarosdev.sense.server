from tinydb import TinyDB, Query
import json
import asyncio
import time

class ProcessingService:

    def __init__(self):
        self.db = TinyDB('/home/pi/app/database/database/db.sensedata', create_dirs=True)

    def process_sense_event(self, event):
        print(f"Inserting {str(event)}")
        sense_oject = json.loads(event)
        self.db.insert(sense_oject)
            