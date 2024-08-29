"""
Script: Create Duo Admin(s) and Send Activation Link

Description:
This Python script allows you to create new Duo Admins by entering their details manually. 
After creating each admin, the script sends an activation email to the new admin. The process 
repeats in a loop, asking the user if they want to create another admin. The API credentials 
(Integration Key, Secret Key, and API Hostname) are securely pulled from a configuration file 
stored on the user's computer.

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

2. **Running the Script:**
   - Update the `config_file` variable in the script to point to the path where the `duo_config.json` file is stored.
   - Execute the script using Python. It will prompt you to enter the details for each admin you want to create, 
     including email, name, role, and optionally, phone number. After each admin is created, an activation email 
     will be sent automatically. The script will continue to prompt you until you choose to stop.

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
import json
import duo_client
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
        'password': dummy_password  # Dummy password for deprecated field
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
            # Assemble the activation link endpoint
            endpoint = f'/admin/v1/admins/{admin_id}/activation_link/email'
            response = admin_api.json_api_call('POST', endpoint, {})
            print(f"[+] Activation email sent successfully for admin_id: {admin_id}")
        except Exception as e:
            print(f"[-] Error sending activation email for admin_id {admin_id}: {e}")

def main():
    while True:
        admin_email = get_next_arg('Enter admin email: ')
        admin_name = get_next_arg('Enter admin name: ')
        admin_role = get_next_arg('Enter admin role: ')
        admin_phone = input('Enter admin phone (optional, press Enter to skip): ') or None
        
        # Call the create admin function
        new_admin_id = create_admin(
            email=admin_email,
            name=admin_name,
            role=admin_role,
            phone=admin_phone
        )
        
        # If admin was successfully created, send activation email
        if new_admin_id:
            send_activation_email(new_admin_id)

        # Ask the user if they want to create another admin
        create_another = input('Do you want to create another admin? (yes/no): ').strip().lower()
        if create_another != 'yes':
            break

if __name__ == "__main__":
    main()
