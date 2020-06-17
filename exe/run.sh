# Set working directory to stocking root
cd ~/stocking/

# Run stocking's query service
python3 src/main.py exe/config.json

# Notify Josh with results
/usr/sbin/sendmail joshtg.007@gmail.com < out/email.txt

# Remove log file in email
rm *.log
