# Set working directory to stocking/
cd ~/stocking/

# Run stocking query service
python3 src/main.py query run/config/query_all_1d.json

# Commit and push changes to origin
git add data/stock_data/
git commit -m "Update stock data"
git push

