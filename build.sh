set -o errexit

pip install -r requirments.txt

python manage.py makemigrations --noinput
python manage.py migrate --noinput

python manage.py collectstatic --no-input