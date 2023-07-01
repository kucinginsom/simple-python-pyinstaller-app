node {
    // Build python app
    stage('Build') {
        docker.image('python:2-alpine').inside {
            sh 'python -m py_compile sources/add2vals.py sources/calc.py'
            stash includes: 'sources/*.py*', name: 'compiled-results'
        }
    }

    // Running test case for python app
    stage('Test') {
        docker.image('qnib/pytest').inside {
            sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
        }
    }
    // Wait for user input before going to Deploy Stage
    stage('Manual Approval') {
        input message: 'Lanjutkan ke tahap Deploy?'
    }    

    // on Deploy Stage, add pythion installer image, after that sleep 1 minute before stage deploy finish
    stage('Deploy') {
        environment {
            APP_NAME = 'pythonapp'
            VIRTUAL_ENV = 'venv'
        }
        steps {
            script {
                //run sh scripted file on aws, sleep 1minute

            }
        }
    }    


}