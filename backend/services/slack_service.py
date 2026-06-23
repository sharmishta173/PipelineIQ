import requests


def send_slack_alert(message, webhook_url):

    response = requests.post(
        webhook_url,
        json={
            "text": message
        }
    )
    return response.status_code
