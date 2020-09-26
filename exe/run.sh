# Set working directory to stocking root
cd ~/stocking/

# Run stocking's query service
python3 src/main.py exe/release/query_config.json

# Save a backup of data in a separate location
cp data/* ~/backup/

# Notify Josh with results
/usr/sbin/sendmail joshtg.007@gmail.com < out/email.txt
