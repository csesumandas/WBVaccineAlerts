# WBVaccineAlerts
This code repository has code to send Covid 19 Vaccine availibility alerts to Telegram Channels for West Bengal, India.
Currently there are four files.
1. cowinv3.py - This is the main script written in python. This script repeatedly checks vaccine status from the govt provided API.
2. config.json - This is the configuration file which has configuration data in JSON format like District ID, Telegram BOT Token and time interval for checking the API for new vaccine status.
3. runallv3.sh - This is a bash script for running the cowinv3.py script for a set of districts and save the output from the script in text file for each district.
4. killall.sh - This is a bash script to stop all instances of running scripts of cowinv3.py

## Deployment
1. Install Python3 in the server.
2. Install below python libraries in the server.
- cloudscraper
- requests
- smtplib, ssl
3. Create Telegram BOT API key. [Guide](https://core.telegram.org/bots)
4. Replace the TELEKEY value from "TELEGRAM_BOT_API_KEY" to your created TELEGRAM BOT API KEY.
5. Change the channel addresses in the script cowinv3.py.
6. Change the configuration in runallv3.sh if required.
7. Run the runallv3.sh in the server.
8. To stop all the processes run killall.sh.
