docker-compose -f src/docker-compose.yml up -d
./gatherData.sh
./processData.sh