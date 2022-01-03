docker-compose -f src/docker-compose.yml up -d
python3 test/clearDB.py
python3 test/sampleDB.py
./gatherData.sh
./processData.sh