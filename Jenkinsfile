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
                // Secret file credential: Jenkins copies the kubeconfig to a temp path in KUBECONFIG
                withCredentials([file(credentialsId: 'kubeconfig-credentials-id', variable: 'KUBECONFIG')]) {
                    sh """
                        set -e
                        if ! command -v kubectl >/dev/null 2>&1; then
                            ARCH=\$(uname -m)
                            case "\$ARCH" in
                                x86_64) KUBE_ARCH=amd64 ;;
                                aarch64|arm64) KUBE_ARCH=arm64 ;;
                                *) echo "Unsupported architecture: \$ARCH"; exit 1 ;;
                            esac
                            KUBECTL_VER=\$(curl -fsL https://dl.k8s.io/release/stable.txt)
                            curl -fsLO "https://dl.k8s.io/release/\${KUBECTL_VER}/bin/linux/\${KUBE_ARCH}/kubectl"
                            chmod +x kubectl
                            export PATH="\${WORKSPACE}:\${PATH}"
                        fi
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