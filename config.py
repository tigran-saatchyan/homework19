"""Flask app Config module"""
from dataclasses import dataclass

from helpers.constants import SQLITE_DB_NAME


@dataclass
class Config:
    """
    Flask app configuration settings
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = SQLITE_DB_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = False
