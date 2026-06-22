def analyze_log(log_text):

    log_text = log_text.lower()

    # Missing dependency
    if "modulenotfounderror" in log_text:

        return {
            "category": "Dependency Error",
            "root_cause": "Missing Python dependency",
            "fix": "Install the missing package and update requirements.txt",
            "confidence": "95%"
        }

    # Failed tests
    elif "assertionerror" in log_text:

        return {
            "category": "Test Failure",
            "root_cause": "Unit test failure",
            "fix": "Review test assertions and application logic",
            "confidence": "90%"
        }

    # Database issues
    elif "operationalerror" in log_text:

        return {
            "category": "Database Error",
            "root_cause": "Database connection failure",
            "fix": "Verify database credentials and server availability",
            "confidence": "92%"
        }

    # Docker issues
    elif "failed to solve" in log_text:

        return {
            "category": "Docker Error",
            "root_cause": "Docker build failure",
            "fix": "Check Dockerfile and dependency installation steps",
            "confidence": "88%"
        }

    # Permission issues
    elif "permission denied" in log_text:

        return {
            "category": "Permission Error",
            "root_cause": "Permission issue",
            "fix": "Verify file permissions and access controls",
            "confidence": "94%"
        }

    # GitHub Actions failures
    elif "process completed with exit code" in log_text:

        return {
            "category": "CI/CD Failure",
            "root_cause": "GitHub Actions workflow step failed",
            "fix": "Inspect the failed workflow step and logs",
            "confidence": "85%"
        }

    return {
        "category": "Unknown Error",
        "root_cause": "Unknown failure",
        "fix": "Manual investigation required",
        "confidence": "50%"
    }