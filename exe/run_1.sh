# Set working directory to stocking root
cd ~/stocking/

# Run stocking's display service
python3 src/main.py exe/config/display_config_1.json

# Move output to a separate location
mv out/output.txt ../output_1.txt
