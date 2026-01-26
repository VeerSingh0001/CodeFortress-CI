pipeline {
    agent any

    environment {
        // Defines the tool we setup in Phase 3
        scannerHome = tool 'sonar-scanner'
        GIT_CREDS = credentials('github-write-token')
        TRUFFLEHOG_VERSION = '3.63.0'
        HOST_IP = '172.17.0.1'
    }

    stages {
        stage('Clean Workspace') {
            steps { deleteDir() }
        }

        stage('Checkout Source') {
            steps {
                checkout scm
                sh 'git config user.email "jenkins@codefortress.local"'
                sh 'git config user.name "Jenkins CI"'
            }
        }

        stage('Security Gate 1: Secrets') {
            steps {
                script {
                    sh "curl -L -o /tmp/trufflehog.tar.gz https://github.com/trufflesecurity/trufflehog/releases/download/v${TRUFFLEHOG_VERSION}/trufflehog_${TRUFFLEHOG_VERSION}_linux_amd64.tar.gz"
                    sh "tar -xzf /tmp/trufflehog.tar.gz -C /tmp"
                    sh '/tmp/trufflehog filesystem . --fail --no-update --exclude-paths .trufflehog-ignore'
                }
            }
        }

        stage('Security Gate 2: SonarQube SAST') {
            steps {
                echo '--- Running Static Analysis ---'
                // Connects to the server
                withSonarQubeEnv('sonarqube-server') {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
            }
        }
        
        // This pauses the pipeline until SonarQube finishes processing
        stage("Quality Gate") {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

       
        stage('Security Gate 3: OWASP ZAP (DAST)') {
            steps {
                script {
                    echo '--- 1. Building & Starting Staging Environment ---'
                    // Clean up potential leftovers
                    sh 'docker rm -f ci-test-app 2>/dev/null || true' 
                    
                    // Containerize the Target App
                    sh 'docker build -t ci-target-app .'
                    
                    // Deploy to Staging (Port 5000)
                    sh 'docker run -d --name ci-test-app -p 5000:5000 ci-target-app'
                    
                    // Create a directory for the attack report
                    sh 'mkdir -p zap_reports'
                    sh 'chmod 777 zap_reports'
                    
                    // Wait for the app to initialize
                    sh 'sleep 10'
                    
                    echo '--- 2. Running ZAP Active Scan (Spider + Attack) ---'
                    
                    sh "docker run --rm -v \$(pwd)/zap_reports:/zap/wrk/:rw ghcr.io/zaproxy/zaproxy:stable zap-full-scan.py -t http://${HOST_IP}:5000 -r report.html -I || true"
                    
                    echo '--- 3. Teardown Staging ---'
                    sh 'docker rm -f ci-test-app'
                }
            }
        }

        stage('Auto-Merge to Main') {
            steps {
                script {
                    sh '''
                        git remote set-url origin https://${GIT_CREDS_USR}:${GIT_CREDS_PSW}@github.com/VeerSingh0001/CodeFortress-CI.git
                        git fetch --all
                        git checkout main
                        git merge origin/dev
                        git push origin main
                    '''
                }
            }
        }
    }
}