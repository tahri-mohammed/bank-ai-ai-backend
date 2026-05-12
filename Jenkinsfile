pipeline {
    agent any

    stages {
        stage('Install') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Check') {
            steps {
                sh 'python3 -m compileall app'
            }
        }
    }
}
