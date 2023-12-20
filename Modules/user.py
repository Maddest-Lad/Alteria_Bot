from pathlib import Path
import json

DATA_DIR = Path("Data")
DATA_DIR.mkdir(exist_ok=True)

class User:  
    def __init__(self, id: str, username: str, history: list = None): 
        self.id = id        
        self.username = username  
        self.history = history if history is not None else []
        
        # Create File For New Users
        if not self.user_file.exists():
            self.save_to_json()

    @property
    def user_file(self) -> Path:
        return DATA_DIR / f"{self.id}.json"

    @classmethod 
    def from_json(cls, json_path: Path):
        """Load a User instance from a JSON file."""
        with json_path.open('r', encoding='utf-8') as json_file:
            json_object = json.load(json_file)
        return cls(json_object['id'], json_object['username'], json_object['history'])
    
    def save_to_json(self):
        """Save the current state of the user to a JSON file."""
        with self.user_file.open('w', encoding='utf-8') as json_file:
            json.dump(self.__dict__, json_file, indent=4)

    def get_history(self) -> list:
        """Return the user's history."""
        return self.history

    def add_to_history(self, addition: str):
        """Add an item to the user's history and save it."""
        self.history.append(addition)
        self.save_to_json()
