"""
Script: Bulk Create Duo Admins from CSV

Description:
This Python script reads a CSV file containing details of new Duo Admin users and automatically creates these 
admins in Duo Security using the Admin API. After creating the admins, the script sends an activation email 
to each newly created admin. The API credentials (Integration Key, Secret Key, and API Hostname) are securely 
pulled from a configuration file stored on the user's computer.

Functions:
- `load_duo_config(file_path)`: Reads the Duo API credentials from a specified JSON configuration file.
- `create_admin(email, name, role, phone='')`: Creates a new Duo Admin using the provided details and returns the admin ID.
- `send_activation_email(admin_id)`: Sends an activation email to the newly created admin.

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

2. **CSV File Format:**
   - Prepare a CSV file with the following columns:
     - `Email`: The email address of the new admin.
     - `Name`: The full name of the new admin.
     - `Role`: The role assigned to the new admin (e.g., `Owner`, `Administrator`).
     - `Phone` (Optional): The phone number of the new admin.

3. **Running the Script:**
   - Update the `config_file` variable in the script to point to the path where the `duo_config.json` file is stored.
   - Execute the script using Python. It will automatically read the API credentials from the JSON file, 
     process the CSV file, create the admins, and send the activation emails.

Notes:
- **Security Considerations:** Ensure that the `duo_config.json` file is stored in a secure location and 
  has appropriate access controls to prevent unauthorized access to the API credentials.
- **Customization:** You can modify the script to add additional fields or logic as required by your specific use case.

Author: Chad Ramey
Date: August 29, 2024
"""

#!/usr/bin/env python
from __future__ import absolute_import, print_function
import sys
import csv
import duo_client
import json
from six.moves import input

# Function to read the Duo configuration from a JSON file
def load_duo_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Load the Duo configuration from a file
config_file = "path_to_your_file/duo_config.json"
config = load_duo_config(config_file)

# Configuration and information about objects to create.
admin_api = duo_client.Admin(
    ikey=config['ikey'],
    skey=config['skey'],
    host=config['host'],
)

def create_admin(email, name, role, phone=''):
    # We will pass a dummy password since the API still requires it but it's deprecated
    dummy_password = 'dummy_password'
    admin_details = {
        'email': email,
        'name': name,
        'role': role,
        'phone': phone,
        'password': dummy_password
    }

    try:
        response = admin_api.add_admin(**admin_details)
        admin_id = response['admin_id']
        print(f"[+] Successfully created admin: {name} with role: {role}")
        return admin_id
    except Exception as e:
        print(f"[-] Error creating admin {name}: {e}")
        return None

def send_activation_email(admin_id):
    if admin_id:
        try:
            endpoint = f'/admin/v1/admins/{admin_id}/activation_link/email'
            response = admin_api.json_api_call('POST', endpoint, {})
            print(f"[+] Activation email sent successfully for admin_id: {admin_id}")
        except Exception as e:
            print(f"[-] Error sending activation email for admin_id {admin_id}: {e}")

def main():
    # Prompt for the CSV file location
    csv_file_path = input('Enter the full path to the CSV file: ')

    # Open the CSV file
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row['Email']
            name = row['Name']
            role = row['Role']
            phone = row.get('Phone', None)  # Phone is optional
            
            new_admin_id = create_admin(
                email=email,
                name=name,
                role=role,
                phone=phone
            )
            
            # If admin was successfully created, send activation email
            if new_admin_id:
                send_activation_email(new_admin_id)

if __name__ == "__main__":
    main()
