#!/social_book/bash.sh
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

echo "Using database: $DATABASE_URL"

