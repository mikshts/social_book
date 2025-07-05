import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_book.settings')

import django
django.setup()

try:
    from twisted.internet import epollreactor
    epollreactor.install()
    print("✅ Using epollreactor")
except ImportError:
    print("⚠️ epollreactor not available, using default reactor")

from daphne.cli import CommandLineInterface

if __name__ == "__main__":
    # Render requires binding to 0.0.0.0 and using the PORT env var
    interface = "0.0.0.0"
    port = int(os.environ.get("PORT", "10000"))

    print(f"🚀 Starting Daphne on {interface}:{port} ...")

    sys.argv = [
        sys.argv[0],
        "social_book.asgi:application",
        "-b", interface,
        "-p", str(port)
    ]

    sys.exit(CommandLineInterface.entrypoint())
