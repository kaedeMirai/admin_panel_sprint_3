#! /bin/bash -x

set -e

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

python3.11 main.py