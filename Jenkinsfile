#!groovy
pipeline {
    agent any
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
                sh 'docker login -u $CREDENTIALS_CREDENTIALS_USR -p $CREDENTIALS_CREDENTIALS_PSW $registry'
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