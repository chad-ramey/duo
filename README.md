# Duo Lab

This repository contains Python scripts designed to automate administrative tasks for Duo Security, including creating admins and generating reports.

## Table of Contents
  - [Scripts Overview](#scripts-overview)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Scripts Overview
Here’s a list of all the scripts in this repository along with their descriptions:

1. **[duo_bulk_create_admins.py](duo_bulk_create_admins.py)**: Automates the bulk creation of Duo admins using a list of admin data, useful for onboarding new admins at scale.
2. **[duo_create_admin.py](duo_create_admin.py)**: Creates a single Duo admin, allowing for individual admin onboarding.
3. **[duo_report_users_and_phones.py](duo_report_users_and_phones.py)**: Generates a report of all Duo users and their associated phone numbers for security and audit purposes.

## Requirements
- **Python 3.x**: Ensure that Python 3 is installed on your system.
- **Duo SDK**: Install the [Duo Python SDK](https://duo.com/docs/administration-api) to interact with the Duo Admin API.
- **API Keys**: You will need Duo API credentials (Integration Key, Secret Key, API Hostname) to authenticate API requests.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo-name/duo-automation-scripts.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Duo API credentials and other necessary environment variables:
   ```bash
   export DUO_INTEGRATION_KEY="your-integration-key"
   export DUO_SECRET_KEY="your-secret-key"
   export DUO_API_HOSTNAME="your-api-hostname"
   ```

## Usage
Run the desired script from the command line or integrate it into your existing automation workflows.

Example:
```bash
python3 duo_create_admin.py --email "admin@example.com" --role "Owner"
```

## Contributing
Feel free to submit issues or pull requests to improve the functionality or add new features.

## License
This project is licensed under the MIT License.
