web: gunicorn headliner:app --log-file -
worker:  python src/data/main.py -i src/resources/rsstraining -p True -l 3
