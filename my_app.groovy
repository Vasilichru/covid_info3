
pipeline {
    //Kubernetes agent for dynamic slave/pod configuration
    agent {
		kubernetes {
			label "kubeagent"
			defaultContainer "jnlp"
			yamlFile "ci/spec.yaml"
		}
	}
    triggers { pollSCM('* * * * *') }
    parameters {
    }


    options {
        timestamps()
    }

    environment {
        DOCKER_REGISTRY='docker.io'
        DOCKER_REPOSITORY= 'Vasilichru'
        APP_NAME="covid-app"
    }

    stages {
        //test stage
        stage('test') {
		steps {
			echo '===== TEST ====='	
		}
        }


        //Pre-Build stage to find out the user(who has started the build job)
/*        stage('Build Environment') {
            steps {
                notify('STARTED')
                githubstatus('STARTED')
                echo sh(script: 'env|sort', returnStdout: true)
                script {
                    def git_branch = "${GIT_BRANCH}"
                        git_branch = git_branch.replace("/", "_")
                    USER = wrap([$class: 'BuildUser']) {
                        return env.BUILD_USER
                    }
                    NGINX_VERSION = "1.21.3"
                    INIT_VERSION = "1"
                    IMAGE_NAME = APP_NAME + "-" + ENVIRONMENT
                    //IMAGE_TAG = INIT_VERSION + "-" + GIT_BRANCH + "-" + BUILD_NUMBER
                    IMAGE_TAG = INIT_VERSION + "-" + GIT_BRANCH + "-" + BUILD_NUMBER
                }
            }
        }

        stage('Checkout Overrides repo') {
            steps {
                script {
                dir("$VAR_CHECKOUT_FOLDER") {
                    def git_repo = 'git@spruce.arlo.com:SOME_REPO/SOME_REPO.git'
                    def cred = 'SECRET'
                        git branch: params.OVERRIDES_REPO, url: git_repo, credentialsId: cred
                    }
                }
            }
        }

        stage("Get Git Tag of a branch") {
            steps{
                script{
                        withCredentials([sshUserPrivateKey(credentialsId: keyId, keyFileVariable: 'GITHUB_KEY')]) {
                            withEnv(["GIT_SSH_COMMAND=ssh -i $GITHUB_KEY -o StrictHostKeyChecking=no"]) {
                                sh("""
                                    git config --global user.name "${userName}"
                                    git config --global user.email ${userEmail}
                                    git config --global -l
                                    git rev-parse --short HEAD
                                """)

                                GIT_COMMIT_1 = sh(script: 'git rev-parse --short=16 HEAD',returnStdout: true).trim()
                                //GIT_COMMIT_2 = sh(script: 'git log --oneline --abbrev=16',returnStdout: true).trim()
                                INIT_IMAGE_TAG = "nginx-${NGINX_VERSION}-${BUILD_NUMBER}-${GIT_COMMIT_1}"
                                //echo "nginx-${NGINX_VERSION}-${BUILD_NUMBER}-${GIT_COMMIT_2}"
                            }
                        }
                    }
                }
        }

         stage('Checkout Init Container repo') {
             steps {
                 script {
                 def git_repo = 'git@sXXXX:SOME_REPO/SOME_REPO.git'
                 def cred = 'sXXXXXX'
                     git branch: "${GIT_BRANCH}", url: git_repo, credentialsId: cred
                     sh 'mv $VAR_CHECKOUT_FOLDER/values.yaml values.yaml'
                     echo "$GIT_COMMIT"
                 }
             }
         }


        stage('NginxPlus step') {
             when {
                 expression { params.BUILD_NGINXPLUS == 'yes' }
             }
             steps {

                 container('artifactory') {   
                     script {

                         sh "ls -la"

                         dir("$NGINXPLUS_FOLDER") {

                             sh "ls -la"
                             image_name = 'base-nginxplus'
                             image_tag = INIT_VERSION + "-" + GIT_BRANCH + "-" + BUILD_NUMBER
                             docker.build("${DOCKER_REGISTRY}/${DOCKER_REPOSITORY}/${image_name}" + ":" + "${image_tag}")

                             echo "Pushing image"
                             echo "Image: ${DOCKER_REPOSITORY}/${image_name}, Image tag: ${image_tag}"
                             dockerpush("${DOCKER_REPOSITORY}/${image_name}","${image_tag}","${DOCKER_REPOSITORY}")

                             NGINX_IMAGE = "${DOCKER_REGISTRY}/${DOCKER_REPOSITORY}/${image_name}" + ":" + "${image_tag}"
                             echo "-------------LATEST NGINX_IMAGE is ${NGINX_IMAGE}------------"
                         }
                     }
                 }
             }
         }*/



/*         stage("Build image") {
		steps {
                 container('artifactory') {
                     script {
                         docker.build("${DOCKER_REGISTRY}/${DOCKER_REPOSITORY}/${IMAGE_NAME}" + ":" + "${INIT_IMAGE_TAG}")
                     }
                 }
             }
 	}

         stage("Test image") {
 		steps {
                 container('artifactory') {
                     script {
                         docker.image("${DOCKER_REGISTRY}/${DOCKER_REPOSITORY}/${IMAGE_NAME}" + ":" + "${INIT_IMAGE_TAG}").inside {
                         }
                     }
                 }
             }
	 }

        stage("Push images") {
            steps {
                container('artifactory') {
                    script {
                        echo "Pushing image"
                        echo "Image: ${DOCKER_REPOSITORY}/${IMAGE_NAME}, Image tag: ${INIT_IMAGE_TAG}"
                        dockerpush("${DOCKER_REPOSITORY}/${IMAGE_NAME}","${INIT_IMAGE_TAG}","${DOCKER_REPOSITORY}")
                    }
                }
            }
        }*/


    }
}

