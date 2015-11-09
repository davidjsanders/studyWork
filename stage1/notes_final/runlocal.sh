uwsgi --http :5000 --wsgi-file runserver.py --callable app --master --processes 4 --threads 2 --socket 127.0.0.1:3031
