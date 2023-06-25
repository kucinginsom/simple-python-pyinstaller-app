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
                script {
                    sh 'python -m py_compile sources/add2vals.py sources/calc.py'
                    stash includes: 'sources/*.py*', name: 'compiled-results'
                }
            }
        }
    }
}
