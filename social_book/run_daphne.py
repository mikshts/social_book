# run_daphne.py

import os
from daphne.cli import CommandLineInterface

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_book.settings")

CommandLineInterface().run([
    "-b", "0.0.0.0",
    "-p", os.environ.get("PORT", "8000"),  # ✅ use Render's assigned port
    "--",
    "social_book.asgi:application"
])
