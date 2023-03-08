"""Constants module"""
import os
from pathlib import Path

SECRET = '$CekpeTHo$'
ALGORITHM = 'HS256'
THIS_FOLDER = Path(__file__).parent.resolve()
LOG_DIR = os.path.join(THIS_FOLDER, "../logs")
SQLITE_DB_NAME = 'sqlite:///movies.db'
