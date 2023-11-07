"""Config for this service."""
import os

from dotenv import find_dotenv, load_dotenv

# this will load all the envars from a .env file
load_dotenv(find_dotenv())


def get_config():
    return Config()


class Config(object):
    """Base config init."""

    SA_KEY = os.getenv('SA_KEY', '100')
