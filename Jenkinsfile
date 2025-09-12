pipeline { 
    agent any
    
    environment {
        DOCKER_IMAGE = "library-management-system"
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage("Code Clone") {
            steps {
                echo "Code Clone Stage"
                git url: "https://github.com/rakshitmalik136/library-management-system-.git", branch: "master"
		sh "ls -la"   // <-- add this
        	sh "cat .env || echo '.env missing!'"
            }
        }
        
        stage("Code Build & Test") {
            steps {
                echo "Code Build Stage"
                script {
                    // Build with both versioned and latest tags
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }
        
        stage("Basic Tests") {
            steps {
                echo "Running Basic Tests"
                script {
                    // Test if the container runs without errors
                    sh "docker run --rm ${DOCKER_IMAGE}:latest python -c 'import flask; print(\"Flask import successful\")'"
                }
            }
        }
        
        stage("Push To DockerHub") {
            steps {
                echo "Pushing to DockerHub"
                withCredentials([usernamePassword(
                    credentialsId:"dockerHubCreds",
                    usernameVariable:"dockerHubUser",
                    passwordVariable:"dockerHubPass")]) {
                    
                    script {
                        sh 'echo $dockerHubPass | docker login -u $dockerHubUser --password-stdin'
                        
                        // Push both versioned and latest tags
                        sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${env.dockerHubUser}/${DOCKER_IMAGE}:${DOCKER_TAG}"
                        sh "docker tag ${DOCKER_IMAGE}:latest ${env.dockerHubUser}/${DOCKER_IMAGE}:latest"
                        
                        sh "docker push ${env.dockerHubUser}/${DOCKER_IMAGE}:${DOCKER_TAG}"
                        sh "docker push ${env.dockerHubUser}/${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }
        
        stage("Deploy") {
            steps {
                echo "Deploying Application"
                script {
                    sh '''
                        docker compose --env-file .env down || echo "No running containers to stop"
    			docker compose --env-file .env up -d --build

                        echo "Waiting for app to start..."
                        sleep 15

                        docker exec lms ls -la /app/templates/ || (echo "Deployment failed"; exit 1)
                    '''
                }
            }
        }
        
        stage("Cleanup") {
            steps {
                echo "Cleaning up unused Docker resources"
                script {
                    sh '''
                        docker image prune -f
                        docker logout || echo "Already logged out"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo "Pipeline execution completed"
            // Clean up workspace
            cleanWs()
        }
        
        success {
            echo "Pipeline completed successfully!"
            echo "Application should be running at http://localhost:5000"
        }
        
        failure {
            echo "Pipeline failed!"
            sh 'docker compose logs || echo "Could not fetch logs"'
        }
        
        cleanup {
            // Additional cleanup if needed
            sh 'docker logout || echo "Already logged out"'
        }
    }
}

