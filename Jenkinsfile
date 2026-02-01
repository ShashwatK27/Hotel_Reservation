pipeline {
  agent any

  stages{
    stage('Cloning GitHub repo to Jenkins'){
      steps{
        script{
          echo 'Cloning Github Repo to Jenkins'
          checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/ShashwatK27/Hotel_Reservation.git']])
        }
      }
    }
  }
}