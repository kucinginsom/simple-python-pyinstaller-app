pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'python:2-alpine'
                }
            }
            steps {
                sh 'python -m py_compile sources/add2vals.py sources/calc.py'
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'qnib/pytest'
                }
            }
            steps {
                sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage('Manual Approval') {
            steps {
                input message: 'Lanjutkan ke tahap Deploy?'
            }            
        }        
        stage('Deploy') {
            env.VOLUME = "${pwd()}/sources:/src"
            env.IMAGE = 'cdrx/pyinstaller-linux:python2'
            dir(env.BUILD_ID) {
                unstash(name: 'compiled-results')
                sh "docker run --rm -v ${env.VOLUME} ${env.IMAGE} 'pyinstaller -F add2vals.py'"
            }
            archiveArtifacts "sources/dist/add2vals"
            sh "docker run --rm -v ${env.VOLUME} ${env.IMAGE} 'rm -rf build dist'"
        }
    }
}
