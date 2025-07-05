import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_book.settings')

import django
django.setup()
from daphne.cli import CommandLineInterface
# ✅ Run migrations BEFORE starting Daphne
from django.core.management import call_command
print("🔄 Running migrations...")
call_command('migrate', interactive=False)
print("✅ Migrations complete.")

# ✅ Start Daphne

if __name__ == "__main__":
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
