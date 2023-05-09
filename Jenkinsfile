#!groovy
pipeline {
    agent {
        docker { image 'python:bullseye' }
    }
    environment {
        CREDENTIALS = credentials('docker-registry-credentials')
        app_name = 'cryptoforecasting-tfm'
        registry = 'registry.victoranchondo.com'
    }
    stages {
        stage('Docker Build') {
            steps {
                sh 'docker image build -t $app_name:latest .'
            }
        }
        stage('Docker Tag') {
            steps {
                sh 'docker image tag $app_name $registry/$app_name'
            }
        }
        stage('Docker Login') {
            steps {
                sh 'echo $CREDENTIALS_CREDENTIALS_PSW | docker login -u $CREDENTIALS_CREDENTIALS_USR --password-stdin'
            }
        }
        stage('Docker Push') {
            steps {
                sh 'docker push $registry/$app_name'
            }
        }
    }
    post {
        always {
            sh 'docker logout'
        }
    }
}