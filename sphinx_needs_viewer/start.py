import os
import sys

from streamlit.web import cli as stcli

if __name__ == "__main__":
    print(f"Running from {os.getcwd()}")
    sys.argv = ["streamlit", "run", "Welcome.py"]
    sys.exit(stcli.main())
