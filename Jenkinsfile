pipeline {
    agent any

    environment {
        // Defines the tool we setup in Phase 3
        scannerHome = tool 'sonar-scanner'
        GIT_CREDS = credentials('github-write-token')
        TRUFFLEHOG_VERSION = '3.63.0'
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