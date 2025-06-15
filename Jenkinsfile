pipeline {
    agent any

    environment {
        REPO_URL = "https://github.com/SadiaImran/NoteApplication.git"
        PROJECT_DIR = "/var/lib/jenkins/NoteApplication"
        TEST_DIR = "NoteAppTests"
    }

    stages {
        stage('Clean workspace') {
            steps {
                sh '''
                echo "🧹 Cleaning old workspace at $PROJECT_DIR ..."
                rm -rf $PROJECT_DIR
                mkdir -p $PROJECT_DIR
                '''
            }
        }

        stage('Clone Repository') {
            steps {
                sh '''
                echo "📥 Cloning GitHub repository..."
                git clone $REPO_URL $PROJECT_DIR
                '''
            }
        }

        stage('Build and Run Tests') {
            steps {
                dir("${PROJECT_DIR}/${TEST_DIR}") {
                    sh '''
                    echo "🐳 Building Docker image for tests..."
                    docker build -t noteapp-tests .
                    
                    echo "🧪 Running test container..."
                    docker run --rm noteapp-tests > test_output.txt || true
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                def authorEmail = sh(
                    script: "cd $PROJECT_DIR && git log -1 --pretty=format:'%ae'",
                    returnStdout: true
                ).trim()

                emailext (
                    to: authorEmail,
                    subject: "📣 Jenkins Test Results - ${currentBuild.currentResult}",
                    body: """
Hi ${authorEmail},

Your recent GitHub push triggered a Jenkins CI pipeline.

🔧 *Build Status:* ${currentBuild.currentResult}  
🔍 *Job:* ${env.JOB_NAME}  
🔁 *Build Number:* #${env.BUILD_NUMBER}  
📜 *Console Output:* ${env.BUILD_URL}

Thanks,  
🤖 Jenkins Automation System
""",
                    attachmentsPattern: "${PROJECT_DIR}/${TEST_DIR}/test_output.txt"
                )
            }
        }
    }
}
