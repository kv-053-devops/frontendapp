pipeline {

  environment {
    PROJECT = "demo2-248908"
    APP_NAME = "frontendapp"
    STORAGE_CREDS = "${PROJECT}"
    FE_SVC_NAME = "${APP_NAME}-frontend"
    CLUSTER = "demo2-gke-cluster"
    CLUSTER_ZONE = "europe-west3-a"
    IMAGE_TAG = "eu.gcr.io/${PROJECT}/${APP_NAME}:${BUILD_NUMBER}"
    JENKINS_CRED = "${PROJECT}"
    APP_REPO="https://github.com/kv-053-devops/frontendapp.git"
    NAMESPACE="dev"
  }

 agent {
    kubernetes {
      yaml """
apiVersion: v1
kind: Pod
metadata:
labels:
  component: ci
spec:
  # Use service account that can deploy to all namespaces
  serviceAccountName: jenkins-sa
  volumes:
  - name: dockersock
    hostPath:
      path: /var/run/docker.sock
  - name: jenkins-gcr-sa-creds
    secret:
      secretName: jenkins-gcr-json
  containers:
  - name: git
    image: gcr.io/cloud-builders/git
    command:
    - cat
    tty: true
  - name: python
    image: gcr.io/cloud-marketplace/google/python
    command:
    - cat
    tty: true
  - name: docker
    image: gcr.io/cloud-builders/docker
    command:
    - cat
    tty: true
    volumeMounts:
    - name: dockersock
      mountPath: /var/run/docker.sock
    - name: jenkins-gcr-sa-creds
      mountPath: /tmp/gcr/
      readOnly: true
  - name: kubectl
    image: gcr.io/cloud-builders/kubectl
    command:
    - cat
    tty: true
"""
}
  }
  stages {
    stage('Checkout') {
        steps {
            git branch: 'master', url: "${APP_REPO}"
        }
    }
    stage('Code test') {
        steps {
        container('python'){
            sh "pip3 install -r requirements.txt";
            sh "python3 unit_test.py";
          }
        }
    }

    stage('Build and push container') {
      steps {
        container('docker') {
        //  sh "cd $WORKSPACE/repo/${APP_NAME}";
         sh "docker build -t ${IMAGE_TAG} .";
         sh "docker images";
        }
    } 
} 
        stage('Push container') {
      steps {
        container('docker') {
          sh "cat /tmp/gcr/jenkins-gcr.json | docker login -u _json_key --password-stdin https://eu.gcr.io";
          sh "docker push ${IMAGE_TAG}";
			// script {
      //       docker.withRegistry("https://eu.gcr.io", "gcr:${STORAGE_CREDS}") {
      //       sh "docker push ${IMAGE_TAG}"
			//      }
      //   }
    }}}
        stage('Deploy') {
      steps {
        container('kubectl') {
         sh "kubectl get deployments --namespace=${NAMESPACE} | grep ${APP_NAME} &&  kubectl patch deployment ${APP_NAME} --namespace=${NAMESPACE} || kubectl create deployment ${APP_NAME} --image=${IMAGE_TAG} --namespace=${NAMESPACE}"
         //sh "kubectl get pods";
         //sh "kubectl expose deployment hello-web --type=LoadBalancer --port 81 --target-port 8081";
        }
    } 
}

}
}
