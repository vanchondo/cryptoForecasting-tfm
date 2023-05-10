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
                withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'CREDENTIALS_USERNAME', passwordVariable: 'CREDENTIALS_PASSWORD')]) {
                    sh 'echo $CREDENTIALS_PASSWORD |  docker login -u ${CREDENTIALS_USERNAME} --password-stdin ${registry}'  
                }
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