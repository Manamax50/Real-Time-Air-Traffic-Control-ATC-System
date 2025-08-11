# start_system.py
import subprocess
import sys
import time

def start_system():
    # Start ATC logic
    atc_process = subprocess.Popen([sys.executable, "atc_logic.py"])
    
    # Start API server
    api_process = subprocess.Popen([sys.executable, "atc_api.py"])
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down system...")
        atc_process.terminate()
        api_process.terminate()
        atc_process.wait()
        api_process.wait()

if __name__ == '__main__':
    start_system()