pipeline {
  agent any

  environment{
  VENV_DIR = 'venv'
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
  }
}