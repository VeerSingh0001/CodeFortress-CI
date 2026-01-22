pipeline {
    agent any

    environment {
        TRUFFLEHOG_VERSION = '3.63.0'
        // Access the credentials we just made
        GIT_CREDS = credentials('github-write-token') 
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Checkout Source') {
            steps {
                // Checkout the branch that triggered the build
                checkout scm
                
                // Configure Git Identity for the merge later
                sh 'git config user.email "jenkins@codefortress.local"'
                sh 'git config user.name "Jenkins CI"'
            }
        }

        stage('Security Gate: Secret Scan') {
            steps {
                script {
                    sh "curl -L -o /tmp/trufflehog.tar.gz https://github.com/trufflesecurity/trufflehog/releases/download/v${TRUFFLEHOG_VERSION}/trufflehog_${TRUFFLEHOG_VERSION}_linux_amd64.tar.gz"
                    sh "tar -xzf /tmp/trufflehog.tar.gz -C /tmp"
                    sh '/tmp/trufflehog filesystem . --fail --no-update --exclude-paths .trufflehog-ignore'
                }
            }
        }

        // TODO: Week 2 - Add SonarQube Stage Here
        
        stage('Auto-Merge to Main') {
            // ONLY run this stage if we are on the 'dev' branch
            when {
                branch 'dev'
            }
            steps {
                echo '--- Security Checks Passed on DEV. Merging to MAIN... ---'
                script {
                    sh '''
                        # 1. Authenticate using the token
                        git remote set-url origin https://${GIT_CREDS_USR}:${GIT_CREDS_PSW}@github.com/VeerSingh0001/CodeFortress-CI.git
                        
                        # 2. Fetch latest main
                        git fetch origin main:main
                        
                        # 3. Checkout Main
                        git checkout main
                        
                        # 4. Merge Dev into Main
                        git merge dev
                        
                        # 5. Push changes
                        git push origin main
                    '''
                }
            }
        }
    }
}