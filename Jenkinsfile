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
                sh 'python -m py_compile sources/random_number_generator.py sources/random.py'
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
        // Wait for user input for approval before going to Deploy Stage
        stage('Manual Approval') {
            steps {
                input message: 'Lanjutkan ke tahap Deploy?'
            }
        }        
        // on Deploy Stage, add pythion installer image, after that sleep 1 minute before stage deploy finish
        stage('Deploy') { 
            agent any
            environment { 
                VOLUME = '$(pwd)/sources:/src'
                IMAGE = 'cdrx/pyinstaller-linux:python2'
            }
            steps {
                dir(path: env.BUILD_ID) { 
                    unstash(name: 'compiled-results') 
                    sh "docker run --rm -v ${VOLUME} ${IMAGE} 'pyinstaller -F random_number_generator.py'" 
                }
            }
            post {
                success {
                    archiveArtifacts "${env.BUILD_ID}/sources/dist/random_number_generator" 
                    sh "docker run --rm -v ${VOLUME} ${IMAGE} 'rm -rf build dist'"
                    sleep(time: 1, unit: 'MINUTES')
                }
            }
        }
    }
}

