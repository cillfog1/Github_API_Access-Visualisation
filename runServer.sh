docker-compose -f src/docker-compose.yml up -d
python3 test/clearDB.py
python3 -m http.server &
python3 src/app.py