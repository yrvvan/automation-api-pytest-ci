import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()  # This loads the .env file

# Function to build parameters from the report
def param_builder():
    try:
        # Load the JSON report
        with open('./report.json', 'r') as file:
            report_data = json.load(file)

        # Extract data from the report
        stats = report_data['summary']

        # Prepare the information dictionary
        information = {
            'test_duration': round(report_data['duration'] / 60, 2),  # Convert duration to minutes
            'test_success_rate': round((stats['passed'] / stats['collected']) * 100, 2),
            'test_passed': stats['passed'],
            'test_failed': stats.get('failed', 0),
            'total_test_cases': stats['collected']
        }

        return information

    except Exception as error:
        print(f"Failed to process the report - Error: {error}")
        raise  # Re-raise the exception for handling elsewhere

# Function to send notification to Mattermost
def push_notification_mattermost():
    try:
        # Get test result parameters
        payload = param_builder()

        # Prepare the message for Mattermost
        message = f"<!channel>\n*Test Case Success Rate* 📢\n- Platform Name: PyTest\n- Environment: {os.getenv('ENV').upper()}\n- Success Rate: {payload['test_success_rate']}%\n- Passed Test Cases: {payload['test_passed']}\n- Failed Test Cases: {payload['test_failed']}\n- Total Test Cases: {payload['total_test_cases']}\n- Duration: {payload['test_duration']} min\n"
        
        # Payload for the Mattermost message
        notif_payload = {
            'icon_url': 'https://ideku.io/assets/images/png/logo-ideku-black.webp',
            'text': message
        }

        # Webhook URL from environment variables
        webhook_mattermost = os.getenv('MATTERMOST_WEBHOOK')

        # Send the notification via HTTP POST request
        response = requests.post(webhook_mattermost, json=notif_payload, headers={'Content-Type': 'application/json'})

        # Check if the response is successful
        if response.status_code == 200:
            print(f"Successfully pushed to Mattermost: {response.text}")
        else:
            print(f"Failed to push to Mattermost. Status code: {response.status_code}")

    except Exception as error:
        print(f"Error in pushing notification: {error}")

# Call the function to push notification to Mattermost
if __name__ == "__main__":
    push_notification_mattermost()
