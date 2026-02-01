pipeline {
  agent any

  environment {
    VENV_DIR    = 'venv'
    GCP_PROJECT = 'project-4b9b9e01-df7f-4cad-803'
    GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
  }

  stages {

    stage('Setup Python Environment') {
      steps {
        sh '''
          echo "Creating virtual environment"
          python -m venv ${VENV_DIR}

          echo "Activating virtual environment"
          . ${VENV_DIR}/bin/activate

          echo "Upgrading pip"
          pip install --upgrade pip

          echo "Installing project in editable mode"
          pip install -e .
        '''
      }
    }

    stage('Build & Push Docker Image to GCR') {
      steps {
        withCredentials([
          file(credentialsId: 'gcloud-token', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
        ]) {
          sh '''
            echo "Adding gcloud to PATH"
            export PATH=$PATH:${GCLOUD_PATH}

            echo "Authenticating with GCP"
            gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

            echo "Setting GCP project"
            gcloud config set project ${GCP_PROJECT}

            echo "Configuring Docker for GCR"
            gcloud auth configure-docker gcr.io --quiet

            echo "Building Docker image"
            docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

            echo "Pushing Docker image to GCR"
            docker push gcr.io/${GCP_PROJECT}/ml-project:latest
          '''
        }
      }
    }
  }

  post {
    success {
      echo '🎉 Pipeline completed successfully!'
    }
    failure {
      echo '❌ Pipeline failed. Check logs above.'
    }
  }
}
