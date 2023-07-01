pipeline {
    agent none
    options {
        skipStagesAfterUnstable()
    }
    stages {
        // Build python app
        stage('Build') {
            agent {
                docker {
                    image 'python:2-alpine'
                }
            }
            steps {
                sh 'python -m py_compile sources/add2vals.py sources/calc.py'
                stash(name: 'compiled-results', includes: 'sources/*.py*')
            }
        }
        // Running test case for python app
        stage('Test') {
            agent {
                docker {
                    image 'qnib/pytest'
                }
            }
            steps {
                sh 'py.test --junit-xml test-reports/results.xml sources/test_calc.py'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        // Wait for user input before going to Deploy Stage
        stage('Manual Approval') {
            steps {
                input message: 'Lanjutkan ke tahap Deploy?'
            }            
        }          
        /* on Deploy Stage, we run ssh agent to connect to AWS EC2 instance
        and after that running shell script that pull new code and restart server
        after that sleep 1 minute before stage deploy finish
        */     
        stage('Deploy') { 
            agent any
            environment { 
                VOLUME = '$(pwd)/sources:/src'
                IMAGE = 'cdrx/pyinstaller-linux:python2'
            }
            steps {
                dir(path: env.BUILD_ID) { 
                    unstash(name: 'compiled-results') 
                    sh "docker run --rm -v ${VOLUME} ${IMAGE} 'pyinstaller -F add2vals.py'" 
                }
            }
            post {
                success {
                    archiveArtifacts "${env.BUILD_ID}/sources/dist/add2vals" 
                    sh "docker run --rm -v ${VOLUME} ${IMAGE} 'rm -rf build dist'"
                    sshagent(['ssh-agent-pythonapp']) {
                        sh 'ssh -t ubuntu@13.250.37.157 -o StrictHostKeyChecking=no sh /home/ubuntu/python_app.sh'
                    }                    
                    sleep(time: 1, unit: 'MINUTES')                                    
                }
            }
        }
    }
}

