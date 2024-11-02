#!/bin/zsh

cd /Users/minho/code/python/return-and-earn || exit

echo "return-and-earn: auto_json_update.sh"

source .venv/bin/activate

echo "running python script"
echo "----------"
python find_locations.py
echo "----------"

echo "committing changes..."
git add return_points.json
git commit -m "$(date '+%Y-%m-%d:%H:%M:%S-auto-json-update')"
git push

echo "done"
