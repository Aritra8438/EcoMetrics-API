"""Production server using Waitress WSGI server"""

import sys
import os
from waitress import serve

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.index import app  # pylint: disable=wrong-import-position

if __name__ == "__main__":
    print("Starting Waitress server on port 10000...")
    serve(app, host="0.0.0.0", port=10000, threads=4)
