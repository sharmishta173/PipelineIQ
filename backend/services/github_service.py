import requests

from app.config import GITHUB_TOKEN


def build_comment(result):

    return f"""
### 🤖 PipelineIQ Analysis

Category:
{result['category']}

Root Cause:
{result['root_cause']}

Suggested Fix:
{result['fix']}

Confidence:
{result['confidence']}
"""


def post_commit_comment(
        owner,
        repo,
        commit_sha,
        comment_text):

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}"
        f"/commits/{commit_sha}/comments"
    )

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.post(
        url,
        headers=headers,
        json={
            "body": comment_text
        }
    )

    return {
        "status_code": response.status_code,
        "response": response.json()
    }