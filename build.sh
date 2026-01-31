#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- Installing Dependencies ---"
pip install -r requirements.txt

echo "--- Creating Media Folders ---"
mkdir -p media/documents/applications
mkdir -p media/locker
mkdir -p media/profiles
mkdir -p media/announcements/images
mkdir -p media/announcements/docs

echo "--- Collecting Static Files ---"
python manage.py collectstatic --no-input

echo "--- Running Migrations ---"
python manage.py migrate --no-input

echo "--- Seeding Database ---"
python manage.py setup_test_data

echo "--- Build Finished Successfully ---"
