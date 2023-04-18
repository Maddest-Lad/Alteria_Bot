import json 
import os
from datetime import datetime
from pathlib import Path

def log(*value):
    log_entry = {"date": datetime.now().isoformat(), "value": json.dumps(value) } 
    with open(Path("Logs/log.json"), 'a') as log:
        json.dump(log_entry, log)
        log.write(os.linesep)