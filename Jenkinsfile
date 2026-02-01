pipeline {
  agent any

  options {
    skipDefaultCheckout(true)
  }

  environment{
  VENV_DIR = 'venv'
  GCP_PROJECT = "project-4b9b9e01-df7f-4cad-803"
  }

  stages{
    stage('Cloning GitHub repo to Jenkins'){
      steps{
        script{
          echo 'Cloning Github Repo to Jenkins'
           deleteDir()
          checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/ShashwatK27/Hotel_Reservation.git']])
        }
      }
    }
    stage('Setting up Virtual Environment'){
      steps{
        script{
          echo 'Setting up Virtual Environment..............'
          sh '''
      /usr/bin/python3 -m venv venv

      venv/bin/python -m pip install --upgrade pip
      venv/bin/pip install -e .
    '''
        }
      }
    }
    stage('Pushing Docker image to GCR'){
      steps{
        withCredentials([file(credentialsId:'gcloud-token', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
        script{
          echo 'Pushing Docker image to GCR..............'
          sh '''

          gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

          venv/bin/python pipelines/training_pipeline.py

          gcloud config set project ${GCP_PROJECT}

          gcloud auth configure-docker --quiet

          docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

          docker push gcr.io/${GCP_PROJECT}/ml-project:latest
          '''
        }
      }
      }
    }

    stage('Deploy to Google Cloud Run'){
      steps{
        withCredentials([file(credentialsId:'gcloud-token', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
        script{
          echo 'Deploying to Google Cloud Run.........'
          sh '''

          gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

          venv/bin/python pipelines/training_pipeline.py

          gcloud config set project ${GCP_PROJECT}

          gcloud run deploy ml-project \
              --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
              --platform=managed \
              --region=us-central1 \
              --allow-unauthenticated
          '''
        }
      }
      }
    }
  }
}