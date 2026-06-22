import requests
from app.config import (
    AZURE_ORG,
    AZURE_PROJECT,
    AZURE_PAT
)

def trigger_pipeline():

    url = (
        f"https://dev.azure.com/"
        f"{AZURE_ORG}/"
        f"{AZURE_PROJECT}"
        f"/_apis/pipelines/1/runs"
        f"?api-version=7.1-preview.1"
    )

    response = requests.post(
        url,
        auth=("", AZURE_PAT)
    )

    return response.json()