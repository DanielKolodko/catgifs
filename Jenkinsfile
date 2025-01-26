pipeline {
    agent any

    environment {
        // Docker image name and tag
        DOCKER_IMAGE = 'danielkolodko/catgifs'
        DOCKER_TAG = 'latest'

        // Docker Hub credentials stored in Jenkins
        DOCKER_CREDENTIALS = 'docker'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository
                git branch: 'main', credentialsId: 'github', url: 'https://github.com/DanielKolodko/catgifs.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Navigate to the app directory
                    dir(FLASK_APP_DIR) {
                        // Build the Docker image for the Flask app
                        bat 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
                    }
                }
            }
        }

        stage('Test Docker Image') {
            steps {
                script {
                    // Run the Docker container to test the image
                    bat 'docker run --rm -d --name test-container -p 5000:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}'

                    // Optional: You can add health checks or additional tests here
                    bat 'curl -f http://localhost:5000 || exit 1'

                    // Stop the container after testing
                    bat 'docker stop test-container'
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    // Push the Docker image to Docker Hub
                    withDockerRegistry([credentialsId: DOCKER_CREDENTIALS, url: 'https://index.docker.io/v1/']) {
                        bat 'docker push ${DOCKER_IMAGE}:${DOCKER_TAG}'
                    }
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                script {
                    // Deploy the Docker container to production (locally or on a server)
                    bat '''
                    docker stop prod-container || true
                    docker rm prod-container || true
                    docker run -d --name prod-container -p 5000:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                    '''
                }
            }
        }
    }

    post {
        always {
            // Clean up unused Docker resources after every pipeline run
            bat 'docker system prune -f || true'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
    }
}
