# Validation Report: Security Gate Enforcement (Secret Scanning)

**Date:** January 18, 2026
**Test Case:** SC-01 (Hardcoded Credential Detection)
**Status:** ✅ PASSED (Build Failed as Expected)

## 1. Objective
To verify that the "Security Gate" policy automatically blocks commits containing high-entropy secrets (e.g., AWS Keys, Database Passwords) to prevent sensitive data leakage.

## 2. Methodology
* **Tool:** TruffleHog (v3.x) via Pre-Commit Hook & Jenkins Pipeline.
* **Scenario:** Attempted to commit a Python file (`db_config.py`) containing a hardcoded database connection string with a visible password. 
```bash
# Production Database Configuration
# TODO: Move this to environment variables later
DB_CONNECTION_STRING = "postgres://admin:SuperSecretPassword123!@production-db.aws.com:5432/customers"
```

## 3. Execution Evidence
Below is the raw log output demonstrating the interception and blocking of the commit:    

**1st Example**
```text
git commit -m "TEST: Intentionally breaking gate with DB Password"
TruffleHog (Docker)......................................................Failed
- hook id: trufflehog-docker
- exit code: 183

🐷🔑🐷  TruffleHog. Unearth your secrets. 🐷🔑🐷

2026-01-18T09:44:14Z    info-0  trufflehog      running source  {"source_manager_worker_id": "szATL", "with_units": true}
Found unverified result 🐷🔑❓
Verification issue: lookup production-db.aws.com on 10.179.77.31:53: no such host
Detector Type: Postgres
Decoder Type: PLAIN
Raw result: postgres://admin:SuperSecretPassword123!@production-db.aws.com:5432
Sslmode: <unset>
File: src/db_config.py
Line: 3

2026-01-18T09:44:16Z    info-0  trufflehog      finished scanning       {"chunks": 11, "bytes": 21972, "verified_secrets": 0, "unverified_secrets": 1, "scan_duration": "1.279321741s", "trufflehog_version": "3.92.5", "verification_caching": {"Hits":0,"Misses":1,"HitsWasted":0,"AttemptsSaved":0,"VerificationTimeSpentMS":1274}}
```
**2nd Exapmle**
```text
git commit -m "Checking for API key"
TruffleHog (Docker)......................................................Failed
- hook id: trufflehog-docker
- exit code: 183

🐷🔑🐷  TruffleHog. Unearth your secrets. 🐷🔑🐷

2026-01-20T09:10:37Z    info-0  trufflehog      running source  {"source_manager_worker_id": "8uc7r", "with_units": true}
Found unverified result 🐷🔑❓
Detector Type: PrivateKey
Decoder Type: PLAIN
Raw result: -----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDH135AcYfkIAZa
HGkPAk6VWRzMEI/awlawxJVeYlZ7C/+q+emckjIdrFKZ2BsGT0raUOelHPdweFKL
BZVhAW4j7TfLU8X+4+Guvmt+rh+f/izYfWCHBYHB7Trckd/165C/HH6SE+AyAhKq
vYVDtnx0aWQrb+HXRM0XUFrQNTc9frPHBhDA2GPJbGs1jZTpn7fPHVR+WeYaah6+
KHW9g/RUsWZrSlxYvFX8eySugYa+hl46Mt5QJsazjx1MggRCu0vIYSD+Nj5k0wF3
FQ8+xRimp2whbNqFQ0y/SqgWsOmu7mJhDliX+6TyLe8GwaqVxfLhPa1FMmxRT5U7
im08YFerAgMBAAECggEAWDgeCM7VgXRNuYvfKPwIus9a8g7Bon22DVTK556btLgI
Rm8KnM7BBu5ijH2k+HUagyPCDtapuOG09qAhYHBkMcHvpne16R6qKxzukT7GwTdQ
jsVSTmi07moOWP6gkoxKGsO2cEAL8aeOnAcMBGdTq4Q27yH13bUGoKsdW9qSJze2
mZV+/TrtY3kj0OSdK4HwdVdCzCGo1jHtta2SNwrouvjAACThswP1aBhfgY6QlQDS
P+PEN0k5O+cZWMidyzwatu86hcc7rG9XQk6ojd39tB0+iZXHtTnmFmY0roFcIsUe
JX4uF/rI2Js39KryQUoc9YjsvnNeaoraG0ztXNzLYQKBgQDvak+hj+kMdWAXUhJH
CZeB57MQRKiaWE/bC8TB86rnoDunyq10kVOl1UhXWD12wYdSII500SPoi1V9ZliL
ZgKpQyNj1BbMA/SYqtmcwUZdkI8JaSJoJiClVkFbSafqve2DkhNINkafOolfgP3r
7c3NeVgFOsoN8kIlMivTqeHYuwKBgQDVr2b+ujRhr8AzRbBcLqtBgsp1du4RlGbF
R6DNmDJwyv5Autmk0ntLBYN8zl4qKpb55qyGfh9Y0x/xkrOzUU/Suj651l9kVGaj
CuqtlevbJN01gT2Yj/KsgSVyYjbIKszrtFWms3Ft2oGBlkAhecRutgpbrG8jly+W
cDeLg3xF0QKBgELWcxSvkGgh/ImGKAQc8WcawCqygD9WmDSWvH9I/1VarkzRkEsS
pz+Mo31+7OnSbWzIGf0SxeuNungfsmh4OhX24FJmS1b5Y7ebOtVAP9yvFr+R0kEx
I7wEsIpDrdUi4MPya9+lB2I8fU1kPX84DFRoo+IR34a1MzIfJ40XyC0xAoGASb/3
ATWM/KYm5MtJmhc1Xi/g5ne8pO6eJbqaAjtkNU+qPvb+RQesK/FkN0AWeeEnKGr3
4pdHBGYhoUOrp9kJfsZu/b7CP6NtpRoQcwbKV2E6w8uuUahk7irInNjO5Xj4LuWX
pihKnsqKZgpQaf1X0YocuxUhapw0fWyPjyQ7UPECgYBr1R/VcQCOGWu7vE5sVcQR
FAI4AO6beCVWAggI0T1EPh+EsdCoOxQPu9zQiV+S8+zWuUwscKvoHJ8vhP0kPpLF
lbvZUjO4YBn5fZBLHExsdx/APXuuwPXlugVC1nUblCyjJ3vMkjFR1p5Kvf6/vIPt
HpRaoHsdBoo5vb0hf9WcZg==
-----END PRIVATE KEY-----
File: forced_secret.txt
Line: 1

2026-01-20T09:10:39Z    info-0  trufflehog      finished scanning       {"chunks": 10, "bytes": 24933, "verified_secrets": 0, "unverified_secrets": 1, "scan_duration": "2.186646706s", "trufflehog_version": "3.92.5", "verification_caching": {"Hits":0,"Misses":1,"HitsWasted":0,"AttemptsSaved":0,"VerificationTimeSpentMS":2182}}
```
