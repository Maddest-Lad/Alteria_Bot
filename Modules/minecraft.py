import subprocess
import time
import threading
import os
import signal

class MinecraftServerManager:
    _instance = None
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if MinecraftServerManager._instance is None:
            with MinecraftServerManager._lock:
                if MinecraftServerManager._instance is None:
                    MinecraftServerManager._instance = MinecraftServerManager()
        return MinecraftServerManager._instance

    def __init__(self):
        self.process = None
        self.restart_attempts = 0
        self.max_restarts = 10
        self.server_running = False
        self.restart_delay = 2  # Seconds before restart attempt

    def start_server(self):
        if self.server_running:
            return "Server is already running."

        self.restart_attempts = 0
        self.server_running = True
        self._run_server()
        return("Starting Server")

    def _run_server(self):
        while self.server_running and self.restart_attempts < self.max_restarts:
            print("Starting the Minecraft server...")
            self.process = subprocess.Popen(
                ['java', '@user_jvm_args.txt', '@libraries/net/neoforged/neoforge/21.0.167/unix_args.txt' , '\"$@\"'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd="/home/sam/MinecraftServers/AllTheMods10_Maddie/")
            self.process.wait()

            if not self.server_running:  # Manual stop
                print("Server manually stopped.")
                break

            print("Server crashed or stopped unexpectedly. Restarting in {} seconds...".format(self.restart_delay))
            self.restart_attempts += 1
            time.sleep(self.restart_delay)

        if self.restart_attempts >= self.max_restarts:
            print("Max restart attempts reached. Server will not restart.")
            self.server_running = False

    def stop_server(self):
        if not self.server_running or self.process is None:
            return "Server is not running."

        print("Stopping the Minecraft server...")
        self.server_running = False
        self._graceful_shutdown()
        return "Server Stopped."

    def _graceful_shutdown(self, timeout=10):
        if self.process:
            try:
                self.process.terminate()
                print("Waiting for server to shut down gracefully...")
                self.process.wait(timeout)
            except subprocess.TimeoutExpired:
                print("Graceful shutdown timed out. Forcing termination...")
                self.process.kill()
            finally:
                self.process = None
                print("Server stopped.")

    def restart_server(self):
        print("Restarting the Minecraft server...")
        self.stop_server()
        time.sleep(self.restart_delay)
        self.start_server()
        return "Server Restarted"


# Example usage
if __name__ == "__main__":
    manager = MinecraftServerManager.get_instance()
    
    manager.start_server()
    time.sleep(50)  # Simulate some running time
    manager.stop_server()
    time.sleep(50)
    manager.restart_server()