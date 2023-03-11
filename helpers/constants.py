"""Constants module"""
import os
from pathlib import Path

# jwt secret and algorithm
JWT_SECRET = '$CekpeTHo$'
JWT_ALGORITHM = 'HS256'

# hashing parameters
CRYPTOGRAPHIC_HASH_FUNCTION = 'sha256'
PWD_HASH_SALT = b'top_secret_salt_and_pepper'
PWD_HASH_ITERATIONS = 100_000

# logging folders
THIS_FOLDER = Path(__file__).parent.resolve()
LOG_DIR = os.path.join(THIS_FOLDER, "../logs")

# SQLite db engine and location
SQLITE_DB_NAME = 'sqlite:///movies.db'
