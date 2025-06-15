pipeline {
    agent any

    environment {
        MAIN_REPO = "https://github.com/SadiaImran/NoteApplication.git"
        TEST_REPO = "https://github.com/SadiaImran/NoteApplication-Tests.git"
        MAIN_DIR  = "/var/lib/jenkins/NoteApplication"
        TEST_DIR  = "/var/lib/jenkins/NoteApplication-Tests"
    }

    stages {
        stage('Clean workspace') {
            steps {
                sh '''
                echo "🧹 Cleaning workspace..."
                rm -rf $MAIN_DIR $TEST_DIR
                mkdir -p $MAIN_DIR $TEST_DIR
                '''
            }
        }

        stage('Clone Application and Tests') {
            steps {
                sh '''
                echo "📥 Cloning main app..."
                git clone $MAIN_REPO $MAIN_DIR

                echo "📥 Cloning test suite..."
                git clone $TEST_REPO $TEST_DIR
                '''
            }
        }

        stage('Build & Run Selenium Tests') {
            steps {
                dir("$TEST_DIR") {
                    sh '''
                    echo "🐳 Building Docker image for tests..."
                    docker build -t noteapp-tests .

                    echo "🧪 Running tests..."
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
                    script: "cd $MAIN_DIR && git log -1 --pretty=format:'%ae'",
                    returnStdout: true
                ).trim()

                emailext (
                    to: authorEmail,
                    subject: "✅ Jenkins Test Results - ${currentBuild.currentResult}",
                    body: """
Hi ${authorEmail},

Your GitHub push triggered an automated test run via Jenkins.

🔧 *Status:* ${currentBuild.currentResult}  
🔁 *Build #:* ${env.BUILD_NUMBER}  
📜 *Details:* ${env.BUILD_URL}

Regards,  
🤖 Jenkins Bot
""",
                    attachmentsPattern: "${TEST_DIR}/test_output.txt"
                )
            }
        }
    }
}
