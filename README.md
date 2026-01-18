# CodeFortress CI: Secure DevSecOps Pipeline


## 🛡️ Project Overview
This project implements a "Shift Left" security strategy. It integrates automated security gates into the CI/CD pipeline to detect secrets and vulnerabilities before deployment.

## 🚀 Key Features
* **Secret Scanning (Week 1):** Pre-commit hooks and Jenkins pipeline integration using **TruffleHog**.
* **SAST Integration (Week 2):** Planned integration with **SonarQube**.
* **DAST Integration (Week 3):** Planned integration with **OWASP ZAP**.

## 📂 Structure
* `src/`: Source code of the target Python application.
* `Jenkinsfile`: The CI/CD pipeline definition.
* `.pre-commit-config.yaml`: Local security gate configuration.
