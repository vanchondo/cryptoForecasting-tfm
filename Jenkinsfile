#!groovy
pipeline {
    agent none
    environment {
        CREDENTIALS = credentials('docker-registry-credentials')
        app_name = 'cryptoforecasting-tfm'
        registry = 'registry.victoranchondo.com'
    }
    stages {
        stage('Docker Build') {
            agent any
            steps {
                sh 'docker image build -t $app_name:latest .'
            }
        }
        stage('Docker Tag') {
            agent any
            steps {
                sh 'docker image tag $app_name $registry/$app_name'
            }
        }
        stage('Docker Login') {
            agent any
            steps {
                sh 'echo $CREDENTIALS_CREDENTIALS_PSW | docker login -u $CREDENTIALS_CREDENTIALS_USR --password-stdin'
            }
        }
        stage('Docker Push') {
            agent any
            steps {
                sh 'docker push $registry/$app_name'
            }
        }
    }
}