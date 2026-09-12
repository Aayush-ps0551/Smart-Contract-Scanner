import os
import subprocess
import sys

def main():
    print("🚀 Starting Web3 Smart Contract Vulnerability Scanner...")
    
    # Check if virtual environment exists
    venv_dir = "venv"
    if os.name == 'nt':  # Windows
        streamlit_path = os.path.join(venv_dir, "Scripts", "streamlit.exe")
    else:  # Mac/Linux
        streamlit_path = os.path.join(venv_dir, "bin", "streamlit")

    # If venv streamlit doesn't exist, try using global streamlit
    if not os.path.exists(streamlit_path):
        print("Virtual environment not found, trying global streamlit...")
        streamlit_path = "streamlit"

    try:
        # Run the Streamlit app
        subprocess.run([streamlit_path, "run", "app.py"])
    except KeyboardInterrupt:
        print("\nScanner stopped.")
    except Exception as e:
        print(f"Error starting the app: {e}")

if __name__ == "__main__":
    main()
