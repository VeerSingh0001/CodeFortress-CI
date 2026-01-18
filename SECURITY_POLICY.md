Security Gate Policy (v1.0)

Secret Management: No high-entropy strings (AWS keys, API tokens, private keys) are permitted in the codebase. Any commit containing a verified secret will be rejected.

Vulnerability Threshold: The application must have Zero (0) vulnerabilities of "Critical" or "High" severity.

Enforcement:

Local: Pre-commit hooks via TruffleHog.

Remote: CI Pipeline failure via SonarQube Quality Gate.
