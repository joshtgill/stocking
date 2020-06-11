# Set working directory to stocking root
cd ~/stocking/

# Run stocking's query service
python3 src/main.py exe/config.json

# Commit updated database files
git add data/
git commit -m "Update stock databases"
git push
