
pipeline {
    //Kubernetes agent for dynamic slave/pod configuration
    agent {
		kubernetes {
		//	label "jenkins"
		//	defaultContainer "alpine"
			yamlFile "spec.yaml"
		}
	}
    //triggers { pollSCM('* * * * *') }
    options {
        timestamps()
    }

    environment {
        DOCKER_REGISTRY='docker.io'
        DOCKER_REPOSITORY= 'Vasilichru'
        APP_NAME="covid_app"
    }

    stages {
        //test stage
 /*       stage('test') {
		steps {
        		container('maven') {
          		//sh 'mvn -version'
			echo '===== TEST 4====='
			}
		}
        } */
	
        stage('Build and Push Docker Image...') {
          steps {
                script {
                  // DOCKER HUB
                  
                  /* Build the container image */            
                  def dockerImage = docker.build("my-image:test")
                        
                  /* Push the container to the docker Hub */
                  dockerImage.push()

                  /* Remove docker image*/
                  //sh 'docker rmi -f my-image:${env.BUILD_ID}'
		  sh 'echo its ok images'

                } 
            } 
        }
    }
	
}

