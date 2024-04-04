pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Kalp16219/TechnicalTest.git'
            }
        }
        
        stage('Terraform Apply') {
            steps {
                sh 'terraform init'
                sh 'terraform apply -auto-approve'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t kalptest .'
            }
        }
        
        stage('Push to AWS ECR') {
            steps {
                sh 'aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account-id.dkr.ecr.your-region.amazonaws.com'
                sh 'docker tag kalptest:latest kalpeshsp982495:kalptest'
                sh 'docker push kalpeshsp982495:kalptest'
            }
        }
        
        stage('Apply Lambda') {
            steps {
                sh 'terraform init lambda-resources'
                sh 'terraform apply -auto-approve lambda-resources'
            }
        }
    }
    
}
