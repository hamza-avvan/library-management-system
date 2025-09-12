pipeline{ 
    agent any
    
    environment {
        DOCKER_IMAGE = "library-management-system"
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages{
        stage("Code Clone"){
            steps{
                echo "Code Clone Stage"
                git url: "https://github.com/rakshitmalik136/library-management-system-.git", branch: "master"
            }
        }
        
        stage("Code Build & Test"){
            steps{
                echo "Code Build Stage"
                script {
                    // Build with both versioned and latest tags
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }
        
        stage("Basic Tests"){
            steps{
                echo "Running Basic Tests"
                script {
                    // Test if the container runs without errors
                    sh "docker run --rm ${DOCKER_IMAGE}:latest python -c 'import flask; print(\"Flask import successful\")'"
                }
            }
        }
        
        stage("Push To DockerHub"){
            steps{
                echo "Pushing to DockerHub"
                withCredentials([usernamePassword(
                    credentialsId:"dockerHubCreds",
                    usernameVariable:"dockerHubUser",
                    passwordVariable:"dockerHubPass")]){
                    
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
        
        stage("Deploy"){
            steps{
                echo "Deploying Application"
                script {
                    // Ensure .env file exists
                    sh '''
                        if [ ! -f .env ]; then
                            echo "Warning: .env file not found. Creating a basic one..."
                            cp .env.example .env || echo "Please ensure .env file is configured properly"
                        fi
                    '''
                    
                    // Deploy with better error handling
                    sh '''
                        docker compose down || echo "No running containers to stop"
                        docker compose up -d --build
                    '''
                    
                    // Verify deployment
                    sh '''
                        sleep 10
                        if docker compose ps | grep -q "Up"; then
                            echo "Deployment successful!"
                        else
                            echo "Deployment may have issues. Check logs:"
                            docker compose logs
                            exit 1
                        fi
                    '''
                }
            }
        }
        
        stage("Cleanup"){
            steps{
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
