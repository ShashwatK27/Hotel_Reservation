pipeline {
  agent any

  environment{
  VENV_DIR = 'venv'
  GCP_PROJECT = "project-4b9b9e01-df7f-4cad-803"
  GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
  }

  stages{
    stage('Cloning GitHub repo to Jenkins'){
      steps{
        script{
          echo 'Cloning Github Repo to Jenkins'
          checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/ShashwatK27/Hotel_Reservation.git']])
        }
      }
    }
    stage('Setting up Virtual Environment'){
      steps{
        script{
          echo 'Setting up Virtual Environment..............'
          sh '''
          python -m venv ${VENV_DIR}
          . ${VENV_DIR}/bin/activate
          pip install --upgrade pip
          pip install -e . 
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
          export PATH=$PATH:${GCLOUD_PATH}

          gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

          gcloud config set project ${GCP_PROJECT}

          gcloud auth configure-docker --quiet

          docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

          docker push gcr.io/${GCP_PROJECT}/ml-project:latest
          '''
        }
      }
      }
    }
  }
}