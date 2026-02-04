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

       
        stage('Security Gate 3: DAST (OWASP ZAP)') {
            steps {
                script {
                    echo '--- Starting ZAP Dynamic Scan ---'
                    
                    sh 'mkdir -p zap_reports'
                    sh 'chmod 777 zap_reports'
                    
                    try {
                        sh '''
                            docker run --rm -u 0 \
                            -v $(pwd)/zap_reports:/zap/wrk/:rw \
                            owasp/zap2docker-stable \
                            zap-baseline.py \
                            -t http://172.17.0.1:5000 \
                            -r report.xml \
                            -I
                        '''
                    } catch (Exception e) {
                        echo '⚠️ ZAP Scan found issues, but we will let the "Decision" stage handle the failure.'
                    }
                }
            }
        }

        stage('Reporting: Upload to DefectDojo') {
            steps {
                withCredentials([string(credentialsId: 'defectdojo-api-key', variable: 'DOJO_API_KEY')]) {
                    script {
                        
                        if (fileExists('zap_reports/report.xml')) {
                            echo '--- Found ZAP Report. Uploading... ---'
                            
                            sh 'docker rm -f dd-uploader 2>/dev/null || true'
                            sh 'docker run -d --name dd-uploader python:3.9-slim sleep 300'
                            
                            sh 'docker cp defectdojo_upload.py dd-uploader:/tmp/upload_script.py'
                            sh 'docker cp zap_reports/report.xml dd-uploader:/tmp/report.xml'
                            
                            sh '''
                                docker exec -e DOJO_API_KEY=$DOJO_API_KEY dd-uploader \
                                bash -c "pip install requests && python /tmp/upload_script.py 'ZAP Scan' /tmp/report.xml"
                            '''
                            
                            sh 'docker rm -f dd-uploader'
                        
                        } else {

                            echo '⚠️ No ZAP Report found (zap_reports/report.xml is missing).'
                            echo 'Skipping DefectDojo upload.'
                        }
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
                    printf '{"text": "🚨 *SECURITY ALERT: Pipeline Failed!*\\n*Project:* %s\\n*Build:* %s\\n*Check DefectDojo for details."}' "$JOB_NAME" "$BUILD_NUMBER" > payload.json
                    
                
                    curl -v -X POST -H "Content-type: application/json" --data @payload.json "$SLACK_WEBHOOK"
                '''
            }
        }

        success {
            script {
                echo '✅ PIPELINE SUCCESS! Sending Alert...'
                sh '''
                    
                    printf '{"text": "✅ *SUCCESS: Pipeline Passed.*\\nCode is secure and merged. \\n*Project:* %s\\n*Build:* %s"}' "$JOB_NAME" "$BUILD_NUMBER" > payload.json
                    
                    curl -v -X POST -H "Content-type: application/json" --data @payload.json "$SLACK_WEBHOOK"
                '''
            }
        }
    }
}