pipeline {
    agent any

    environment {
        TRUFFLEHOG_VERSION = '3.63.0'
        // Use the ID you created in Jenkins Credentials
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
                // This downloads the code from 'dev' (as per your job config)
                checkout scm
                
                // Configure Git so it can merge
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

        stage('Auto-Merge to Main') {
           
            steps {
                echo '--- Security Checks Passed. Merging to MAIN... ---'
                script {
                    sh '''
                        # 1. Setup Remote URL with Credentials
                        git remote set-url origin https://${GIT_CREDS_USR}:${GIT_CREDS_PSW}@github.com/VeerSingh0001/CodeFortress-CI.git
                        
                        # 2. Fetch all branches (Jenkins usually only fetches one)
                        git fetch --all
                        
                        # 3. Checkout Main and Merge Dev
                        # We force checkout main, then merge the remote dev branch
                        git checkout main
                        git merge origin/dev
                        
                        # 4. Push the result
                        git push origin main
                    '''
                }
            }
        }
    }
}