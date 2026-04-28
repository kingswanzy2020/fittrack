pipeline {
    agent any

    environment {
        // Docker Hub image path - replace with your username
        DOCKER_IMAGE = 'ahmed3015/fittrack'
        // Use the Jenkins build number as the image tag
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        // Must match the credential ID you created in Jenkins
        DOCKER_CREDENTIALS = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull the latest code from the repository
                checkout scm
            }
        }

        stage('Build') {
            steps {
                script {
                    // Build the Docker image from the Dockerfile
                    dockerImage = docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}")
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    // Authenticate with Docker Hub and push the image
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_CREDENTIALS) {
                        dockerImage.push("${IMAGE_TAG}")
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                // Update the Kubernetes deployment with the new image tag
                sh """
                    kubectl set image deployment/fittrack \
                        fittrack=${DOCKER_IMAGE}:${IMAGE_TAG} \
                        -n fittrack
                    kubectl rollout status deployment/fittrack \
                        -n fittrack \
                        --timeout=120s
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully. FitTrack v${IMAGE_TAG} deployed."
        }
        failure {
            echo "Pipeline failed. Check logs for details."
        }
    }
}
