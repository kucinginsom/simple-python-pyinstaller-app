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

    /* on Deploy Stage, we run ssh agent to connect to AWS EC2 instance
    and after that running shell script that pull new code and restart server
    after that sleep 1 minute before stage deploy finish
    */
    stage('Deploy') {
        sshagent(['ssh-agent-pythonapp']) {
            sh 'ssh -t ubuntu@13.250.37.157 -o StrictHostKeyChecking=no sh /home/ubuntu/python_app.sh'
        }
        sleep(time: 1, unit: 'MINUTES')
    }    
}