#!groovy
pipeline {
    agent any
    environment {
        CREDENTIALS = credentials('docker-registry-credentials')
        DOCKER_USERNAME = credentials('docker-registry-credentials-username')
        DOCKER_PASSWORD = credentials('docker-registry-credentials-password')
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
                withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD} ${registry}'
                    sh 'docker push $registry/$app_name'
                }
            }
        }
    }
    post {
        always {
            sh 'docker logout'
        }
    }
}