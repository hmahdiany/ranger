package kubecontext

import (
	"fmt"
	"log"
	"os"
	"path/filepath"

	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/client-go/util/homedir"
)

func CreateContext(kubeconfig string) (*kubernetes.Clientset, error) {

	if kubeconfig == "" {
		fmt.Println("using default kubectl config file: ~/.kube/config")
		kubeconfig = filepath.Join(homedir.HomeDir(), ".kube", "config")

		if _, err := os.Stat(kubeconfig); err != nil {
			log.Fatal(err)
		}
	}

	// check if input kubectl config file exists
	if _, err := os.Stat(kubeconfig); err != nil {
		log.Fatal(err)
	}

	// use the current context in kubeconfig
	config, err := clientcmd.BuildConfigFromFlags("", kubeconfig)
	if err != nil {
		panic(err.Error())
	}

	// create the clientset
	clientset, err := kubernetes.NewForConfig(config)
	return clientset, err
}
