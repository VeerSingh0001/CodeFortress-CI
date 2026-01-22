### Week 2: SAST Integration (Completed)
* **Objective:** Automated vulnerability detection.
* **Tool:** SonarQube Community (Dockerized).
* **Workflow:**
  * Developer pushes to `dev`.
  * Jenkins triggers SonarScanner.
  * **Quality Gate** blocks the pipeline if vulnerabilities (SQLi, XSS) are found.
  * If Pass -> Auto-merge to `main`.
* **Proof:**

<img width="1865" height="906" alt="Screenshot_20260122_144439" src="https://github.com/user-attachments/assets/971e8ff5-1dbe-4e9f-a139-b027e0e83703" />
<img width="1876" height="850" alt="Screenshot_20260122_144344" src="https://github.com/user-attachments/assets/d434469e-3aee-4c7c-a79f-ad92abe21a16" />
