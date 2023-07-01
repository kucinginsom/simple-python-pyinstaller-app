node {
    options {
        skipStagesAfterUnstable()
    }

    // Build and compile python app
    stage('Build') {
        docker.image('python:2-alpine').inside {
            sh 'python -m py_compile sources/add2vals.py sources/calc.py'
            stash(name: 'compiled-results', includes: 'sources/*.py*')
        }
    }

    // Running test cases for python app
    stage('Test') {
        docker.image('qnib/pytest').inside {
            sh 'py.test --junit-xml test-reports/results.xml sources/test_calc.py'
        }
        post {
            always {
                junit 'test-reports/results.xml'
            }
        }
    }

    // Wait for user input for approval before going to the Deploy Stage
    stage('Manual Approval') {
        steps {
            input message: 'Lanjutkan ke tahap Deploy?'
        }
    }

    // Deploy Stage - use pyinstaller image and sleep 1 minute before finishing
    stage('Deploy') {
        environment {
            VOLUME = '$(pwd)/sources:/src'
            IMAGE = 'cdrx/pyinstaller-linux:python2'
        }
        dir(path: env.BUILD_ID) {
            unstash(name: 'compiled-results')
            sh "docker run --rm -v ${VOLUME} ${IMAGE} 'pyinstaller -F add2vals.py'"
        }
        post {
            success {
                archiveArtifacts "${env.BUILD_ID}/sources/dist/add2vals"
                sh "docker run --rm -v ${VOLUME} ${IMAGE} 'rm -rf build dist'"
                sleep(time: 1, unit: 'MINUTES')
            }
        }
    }
}