# Set working directory to stocking root
cd ~/stocking/

# Run stocking's query service
python3 src/main.py query run/config/query_all_1d.json

# Commit and push updated stock data to origin
git add data/stock_data/
git commit -m "Update stock data"
git push