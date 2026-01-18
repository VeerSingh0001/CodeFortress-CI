pipeline {
    agent any

    environment {
        TRUFFLEHOG_VERSION = '3.63.0'
    }

    stages {
        // Stage 1: Clean Workspace (Prevents "ghost" files from previous runs)
        stage('Clean Workspace') {
            steps {
                echo '--- 0. Cleaning Workspace ---'
                deleteDir()
            }
        }

        // Stage 2: Pull Code
        stage('Checkout Source') {
            steps {
                echo '--- 1. Cloning Repository ---'
                // This automatically pulls the code from the repo where this Jenkinsfile lives
                checkout scm
            }
        }

        // Stage 3: Security Gate (Week 1 Requirement)
        stage('Security Gate: Secret Scan') {
            steps {
                echo '--- 2. Running TruffleHog Security Gate ---'
                script {
                    // 1. Download TruffleHog to /tmp (Safe location)
                    sh "curl -L -o /tmp/trufflehog.tar.gz https://github.com/trufflesecurity/trufflehog/releases/download/v${TRUFFLEHOG_VERSION}/trufflehog_${TRUFFLEHOG_VERSION}_linux_amd64.tar.gz"
                    
                    // 2. Extract to /tmp
                    sh "tar -xzf /tmp/trufflehog.tar.gz -C /tmp"
                    
                    // 3. Run Scan
                    // We scan '.' (current folder). The tool ignores itself because it's in /tmp
                    sh '/tmp/trufflehog filesystem . --fail --no-update --exclude-paths .trufflehog-ignore'
                }
            }
        }

        // Stage 4: Build (Only runs if Security Gate passes)
        stage('Build Artifact') {
            steps {
                echo '--- 3. Secrets Verified. Proceeding to Build. ---'
                // Simulating a build process
                sh 'echo "Building Secure App v1.0..."'
            }
        }
    }
}
