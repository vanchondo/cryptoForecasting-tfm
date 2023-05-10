#!groovy
pipeline {
    agent any
    environment {
        CREDENTIALS = credentials('docker-registry-credentials')
        app_name = 'cryptoforecasting-tfm'
        version = "0.${BUILD_NUMBER}"
    }
    stages {       
        stage('Docker Build') {
            steps {
                sh 'docker image build -t $app_name:${version} .'
                sh 'docker image tag $app_name ${REGISTRY_URL}/$app_name'
            }
        }
        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'CREDENTIALS_USERNAME', passwordVariable: 'CREDENTIALS_PASSWORD')]) {
                    sh 'echo $CREDENTIALS_PASSWORD |  docker login -u ${CREDENTIALS_USERNAME} --password-stdin ${REGISTRY_URL}'  
                    sh 'docker push ${REGISTRY_URL}/$app_name'
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