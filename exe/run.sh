# Set working directory to stocking root
cd ~/stocking/

# Run stocking's query service
python3 src/main.py exe/release/query_config.json

# Save a backup of data in a separate location
cp data/* ~/backup/stocking/
