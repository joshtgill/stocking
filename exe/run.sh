# Set working directory to stocking root
cd ~/stocking/

# Pull latest changes
git pull

# Run stocking's query service
python3 src/main.py exe/config/query_config.json

# Notify Josh with results
/usr/sbin/sendmail joshtg.007@gmail.com < out/email.txt
