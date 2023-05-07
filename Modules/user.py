from pathlib import Path
import json

DATA_DIR = Path("Data")

class User:
    
    username: str
    id: str
    
    # For Daily Weather Reports
    location: str 
    report_time: str # By Hour 1-24
    
    def __init__(self, id, username, location=None, report_time=None):
        self.id = id        
        self.username = username
        self.location = location
        self.report_time = report_time
        
        # Create File For New Users
        if not Path.joinpath(DATA_DIR, id).exists():
            self.update_json()

    # Load From JSON File Constructor
    @classmethod 
    def from_json(cls, json_path: Path):
        with open(json_path, 'r') as json_file:
            user = json.load(json_file)
            return cls(user['id'], user['username'], user['location'], user['report_time'])
    
    # Overwrites The Existing File
    def update_json(self):
        with open(f"{Path.joinpath(DATA_DIR, self.id)}.json", 'w', encoding='utf-8') as json_file:
            json.dump(self.__dict__, json_file, skipkeys=True, indent=4)
            
    ### Weather Scheduler Information - Passing None will Opt Out 
    def set_location(self, location):
        self.location = location
        self.update_json()
    
    # PST Incoming Data Should be Convert to PST via utils.convert_to_pacific()
    def set_report_time(self, report_time):
        self.report_time = report_time
        self.update_json()    
