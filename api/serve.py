"""Production server using Waitress WSGI server"""

import sys
import os

# Add parent directory to path to handle imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from waitress import serve
from api.database import app
import api.index  # Import to register routes

if __name__ == "__main__":
    print("Starting Waitress server on port 10000...")
    serve(app, host="0.0.0.0", port=10000, threads=4)
