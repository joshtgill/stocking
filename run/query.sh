# Set working directory to stocking/
cd ~/stocking/

# Run stocking with query flag
python3 src/main.py config/main_config.json 0

# Commit and push changes to origin
git add data/stock_data/
git commit -m "Update stock data"
git push

