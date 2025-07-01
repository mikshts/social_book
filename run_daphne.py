import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_book.settings')

import django
django.setup()  # <-- initialize Django apps registry

try:
    from twisted.internet import epollreactor
    epollreactor.install()
    print("Using epollreactor")
except ImportError:
    print("epollreactor not available, using default reactor")

from daphne.cli import CommandLineInterface

if __name__ == "__main__":
    # Default interface and port
    interface = "127.0.0.1"
    port = 8000
    
    # Parse command line args to override interface and port
    # Example usage: python run_daphne.py 0.0.0.0 8000 social_book.asgi:application
    if len(sys.argv) >= 3:
        interface = sys.argv[1]
        port = int(sys.argv[2])
        # Remove these from args before passing to Daphne CLI
        if len(sys.argv) < 4:
            sys.argv.append('social_book.asgi:application')  # default fallback
        else:
            sys.argv = [sys.argv[0]] + sys.argv[3:]


    print(f"Starting Daphne on {interface}:{port} ...")
    
    # Build Daphne CLI args with interface and port
    sys.argv.extend(['-b', interface, '-p', str(port)])

    sys.exit(CommandLineInterface.entrypoint())  # Start Daphne with the provided args
