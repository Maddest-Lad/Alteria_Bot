from pathlib import Path
import json

DATA_DIR = Path("Data")

class User:
    # Base Discord Info
    username: str
    id: str

    # Weather Reporting
    location: str 
    report_time: str # By Hour 1-24

    # Text-Generation Chat Usage
    history: list
    
    def __init__(self, id, username, location=None, report_time=None, history=None): 
        self.id = id        
        self.username = username  
        self.location = location
        self.report_time = report_time
        self.history = history
        
        # Create File For New Users
        if not Path.joinpath(DATA_DIR, id).exists():
            self.update_json()

    # Load From JSON File Constructor
    @classmethod 
    def from_json(cls, json_path: Path):
        with open(json_path, 'r') as json_file:
            from_json = json.load(json_file)
            return cls(from_json['id'], from_json['username'], from_json['location'], from_json['report_time'], from_json['history'])
    
    # Overwrites The Existing File
    def update_json(self):
        with open(f"{Path.joinpath(DATA_DIR, self.id)}.json", 'w', encoding='utf-8') as json_file:
            json.dump(self.__dict__, json_file, skipkeys=True, indent=4)
            
    # Weather Scheduler Information - Passing None will Opt Out 
    def set_location(self, location):
        self.location = location
        self.update_json()
    
    # PST Incoming Data Should be Convert to PST via utils.convert_to_pacific()
    def set_report_time(self, report_time):
        self.report_time = report_time
        self.update_json()    

    # History Handler
    def get_history(self):
        if not self.history:
            self.history = []
        return self.history

    def add_to_history(self, addition):
        if not self.history:
            history = []
        self.history.append(addition)
        self.update_json()
