"""
Script: Export Duo Users to CSV

Description:
This Python script retrieves a list of users and associated phone details from Duo Security's Admin API
and exports the information to a CSV file. The API credentials (Integration Key, Secret Key, and API Hostname)
are securely pulled from a configuration file specified by the user.

Functions:
- `load_duo_config(file_path)`: Reads the Duo API credentials from a specified JSON configuration file.
- `get_next_arg(prompt)`: A helper function to get the next argument from the command line or prompt the user 
  if no arguments are provided (used in case the script needs to be run interactively).

Usage:
1. **Configuration File Setup:**
   - Create a JSON file (e.g., `duo_config.json`) on your computer containing the Duo API credentials:
     ```json
     {
         "ikey": "your-integration-key",
         "skey": "your-secret-key",
         "host": "your-api-hostname"
     }
     ```
   - Ensure that this file is securely stored and accessible only by authorized users.

2. **Running the Script:**
   - When prompted, provide the full path to your `duo_config.json` file.
   - The script will automatically read the API credentials from the JSON file and 
     retrieve the user data from Duo.

3. **CSV Output:**
   - The script prints a CSV report to the standard output, including the following fields:
     - `Username`: The Duo username.
     - `Phone Number`: The associated phone number.
     - `Type`: The type of the phone (e.g., mobile, landline).
     - `Platform`: The platform of the phone (e.g., iOS, Android).

Notes:
- **Security Considerations:** Ensure that the `duo_config.json` file is stored in a secure location and 
  has appropriate access controls to prevent unauthorized access to the API credentials.
- **Customization:** You can modify the script to change the CSV output fields or the data source by 
  adjusting the logic in the main script body.

Author: Chad Ramey
Date: August 29, 2024
"""

#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import csv
import sys
import json

import duo_client
from six.moves import input

# Function to read the Duo configuration from a JSON file
def load_duo_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    # Prompt for the configuration file location
    config_file = input('Enter the full path to your Duo configuration file (e.g., duo_config.json): ')
    
    # Load the Duo configuration from the file
    config = load_duo_config(config_file)

    # Set up the Duo Admin API client
    admin_api = duo_client.Admin(
        ikey=config['ikey'],
        skey=config['skey'],
        host=config['host'],
    )

    # Retrieve user info from API:
    users = admin_api.get_users()

    # Print CSV of username, phone number, phone type, and phone platform:
    #
    # (If a user has multiple phones, there will be one line printed per
    # associated phone.)
    reporter = csv.writer(sys.stdout)
    print("[+] Report of all users and associated phones:")
    reporter.writerow(('Username', 'Phone Number', 'Type', 'Platform'))
    for user in users:
        for phone in user["phones"]:
            reporter.writerow([
                user["username"],
                phone["number"],
                phone["type"],
                phone["platform"],
            ])

if __name__ == "__main__":
    main()
