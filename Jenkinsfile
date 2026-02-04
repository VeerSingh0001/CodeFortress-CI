pipeline {
    agent any

    environment {
        // Defines the tool
        scannerHome = tool 'sonar-scanner'
        GIT_CREDS = credentials('github-write-token')
        TRUFFLEHOG_VERSION = '3.63.0'
        HOST_IP = '172.17.0.1'
        SLACK_WEBHOOK = credentials('slack-webhook-url')
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
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    script {
                        echo '--- 1. Building & Starting Staging Environment ---'
                        sh 'docker rm -f ci-test-app 2>/dev/null || true' 
                        sh 'docker build -t ci-target-app .'
                        sh 'docker run -d --name ci-test-app -p 5000:5000 ci-target-app'
                        sh 'sleep 10'
                        
                        echo '--- 2. Running ZAP Active Scan ---'
                        sh 'docker rm -f zap-scanner 2>/dev/null || true'
                        sh 'docker volume rm zap-vol 2>/dev/null || true'
                        sh 'docker volume create zap-vol'
                        
                        sh "docker run --user 0 --name zap-scanner -v zap-vol:/zap/wrk ghcr.io/zaproxy/zaproxy:stable zap-full-scan.py -t http://${HOST_IP}:5000 -r report.html -J report.json -x report.xml -I || true"
                        
                        echo '--- 3. Extracting Reports ---'
                        sh 'mkdir -p zap_reports'
                        sh 'docker cp zap-scanner:/zap/wrk/report.html ./zap_reports/report.html'
                        sh 'docker cp zap-scanner:/zap/wrk/report.json ./zap_reports/report.json'
                        sh 'docker cp zap-scanner:/zap/wrk/report.xml ./zap_reports/report.xml'
                        
                        sh 'docker rm -f zap-scanner'
                        sh 'docker volume rm zap-vol'
                        sh 'docker rm -f ci-test-app'

                        echo '--- 4. Enforcing Security Gate Policy ---'
                        if (readFile('zap_reports/report.json').trim().isEmpty()) {
                            error("❌ ZAP Report is missing or empty!")
                        }

                        def exitCode = sh(script: 'grep -qE \'"risk(desc)?":\\s*"(High|Medium|Critical)\' ./zap_reports/report.json', returnStatus: true)
                        
                        if (exitCode == 0) {
                            echo "🚨 SECURITY GATE FAILED: Vulnerabilities detected!"
                            error("Blocking Build due to Critical/High Vulnerabilities") 
                        } else {
                            echo "✅ SECURITY GATE PASSED"
                        }
                    }
                }
            }
        }

        stage('Reporting: Upload to DefectDojo') {
            steps {
                withCredentials([string(credentialsId: 'defectdojo-api-key', variable: 'DOJO_API_KEY')]) {
                    script {
                        echo '--- Uploading Reports to DefectDojo ---'
                        
                        sh 'docker rm -f dd-uploader 2>/dev/null || true'
                        sh 'docker run -d --name dd-uploader python:3.9-slim sleep 300'
                        
                        sh 'docker cp defectdojo_upload.py dd-uploader:/tmp/upload_script.py'
                        sh 'docker cp zap_reports/report.xml dd-uploader:/tmp/report.xml'
                        
                        sh '''
                            docker exec -e DOJO_API_KEY=$DOJO_API_KEY dd-uploader \
                            bash -c "pip install requests && python /tmp/upload_script.py 'ZAP Scan' /tmp/report.xml"
                        '''
                        
                        sh 'docker rm -f dd-uploader'
                    }
                }
            }
        }

        stage('Final Security Decision') {
            steps {
                script {
                    if (currentBuild.result == 'FAILURE') {
                        echo "🛑 BLOCKING MERGE: Security Gates Failed."
                        error("Pipeline stopped due to security vulnerabilities. Check DefectDojo for details.")
                    } else {
                        echo "✅ QUALITY GATES PASSED: Proceeding to Merge."
                    }
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


    post {
        failure {
            script {
                echo '🚨 PIPELINE FAILED! Sending Alert...'
                sh '''
                    cat <<EOF > payload.json
                    {
                        "text": "🚨 *SECURITY ALERT: Pipeline Failed!*\\n*Project:* ${JOB_NAME}\\n*Build:* ${BUILD_NUMBER}\\n*Check DefectDojo for details.*"
                    }
                    EOF
                    curl -X POST -H "Content-type: application/json" --data @payload.json "$SLACK_WEBHOOK"
                '''
            }
        }

        success {
            script {
                echo '✅ PIPELINE SUCCESS! Sending Alert...'
                sh '''
                    cat <<EOF > payload.json
                    {
                        "text": "✅ *SUCCESS: Pipeline Passed.*\\nCode is secure and ready for merge.\\n*Project:* ${JOB_NAME}\\n*Build:* ${BUILD_NUMBER}"
                    }
                    EOF
                    curl -X POST -H "Content-type: application/json" --data @payload.json "$SLACK_WEBHOOK"
                '''
            }
        }
    }
}

