import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False
    return True

def run_streamlit_app():
    """Run the Streamlit application"""
    try:
        os.chdir("src")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except Exception as e:
        print(f"Error running Streamlit app: {e}")

if __name__ == "__main__":
    print("Starting Dumroo AI Admin Panel...")
    
    if install_requirements():
        print("Launching web application...")
        run_streamlit_app()
    else:
        print("Failed to install requirements. Please install manually.")