
pipeline {
    //Kubernetes agent for dynamic slave/pod configuration
    agent {
		kubernetes {
			label "kubeagent"
			defaultContainer "jnlp"
			yamlFile "spec.yaml"
		}
	}
    triggers { pollSCM('* * * * *') }
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
        stage('test') {
		steps {
			echo '===== TEST ====='	
		}
        }
    }
}

