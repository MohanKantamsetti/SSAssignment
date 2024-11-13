#!/bin/bash
set -e

# Wait for a few seconds to ensure that MongoDB has started
sleep 10

# Import JSON files into MongoDB
for file in /import-files/*.json; do
  collection=$(basename "$file" .json)
  mongoimport --db $MONGO_INITDB_DATABASE --collection $collection --file "$file" --jsonArray
done
