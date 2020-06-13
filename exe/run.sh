# Set working directory to stocking root
cd ~/stocking/

# Run stocking's query service
python3 src/main.py exe/config.json

# Zip stock data files for easy transfer
rm -f data/stock_data.zip
zip data/stock_data.zip data/*
