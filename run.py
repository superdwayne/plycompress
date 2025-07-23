import subprocess
import sys
import time
from multiprocessing import Process

def run_streamlit():
    """Run Streamlit app"""
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"])

def run_fastapi():
    """Run FastAPI app"""
    subprocess.run([sys.executable, "api.py"])

if __name__ == "__main__":
    print("Starting PLY Compress services...")
    print("Streamlit UI will be available at: http://localhost:8501")
    print("FastAPI will be available at: http://localhost:8000")
    print("API docs will be available at: http://localhost:8000/docs")
    
    # Start both processes
    streamlit_process = Process(target=run_streamlit)
    fastapi_process = Process(target=run_fastapi)
    
    streamlit_process.start()
    time.sleep(2)  # Give Streamlit time to start
    fastapi_process.start()
    
    try:
        # Wait for both processes
        streamlit_process.join()
        fastapi_process.join()
    except KeyboardInterrupt:
        print("\nShutting down services...")
        streamlit_process.terminate()
        fastapi_process.terminate()
        streamlit_process.join()
        fastapi_process.join()