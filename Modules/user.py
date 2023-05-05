from pathlib import Path
import json

DATA_DIR = Path("Data")

class User:
    
    username: str
    id: str
    location: str # For Weather Reports
    
    def __init__(self, id, username, location=None):
        self.id = id        
        self.username = username
        self.location = location
        
        # Create File For New Users
        if not Path.joinpath(DATA_DIR, id).exists():
            self.update_json()

    # Load From JSON File Constructor
    @classmethod 
    def from_json(cls, json_path: Path):
        with open(json_path, 'r') as json_file:
            user = json.load(json_file)
            return cls(user['id'], user['username'], user['location'])
    
    # Overwrites The Existing File
    def update_json(self):
        with open(f"{Path.joinpath(DATA_DIR, self.id)}.json", 'w', encoding='utf-8') as json_file:
            json.dump(self.__dict__, json_file, skipkeys=True, indent=4)
            
    # Set The Location (Opt into Weather Notifications), Passing None will Opt Out 
    def set_location(self, location):
        self.location = location
        self.update_json()

# Testing
if __name__ == "__main__":
    b = User.from_json("Data/165971552771244033.json")
    b.set_location(None)
    print(b.location)
