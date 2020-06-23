# Set working directory to stocking root
cd ~/stocking/

# Run stocking's query service
python3 src/main.py exe/query_config.json

# Notify Josh with results
/usr/sbin/sendmail joshtg.007@gmail.com < out/email.txt

# Remove log file (already in email)
rm *.log
