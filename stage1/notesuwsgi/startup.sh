#service nginx start
/flask/bin/uwsgi --http :5000 --wsgi-file runserver.py --callable app --master --processes 4 --threads 2
#/flask/bin/python3 /notes/runserver.py
