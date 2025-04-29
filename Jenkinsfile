pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')           // DockerHub creds ID in Jenkins
        IMAGE_NAME = 'prasanna0307/survey-flask-app'
        DEPLOYMENT_NAME = 'hw4deployed'
        CONTAINER_NAME = 'container-0'
        NAMESPACE = 'default'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $IMAGE_NAME:latest .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                echo 'Logging in to DockerHub...'
                script {
                    sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                echo 'Pushing Docker image to DockerHub...'
                sh 'docker push $IMAGE_NAME:latest'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying updated image to Kubernetes...'
                script {
                    sh '''
                        kubectl set image deployment/$DEPLOYMENT_NAME $CONTAINER_NAME=$IMAGE_NAME:latest -n $NAMESPACE
                        kubectl rollout status deployment/$DEPLOYMENT_NAME -n $NAMESPACE
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Logging out from DockerHub...'
            sh 'docker logout'
        }
    }
}
