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
