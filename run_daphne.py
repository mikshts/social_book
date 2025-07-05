import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_book.settings')

import django
django.setup()  # Initialize Django apps registry

try:
    from twisted.internet import epollreactor
    epollreactor.install()
    print("✅ Using epollreactor")
except ImportError:
    print("⚠️ epollreactor not available, using default reactor")

from daphne.cli import CommandLineInterface

if __name__ == "__main__":
    # Get host and port from environment, fallback to 0.0.0.0:10000 (Render's default)
    interface = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "10000"))

    # Optionally allow override via CLI arguments (e.g., for local dev)
    if len(sys.argv) >= 3:
        interface = sys.argv[1]
        port = int(sys.argv[2])
        if len(sys.argv) < 4:
            sys.argv.append("social_book.asgi:application")
        else:
            sys.argv = [sys.argv[0]] + sys.argv[3:]
    else:
        sys.argv = [sys.argv[0], "social_book.asgi:application"]

    print(f"🚀 Starting Daphne on {interface}:{port} ...")

    # Append Daphne CLI args
    sys.argv.extend(["-b", interface, "-p", str(port)])

    sys.exit(CommandLineInterface.entrypoint())
