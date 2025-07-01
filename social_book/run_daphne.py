# run_daphne.py

import os
from daphne.cli import CommandLineInterface

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_book.settings")

CommandLineInterface().run([
    "-b", "0.0.0.0",
    "-p", "8000",
    "--",  # <- important: separates options from the application path
    "social_book.asgi:application"
])
