### Week 2: SAST Integration (Completed)
* **Objective:** Automated vulnerability detection.
* **Tool:** SonarQube Community (Dockerized).
* **Workflow:**
  * Developer pushes to `dev`.
  * Jenkins triggers SonarScanner.
  * **Quality Gate** blocks the pipeline if vulnerabilities (SQLi, XSS) are found.
  * If Pass -> Auto-merge to `main`.
* **Proof:**

