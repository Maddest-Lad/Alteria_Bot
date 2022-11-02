import subprocess

class DogCam:
    
    def __init__(self):
        self.terminal = None
        
    def start(self):
        if self.terminal is not None:
            return "DogCam is already running, you can view it at https://dog.madlad.io"
        else:
            print("Starting DogCam")
            self.terminal = subprocess.Popen("motion", shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return "Starting Up DogCam, view it at https://dog.madlad.io"
    
    def stop(self):
        if self.terminal is not None:
            self.terminal.kill()
            
            # Make Sure It's Extra Dead
            subprocess.run("killall motion", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Return Order to the Universe
            self.terminal = None
            return "Killed DogCam"
        else:
            return "DogCam is not currently running"